from pyspark import SparkContext
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

def load_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguaration().set('fs.s3a.access.key','rootuser')
    spark_context._jsc.hadoopConfiguaration().set('fs.s3a.secret.key','rootpass123')
    spark_context._jsc.hadoopConfiguaration().set('fs.s3a.path.style.access','true')
    spark_context._jsc.hadoopConfiguaration().set('fs.s3a.impl','org.apache.hadoop.fs.s3a.S3AFileSystem')
    spark_context._jsc.hadoopConfiguaration().set('fs.s3a.endpoint','http://minio:9000')
    spark_context._jsc.hadoopConfiguaration().set('fs.s3a.connection.ssl.enabled','false')

load_config(spark.sparkContext)

print("Configuration of spark successfully finished")

dataframe = spark.read.json('s3a://orders/*')

average = dataframe.agg({'amount' : 'avg'})


average.show()