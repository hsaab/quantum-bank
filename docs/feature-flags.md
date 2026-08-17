# Feature flags

Quantum Bank uses feature flags for more than toggling UI: one flag switches the
**entire persistence layer** between SQLite and PostgreSQL at runtime, and other
flags drive a progressive schema rollout and live front-end variant switching.

Flags are managed with **Harness FME** (Feature Management & Experimentation),
which uses the Split SDK. The server-side client is `splitio-client`
(see [`requirements.txt`](../requirements.txt)); the browser uses the JS SDK.

## Where it lives

| Concern | File |
|---------|------|
| SDK initialization (server) | [`split_config.py`](../split_config.py) |
| Flag resolution + guards | [`db_flags.py`](../db_flags.py) |
| Browser SDK (live variant switching) | [`static/js/split-client.js`](../static/js/split-client.js) |
| API keys | [`.env.example`](../.env.example) → `.env` |
| Flag definitions / dashboard setup | [SPLITIO_SETUP.md](SPLITIO_SETUP.md) |

## The flags

| Flag | Type | What it gates |
|------|------|---------------|
| `postgres_database` | server | SQLite vs PostgreSQL backend selection |
| `home_page_variant` | browser | Which home/pricing variant renders |
| `demo_mode` | browser | Pre-loads variants for refresh-free live switching |
| `DEMO_ROLLOUT_SCHEMA` | env | Allow applying the demo schema change (idempotent) |
| `DEMO_ROLLOUT_FEATURE` | env | Read/write the new schema once it exists |
| `DEMO_FORCE_ROLLOUT_MIGRATION_FAIL` | env | Force a migration failure to demo rollback |

The `DEMO_*` flags are intentionally env-driven so the rollout walkthrough is
reproducible without a live dashboard. See [db-devops.md](db-devops.md).

## Resolution order and the safety guard

`is_postgres_database_enabled()` in [`db_flags.py`](../db_flags.py) resolves in
this order:

1. **Harness FME treatment** — if the SDK returns `on`/`off`, that wins.
2. **`POSTGRES_DATABASE` env var** — used when FME returns `control` or is
   unavailable (no key, timeout, error).
3. **Default `off`** — SQLite.

Even when the flag resolves **on**, the app stays on SQLite (and logs a warning)
unless `DATABASE_URL` is set. A half-finished rollout therefore cannot take the
app down — the flag and the connection string must *both* be present.

## Try it

```bash
# Flip via env (no dashboard needed):
export POSTGRES_DATABASE=on
export DATABASE_URL="postgresql://YOUR_OS_USER@localhost:5432/quantum_bank"
python app.py            # data layer now targets Postgres

# Flip the flag off again → next get_db() falls back to SQLite, no redeploy.
```

To drive the same flag from the FME dashboard instead of env, set
`SPLIT_API_KEY` and define `postgres_database` per [SPLITIO_SETUP.md](SPLITIO_SETUP.md).
