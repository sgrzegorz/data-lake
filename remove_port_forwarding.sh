#!/bin/bash

usage() {
    echo "Usage: $0 [-a]"
    echo "Without arguments remove port forwarding only from the current minio deployment."
    echo "Arguments:"
    echo "-a, remove all minio port forwardings"
}

MINIO_HELM_DEPLOYMENT=$(helm list --filter=minio | awk '{print $1}' | tail -n 1)

while getopts "ah" o; do
    case "${o}" in
        a)
            MINIO_HELM_DEPLOYMENT="minio"
            ;;
        h)
            usage
            ;;
        *)
            ;;
    esac
done

while (($(ps aux | grep "$MINIO_HELM_DEPLOYMENT" | grep "port-forward" | wc -l) > 0 )); do
  PID_TO_REMOVE=$(ps aux | grep "$MINIO_HELM_DEPLOYMENT" | grep "port-forward" | awk '{print $2}' | head -n 1)
  echo "Removing port forwarding of $MINIO_HELM_DEPLOYMENT with pid $PID_TO_REMOVE"
  kill -9 $PID_TO_REMOVE
done

