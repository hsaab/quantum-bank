# Local PostgreSQL (native / bare metal)

Run QuantumBank against **PostgreSQL installed on your machine** — not Docker.
The app still defaults to **SQLite** when `POSTGRES_DATABASE` is off or
`DATABASE_URL` is unset.

For cloud deploy (Render, GCP Cloud SQL), see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
(dedicated cloud Postgres docs coming soon).

## Prerequisites

- Python 3.11+ and a project virtualenv (`python -m venv venv`)
- `pip install -r requirements.txt`
- **PostgreSQL 16** server and client tools on your host

We do **not** use Docker for local Postgres in this project.

## Install Postgres (macOS — Homebrew)

```bash
brew install postgresql@16
brew services start postgresql@16
```

If `brew services` fails with a missing data directory (Homebrew's post-install
caveat does not always create the cluster), initialize it once. The data dir
lives under the Homebrew prefix — find it with `brew --prefix`:

```bash
PG_DATA="$(brew --prefix)/var/postgresql@16"
initdb --locale=en_US.UTF-8 -E UTF-8 "$PG_DATA"
brew services restart postgresql@16
```

Verify:

```bash
pg_isready -h localhost
```

**Linux:** install `postgresql-16` (or equivalent) from your distro, start the
service, and use the same `createdb` / connection steps below with your OS user.

## Create the database (one-time)

```bash
createdb -h localhost quantum_bank
```

## Configure the app

Copy [`.env.example`](../.env.example) to `.env` if you have not already, then set:

```bash
# Native local Postgres (trust / peer auth — typical Homebrew default)
DATABASE_URL=postgresql://YOUR_OS_USER@localhost:5432/quantum_bank
POSTGRES_DATABASE=on
```

Replace `YOUR_OS_USER` with your macOS/Linux username (the role Postgres trusts
for local connections). No password is required for the default Homebrew trust
setup.

Other vars (`SPLIT_API_KEY`, `SECRET_KEY`) are unchanged — see the main
[README](../README.md).

## Run the app

```bash
source venv/bin/activate   # or: venv/bin/python ...
python app.py             # → http://localhost:5001  (not 5000)
```

Log in with the seeded user **`demo`** (no password — demo only).

On first startup with an empty `quantum_bank` database, `init_db()` applies
[`migrations/001_initial.sql`](../migrations/001_initial.sql) and seeds demo data.

## Smoke checklist

After login, confirm:

- [ ] Dashboard loads with account balances
- [ ] `/transactions` and `/account?id=…` render dates (no 500)
- [ ] A small transfer succeeds (UI or API)

Optional curl smoke (app running on port **5001**):

```bash
J=/tmp/qb-cookies.txt; rm -f "$J"
curl -s -o /dev/null -w "GET / -> %{http_code}\n" http://127.0.0.1:5001/
curl -s -c "$J" -b "$J" -o /dev/null -w "login -> %{http_code}\n" \
  -d "username=demo" http://127.0.0.1:5001/login
curl -s -b "$J" -o /dev/null -w "dashboard -> %{http_code}\n" \
  http://127.0.0.1:5001/dashboard
curl -s -b "$J" http://127.0.0.1:5001/api/accounts | grep -E '"account_number"|"balance"'
```

## Run tests against Postgres

Postgres must be running and `quantum_bank` must exist.

```bash
# Fresh DB (optional — re-seeds on init_db during tests)
dropdb -h localhost quantum_bank 2>/dev/null; createdb -h localhost quantum_bank

export DATABASE_URL="postgresql://YOUR_OS_USER@localhost:5432/quantum_bank"
export POSTGRES_DATABASE=on
pytest test/ -v
```

Default CI-style run (SQLite only):

```bash
unset DATABASE_URL
export POSTGRES_DATABASE=off
pytest test/ -v
```

## Reset the database

```bash
dropdb -h localhost quantum_bank
createdb -h localhost quantum_bank
# Next app start or init_db() re-seeds demo data
```

## Switch back to SQLite

```bash
unset DATABASE_URL
export POSTGRES_DATABASE=off
python app.py
```

Or remove those lines from `.env`. The app uses `quantum_bank.db` in the project
root by default.

## Troubleshooting

| Symptom | What to try |
|---------|-------------|
| `connection refused` on 5432 | `brew services start postgresql@16` (or your distro equivalent); `pg_isready -h localhost` |
| `database "quantum_bank" does not exist` | `createdb -h localhost quantum_bank` |
| Port **5001** already in use | Flask debug reloader may leave a child process — stop with `pkill -f "python app.py"` or use a free port temporarily |
| Stale schema / old `card_number` columns | You may have an old SQLite file — delete `quantum_bank.db` when testing SQLite; for PG use `dropdb` + `createdb` |
| Split logs `postgres_database` missing | Harmless — set `POSTGRES_DATABASE=on` in `.env`; creating the Split flag is optional |
| Managed cloud Postgres later | Use `?sslmode=require` (or Cloud SQL Auth Proxy) and ensure the DB role can **CREATE** tables — see CHUNK_5 deploy docs |

## DB role note

Local superuser / your OS user can run DDL — fine for development. Managed
Postgres (Render, Cloud SQL) may require granting CREATE on the target schema
or applying `migrations/001_initial.sql` out-of-band before first boot.
