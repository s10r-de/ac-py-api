#!/bin/bash
#set -x
set -e

t_oldest=$(date --date="2 days ago" +%s)

SERVICE_NAME=activecollab

for SNAP in $(sudo lvdisplay -c |awk -F: "/${SERVICE_NAME}-snap-20/{print \$1}"); do
    snap_date=$(echo "${SNAP}" | awk -F- '{print $3}')
    t_snap_date=$(date --date="${snap_date}" +%s)
    echo "check age of ${SNAP} timestamp=${snap_date}"
    if [ $t_snap_date -lt $t_oldest ]; then
        echo lvremove -f "${SNAP}"
        #lvremove -f "${SNAP}"
    fi
done