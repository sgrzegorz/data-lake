#!/bin/bash

MINIO_DEPLOYMENT_NAME="minio"
helm uninstall $MINIO_DEPLOYMENT_NAME
./remove_port_forwarding.sh -a

helm uninstall sparkoperator

kubectl delete sparkapplications --all

kubectl delete all --all
