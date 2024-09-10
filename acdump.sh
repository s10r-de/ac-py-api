#!/bin/bash
. ./.venv/bin/activate
export PYTHONPATH=$PWD/:$PYTHONPATH
exec python3 AcDump/main.py "$@"
