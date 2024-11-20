#/usr/bin/bash
cd /app
source .venv/bin/activate
echo "python3 AcDump/main.py \$@"
exec python3 AcDump/main.py $@
