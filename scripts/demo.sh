#!/usr/bin/env bash
# One-command demo runner for peers / portfolio viewers.
#
# Bootstraps a venv, installs deps, ensures a SECRET_KEY, then starts the
# Flask dev server on http://localhost:5001/demo so the home page lands
# directly in demo mode.
#
# Postgres is intentionally NOT spun up here — SQLite is the zero-config
# default and the whole point of the postgres_database flag is that the
# app works without it. To demo the Postgres backend, see docs/LOCAL_POSTGRES.md
# and run with DATABASE_URL + POSTGRES_DATABASE=on already set.
set -euo pipefail
cd "$(dirname "$0")/.."

VENV="${VENV:-.venv}"
PORT="${PORT:-5001}"
PY="${PYTHON:-python3}"

if [ ! -d "$VENV" ]; then
  echo "[demo] creating venv at $VENV"
  "$PY" -m venv "$VENV"
fi

# shellcheck disable=SC1091
. "$VENV/bin/activate"

echo "[demo] installing requirements"
pip install --quiet --upgrade pip >/dev/null
pip install --quiet -r requirements.txt

# Stable session key so refreshes don't log the demo user out.
export SECRET_KEY="${SECRET_KEY:-quantum-bank-demo-key-not-for-prod}"

# Surface (rather than hide) the most common misconfig: SPLIT_API_KEY missing.
# The app handles that gracefully, but a peer running this should see why.
if [ -z "${SPLIT_API_KEY:-}" ]; then
  echo "[demo] SPLIT_API_KEY not set — falling back to env/default treatments (this is fine for a local demo)"
fi

if [ -n "${DATABASE_URL:-}" ] && [ "${POSTGRES_DATABASE:-off}" = "on" ]; then
  echo "[demo] Postgres backend ENABLED via DATABASE_URL + POSTGRES_DATABASE=on"
else
  echo "[demo] SQLite backend (default). Set DATABASE_URL + POSTGRES_DATABASE=on to flip."
fi

URL="http://localhost:${PORT}/demo"
echo "[demo] starting Flask on ${URL}"
echo "[demo] Ctrl+C to stop."

# Open browser in a background subshell with a short delay so the server
# binds first. Best-effort — silently no-ops on platforms without `open`.
(
  sleep 1
  if command -v open >/dev/null 2>&1; then
    open "$URL" || true
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL" || true
  fi
) &

exec python app.py
