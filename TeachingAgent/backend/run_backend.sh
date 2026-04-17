#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON_BIN="$WORKSPACE_ROOT/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Python venv not found at $PYTHON_BIN"
  echo "Create it first, e.g. from workspace root: python3 -m venv .venv"
  exit 1
fi

cd "$SCRIPT_DIR"
exec "$PYTHON_BIN" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir app
