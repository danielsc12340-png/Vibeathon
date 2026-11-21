#!/usr/bin/env sh
cd "$(dirname "$0")"
PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then echo "No se encontró Python 3. Instálalo desde https://www.python.org/downloads/"; exit 1; fi
[ -x .venv/bin/python ] || "$PY" -m venv .venv
.venv/bin/python -m pip install -q -r requirements.txt
exec .venv/bin/python run.py "$@"
