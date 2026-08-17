# Working notes — rod k8s Postgres manifest (PAUSED)

_Gitignored scratch notes. Picking this back up later._

## Goal
Stand up a self-contained QuantumBank demo stack on Kubernetes — Postgres + the
app — modeled on a reference YAML the user had (3 Postgres envs + a default Mongo).
We pared it down to ONE Postgres, dropped Mongo, used a Secret for creds.

## Status: DONE (created + verified), NOT YET APPLIED to a cluster

### File created
`.harness/kubernetes/rod-quantum-bank-postgres.yaml` — single `---`-separated file,
namespace **`quantum-db`** (user pre-created this in GKE). 7 resources:

1. **Secret** `quantum-bank-secrets` — Postgres creds, `DATABASE_URL`, + app secrets
2. **ConfigMap** `init-db-schema` — schema, verbatim copy of `migrations/001_initial.sql`
3. **Service** `postgres` (ClusterIP, 5432)
4. **StatefulSet** `postgres` (postgres:16.10, 1 replica, 10Gi PVC, creds via secretKeyRef)
5. **Job** `init-schema` (waits on pg_isready, runs psql against init.sql)
6. **Deployment** `rod-quantum-bank-backend` (2 replicas, wired to PG via Secret)
7. **Service** `rod-quantum-bank-backend` (LoadBalancer, port 80 → targetPort 5000)

Hassan's `hsaab-*` manifests were intentionally left UNTOUCHED.

### Verified
- `kubectl apply --dry-run=client` — all 7 resources validate.
- Schema parity check (python): ConfigMap `init.sql` == `migrations/001_initial.sql`
  (modulo `IF NOT EXISTS`). `card_last4` present; `card_number`/`cvv` absent.

## Key decisions made
- **Single Postgres, no Mongo** — db1/db2/db3 in the reference was just the user's
  multi-env default; app only uses one `quantum_bank` DB.
- **Secret for creds** (user's choice) — demo-grade `secretpass` inline in the Secret.
- **App + DB packaged together** in one file — fine here because this is a
  hand-applied standalone stack, NOT driven by Hassan's CI pipeline (which churns
  the image on every `<+pipeline.sequenceId>` push). Coupling cadence was the only
  best-practice concern and it doesn't apply.
- **`POSTGRES_DATABASE: "on"`** kept on the Deployment (final recommendation):
  resting default = Postgres so the provisioned DB isn't dead weight; Split
  `postgres_database` flag still OVERRIDES the env in both directions, so the
  feature flag remains the live controller. Works for both backends today.

## Corrections vs the user's original draft
- **cards table (critical):** draft invented `card_number` + `cvv`. Real schema has
  `card_last4` ONLY (models.py:572 inserts card_last4; file header forbids CVV/PAN).
- DB name `mydb` → `quantum_bank` (what the app's DATABASE_URL expects).
- bare `CREATE TABLE` → `CREATE TABLE IF NOT EXISTS` (app's init_db() also creates
  schema on boot — bare CREATE races and fails the Job's backoffLimit).
- inline `secretpass` → Kubernetes Secret.
- added `namespace`.

## Flag resolution recap (db_flags.py)
get_db() → using_postgres() (models.py:36) → is_postgres_database_enabled() (db_flags.py:20)
Order: Split `postgres_database` treatment → `POSTGRES_DATABASE` env → default off.
Guard: flag-on but `DATABASE_URL` unset → logs warning, stays on SQLite (db_flags.py:62).
So DATABASE_URL is a PREREQUISITE (reachability), not the switch.

## TODO before applying (left for next session)
1. **Fill app secrets** in the Secret — `SECRET_KEY` and `SPLIT_API_KEY` are
   `REPLACE_ME` placeholders. Real values are in `.env` (NOT copied in — would leak
   into a tracked file). Option: inject out-of-band via `kubectl create secret`.
2. **Confirm app image** — used `hsaab/quantum-bank-backend:latest` (only built image;
   rod pipeline is test-only, no push). Swap registry/tag if needed.
3. Decide whether to keep the redundant schema **Job** (app's init_db() also creates
   + SEEDS the demo user; Job only creates empty tables). Both idempotent. Currently kept.

## Apply sequence (when resuming)
```bash
kubectl apply -f .harness/kubernetes/rod-quantum-bank-postgres.yaml
kubectl -n quantum-db rollout status statefulset/postgres
kubectl -n quantum-db wait --for=condition=complete job/init-schema
kubectl -n quantum-db exec statefulset/postgres -- psql -U admin -d quantum_bank -c '\dt'
kubectl -n quantum-db get svc rod-quantum-bank-backend   # grab LoadBalancer external IP
```
