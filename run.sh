#!/bin/bash

MINIO_DEPLOYMENT_NAME="minio"

# add minio helm charts repo
echo "Adding minio helm chart repo..."
helm repo add minio https://charts.min.io/

# deploy minio standalone with small hardware requirements
echo "Installing minio..."
helm install $MINIO_DEPLOYMENT_NAME --namespace default -f minio/values.yaml minio/minio


# install minio coinbase feeder
kubectl apply -f loader/deployment.yaml

# export ports
echo "Exporting ports..."
kubectl port-forward service/$MINIO_DEPLOYMENT_NAME 9000:9000 --namespace default &
kubectl port-forward service/$MINIO_DEPLOYMENT_NAME-console 9001:9001 --namespace default &

