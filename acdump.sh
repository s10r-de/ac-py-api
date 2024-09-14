#!/bin/bash
. ./.venv/bin/activate
export PYTHONPATH=$PWD/AcDump:$PWD/AcStorage:$PWD/ActiveCollabAPI:$PYTHONPATH
exec python3 AcDump/main.py "$@"
