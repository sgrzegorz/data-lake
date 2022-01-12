#!/bin/bash

# add minio helm charts repo
echo "Adding minio helm chart repo..."
helm repo add minio https://charts.min.io/

# deploy minio standalone with small hardware requirements
echo "Installing minio..."
helm install --namespace default -f minio/values.yaml --generate-name minio/minio

MINIO_HELM_DEPLOYMENT=$(helm list --filter=minio | awk '{print $1}' | tail -n 1)

# install minio coinbase feeder
kubectl apply -f loader/deployment.yaml

# export ports
echo "Exporting ports..."
kubectl port-forward service/$MINIO_HELM_DEPLOYMENT 9000:9000 --namespace default &
kubectl port-forward service/$MINIO_HELM_DEPLOYMENT-console 9001:9001 --namespace default &

