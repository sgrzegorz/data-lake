#!/bin/bash

MINIO_DEPLOYMENT_NAME="minio"
helm uninstall $MINIO_DEPLOYMENT_NAME
./remove_port_forwarding.sh -a

helm uninstall sparkoperator

kubectl delete sparkapplication spark-job

kubectl delete sparkapplication scheduled-spark-job

kubectl delete all --all

