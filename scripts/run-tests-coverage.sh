#!/usr/bin/env bash
# Local coverage gate (CI uses plain `pytest` without these flags; see pytest.ini).
set -euo pipefail
cd "$(dirname "$0")/.."
exec pytest -q \
  --cov=app \
  --cov=api \
  --cov=models \
  --cov=split_config \
  --cov-config=.coveragerc \
  --cov-report=term-missing \
  --cov-fail-under=90 \
  "$@"
