# Database DevOps

Quantum Bank treats a database backend swap and a schema rollout as **gated,
reversible units of change** rather than a redeploy. This is the pattern
**Harness Database DevOps** is built for: version the schema, promote it through
environments, and pair it with a feature flag so it can be turned off in seconds.

## Where it lives

| Concern | File |
|---------|------|
| Versioned schema | [`migrations/001_initial.sql`](../migrations/001_initial.sql) |
| Backend-agnostic data layer | [`dao/`](../dao/), [`models.py`](../models.py) |
| Backend selection + rollout flags | [`db_flags.py`](../db_flags.py) |
| Local Postgres setup | [LOCAL_POSTGRES.md](LOCAL_POSTGRES.md) |
| Rollout walkthrough | [demos/rewards-rollout.md](demos/rewards-rollout.md) |

## Dual-backend data layer

One set of query functions runs on **both** SQLite and PostgreSQL. The layer
normalizes the differences that usually leak into app code:

- parameter style (`?` vs `%s`),
- `RETURNING id` vs `lastrowid`,
- `Decimal`/`datetime` typing (Postgres returns typed values; SQLite returns
  strings).

Because the same suite runs against either engine, a backend swap is a
configuration change, not a rewrite. See [feature-flags.md](feature-flags.md)
for how the backend is selected.

## Schema as a gated rollout

The rewards-ledger rollout shows a schema change moving through states without a
redeploy, each step controlled by a flag from [`db_flags.py`](../db_flags.py):

1. **`DEMO_ROLLOUT_SCHEMA`** — apply the new schema (idempotent; safe to re-run).
2. **`DEMO_ROLLOUT_FEATURE`** — start reading/writing the new columns.
3. **`DEMO_FORCE_ROLLOUT_MIGRATION_FAIL`** — force the migration to fail, to
   rehearse rollback.

A **caller-owned savepoint** wraps the rewards write inside `transfer_money`, so
if the rollout logic fails the core transfer still commits. Turning a flag off
reverts behavior immediately; the schema change itself is idempotent and
reversible.

Full step-by-step: [demos/rewards-rollout.md](demos/rewards-rollout.md)
(baseline → fallback → ready → forced fail → recovery).

## Try it

```bash
# 1. Stand up local Postgres (see LOCAL_POSTGRES.md), then:
export DATABASE_URL="postgresql://YOUR_OS_USER@localhost:5432/quantum_bank"
export POSTGRES_DATABASE=on

# 2. Walk the rollout states:
export DEMO_ROLLOUT_SCHEMA=on      # apply schema
export DEMO_ROLLOUT_FEATURE=on     # use it
# ...or DEMO_FORCE_ROLLOUT_MIGRATION_FAIL=on to rehearse a failed migration.
python app.py
```
