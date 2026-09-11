#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 - <<'PY' >/dev/null 2>&1 || python3 -m pip install -r requirements.txt
import fastapi, uvicorn, multipart
PY
( sleep 2; python3 -m webbrowser http://127.0.0.1:8765 >/dev/null 2>&1 || true ) &
python3 run.py
