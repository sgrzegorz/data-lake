from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import flatten
from pyspark.sql.functions import avg
from minio import Minio
from minio.commonconfig import CopySource
import os

spark = SparkSession.builder.getOrCreate()

SOURCE_BUCKET='raw-data'
TARGET_BUCKET="processed-data"

def load_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.access.key', 'rootuser')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.secret.key', 'rootpass123')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.path.style.access', 'true')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.endpoint', 'http://localhost:9000')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.connection.ssl.enabled', 'false')


load_config(spark.sparkContext)

sc = spark.sparkContext

print("Configuration of spark successfully finished")


minio_service_host = os.getenv("MINIO_SERVICE_HOST")
minio_service_port = os.getenv("MINIO_SERVICE_PORT")
host = f"{minio_service_host}:{minio_service_port}"
# to test locally uncomment following line
# host = f"localhost:9000"
print(f'Data lake source {host}')

access_key = "rootuser"
secret_key = "rootpass123"
client = Minio(host, access_key=access_key, secret_key=secret_key, secure=False)


def process_data(filename):
    df = spark.read.json(f's3a://{SOURCE_BUCKET}/{filename}')
    df = df.select('product_id', 'time', flatten(df.changes).alias('changes'),
                   'type')
    # df = df.withColumn(col(flatten(df.changes).alias('changes')))
    df = df.select('product_id', 'time', df.changes[0], df.changes[1],
                   df.changes[2], 'type')
    df = df.withColumnRenamed('changes[0]', 'action')
    df = df.withColumnRenamed('changes[1]', 'price')
    df = df.withColumnRenamed('changes[2]', 'weight')

    df = df.groupBy("action").agg(avg("price").alias('result avg price'))
    print(filename)
    df.show(10)


objects = client.list_objects(SOURCE_BUCKET)
for obj in objects:
    #     print(obj._object_name)
    process_data(obj._object_name)

    print(f"Copying {obj._object_name} from bucket {SOURCE_BUCKET} to {TARGET_BUCKET}")

    result = client.copy_object(
        TARGET_BUCKET,
        obj._object_name,
        CopySource(SOURCE_BUCKET, obj._object_name),
    )

    print(f"Removing {obj._object_name} from bucket {SOURCE_BUCKET}")
    client.remove_object(SOURCE_BUCKET, obj._object_name)
