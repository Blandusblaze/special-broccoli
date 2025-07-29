from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v:json.dumps(v).encode("utf-8")
)

message = {
    "customer_csv":"customers.csv",
    "subscription_csv":"subscriptions.csv"
}

producer.send("raw.input.events",message)
producer.flush()
print("CSV Paths send to Kafka Topic 'raw.input.events' ")