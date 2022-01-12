#!/bin/bash

MINIO_HELM_DEPLOYMENT=$(helm list --filter=minio | awk '{print $1}' | tail -n 1)
helm uninstall $MINIO_HELM_DEPLOYMENT
./remove_port_forwarding.sh -a

kubectl delete all --all

