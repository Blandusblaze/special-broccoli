import json
import os
from datetime import datetime
from kafka import KafkaConsumer, KafkaProducer
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, broadcast

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'raw.input.events',
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='spark-etl-group'
)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaETLConsumer") \
    .getOrCreate()

# Consume and process messages
for message in consumer:
    data = message.value
    customer_path = data['customer_csv']
    subscription_path = data['subscription_csv']

    # Create timestamped output path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = f"./output/data_{timestamp}"
    os.makedirs(output_path, exist_ok=True)

    # Read CSV files
    customer_df = spark.read.option("header", True).option("inferSchema", True).csv(customer_path)
    subscription_df = spark.read.option("header", True).option("inferSchema", True).csv(subscription_path)

    # Convert subscription_date to date type
    customer_df = customer_df.withColumn("subscription_date", to_date(col("subscription_date"), "yyyy-MM-dd"))
    subscription_df = subscription_df.withColumn("subscription_date", to_date(col("subscription_date"), "yyyy-MM-dd"))

    # Perform broadcast join
    joined_df = subscription_df.join(
        broadcast(customer_df),
        on=["customerid", "subscription_date"],
        how="inner"
    )

    # Write result to partitioned Parquet file
    joined_df.write.mode("overwrite").partitionBy("platform").parquet(output_path)

    # Send result message to Kafka
    result_message = {
        "status": "success",
        "output_path": output_path
    }
    producer.send("data.cleaned", value=result_message)
    producer.flush()
