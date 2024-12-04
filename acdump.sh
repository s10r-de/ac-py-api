#!/bin/bash
. ./.venv/bin/activate
export PYTHONPATH=$PWD/active_collab_app:$PWD/active_collab_storage:$PWD/active_collab_api:$PYTHONPATH
exec python3 active_collab_app/main.py "$@"
