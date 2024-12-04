#!/bin/bash
. ./.venv/bin/activate
export PYTHONPATH=$PWD/AcDump:$PWD/AcStorage:$PWD/active_collab_api:$PYTHONPATH
exec python3 AcDump/main.py "$@"
