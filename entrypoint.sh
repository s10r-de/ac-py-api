#/usr/bin/bash
cd /app
source .venv/bin/activate
echo "python3 active_collab_app/main.py \$@"
exec python3 active_collab_app/main.py $@
