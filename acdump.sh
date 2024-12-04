#!/bin/bash
. ./.venv/bin/activate
export PYTHONPATH=$PWD/AcDump:$PWD/active_collab_storage:$PWD/active_collab_api:$PYTHONPATH
exec python3 AcDump/main.py "$@"
