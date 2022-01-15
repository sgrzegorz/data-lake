# Data lake project

Requirements:
- running kubernetes cluster (for example minio is sufficient)
- helm installed and configured

To setup cluster:
```
./run.sh
```

To check if cluster is deployed see:
```
helm list
```
```
kubectl get pods
```
```
kubectl get services
```

To uninstall all resources:
```
./uninstall.sh
```

To clear all kubernetes cluster resources:
```
kubectl delete all --all
```

Build dockerfile

For the first time run
`docker login`

```
docker build .  -t sgrzegorz/coinbase
docker push sgrzegorz/coinbase
```

Installing spark operator

```
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm install sparkoperator spark-operator/spark-operator --set image.tag=v1beta2-1.3.0-3.1.1

helm uninstall sparkoperator

```

```
docker build . -t sgrzegorz/sparkjob 
docker push sgrzegorz/sparkjob

```
