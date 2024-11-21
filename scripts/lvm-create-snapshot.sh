#!/bin/bash
## run with sudo -E
#set -x
set -e

TODAY=$(date +%Y%m%d)
SNAP_SIZE="25G"
LOCK_FILE=/tmp/$(basename $0).lock

SERVICE_NAME=activecollab

SNAP="${SERVICE_NAME}-snap-${TODAY}"


function create_lvm_snapshot() {
    echo "$0: cleanup old snapshots..."
    ./scripts/lvm-cleanup-snapshots.sh

    echo "$0: create snapshot..."
    lvcreate -L "${SNAP_SIZE}" -s -n "${SNAP}" "/dev/mapper/vg0-${SERVICE_NAME}"
}

function cleanup() {
    set +e  # ignore errors
    echo "$0: cleanup ..."
    # we keep the snapshots to be able to do quicker recovery
    # too old snaps will be cleanup separately
    rm -f "${LOCK_FILE}" 2>/dev/null
}

trap cleanup SIGINT
trap cleanup SIGTERM
trap cleanup SIGQUIT
trap cleanup EXIT

if [ -e "${LOCK_FILE}" ]; then
	echo "ERROR: another backup is running!"
	exit 2
fi
date +%s > "${LOCK_FILE}"

create_lvm_snapshot

echo "$0: Finished."