#!/bin/bash

MINIO_DEPLOYMENT_NAME="minio"

# add minio helm charts repo
echo "Adding minio helm chart repo..."
helm repo add minio https://charts.min.io/

# deploy minio standalone with small hardware requirements
echo "Installing minio..."
helm install $MINIO_DEPLOYMENT_NAME --namespace default -f minio/values.yaml minio/minio


# install minio coinbase feeder
kubectl apply -f loader/coinbase-worker.yaml

# export ports
echo "Exporting ports..." | tee port_forwarding.log
kubectl port-forward service/$MINIO_DEPLOYMENT_NAME 9000:9000 --namespace default >> port_forwarding.log 2>&1 &
kubectl port-forward service/$MINIO_DEPLOYMENT_NAME-console 9001:9001 --namespace default >> port_forwarding.log 2>&1 &


echo "Adding spark helm chart repo"
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator

echo "Installing spark..."
helm install sparkoperator spark-operator/spark-operator --set image.tag=v1beta2-1.3.0-3.1.1

echo "Adding spark deployment from spark/spark-job..."
kubectl apply -f spark/scheduled-spark-job.yaml
