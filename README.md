# Data lake project

Requirements:
- running kubernetes cluster (for example minio is sufficient)
- helm installed and configured

To setup cluster:
```
./install.sh
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



Building spark locally, for spark version `3.2.0` installed in /opt/spark

```
sudo curl -H "Accept: application/zip" https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar -o /opt/spark/jars/hadoop-aws-3.3.1.jar
sudo curl -H "Accept: application/zip" https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar -o /opt/spark/jars/aws-java-sdk-bundle-1.11.901.jar
cd /opt/spark
./bin/docker-image-tool.sh -r spark-base -t 1.0.0 -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
```

```
cd $project/spark
docker build . -t sgrzegorz/sparkjob 
docker push sgrzegorz/sparkjob
```

Testing spark locally
 
```
# Change "http://minio:9000" to "http://localhost:9000" in main.py
pip install requirements.txt
spark-submit main.py

```

Configure Google Cluster

```
glcloud init
gcloud container clusters get-credentials CLUSTER_NAME

```

Minimal required resources
```
3 CPU
4GB memory 
10 GB storage
```
