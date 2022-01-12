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