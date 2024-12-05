#!/usr/bin/bash
cd /app || exit 1
source .venv/bin/activate
echo "python3 active_collab_app/main.py \$@"
exec python3 active_collab_app/main.py "$@"
