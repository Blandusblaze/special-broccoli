import logging
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, transform, filter, trim, year, sha2, monotonically_increasing_id, broadcast, \
    to_date
from pyspark.sql.types import DateType, IntegerType

spark = SparkSession.builder \
    .appName("ETLPipelineFromCSVToDeltaLake") \
    .getOrCreate()

customer_df = spark.read.option("header", True) \
    .option("inferSchema", True) \
    .csv(r"customers.csv")

subscription_df = spark.read.option("header", True) \
    .option("inferSchema", True) \
    .csv(r"subscriptions.csv")

customer_df = customer_df.withColumn("subscription_date", to_date(col("subscription_date"), "yyyy-MM-dd"))
subscription_df = subscription_df.withColumn("subscription_date", to_date(col("subscription_date"), "yyyy-MM-dd"))


joined_df = subscription_df.join(
    broadcast(customer_df),
    on=["customerid","subscription_date"],
    how="inner"
)

joined_df.write.format("parquet").mode("overwrite").partitionBy("platform").save("./output/data")


joined_schema = joined_df.printSchema()
joined_df.show(5)
print(f"No of Partitions:{joined_df.rdd.getNumPartitions()}")
