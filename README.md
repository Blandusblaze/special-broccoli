# 🥦 Special Broccoli: A Streaming-First Mini Data Engineering Pipeline

This project is a streaming-first mini data engineering pipeline built using **Apache Kafka**, **PySpark**, and **Parquet** — a twisted but functional combo I call **Special Broccoli**.

## 🔍 Project Overview

The goal is to simulate a realistic, modular pipeline to process data from raw events, transform it using Spark, and save it efficiently using partitioned Parquet files.

### 🧱 Components Used

- **Kafka** for publishing and subscribing to streaming events.
- **PySpark** for consuming, transforming, and processing those events.
- **Parquet** for storing transformed data efficiently, partitioned by platform.

## 🧾 Dataset Info

The data consists of **customer records subscribed to various streaming platforms**, along with an estimate of their **churn probability**.

### Sample fields:

- `customer_id`
- `platform` (e.g., Netflix, Prime, Hulu, etc.)
- `churn_probability`
- `subscription_date`
- `region`

## 🛠️ Pipeline Stages

1. **Kafka Topics Setup** — using Docker Compose to start Kafka and create necessary topics.
2. **Producer** — pushes `raw.input.events` into Kafka simulating customer data.
3. **Spark Consumer** — reads from Kafka, joins with a reference dataset, transforms it.
4. **Output** — Writes final transformed data to **Parquet**, partitioned by `platform`.

## 📦 Output

Final dataset is saved in `parquet/` folder like:

```bash
parquet/platform=Netflix/part-*.parquet
parquet/platform=Prime/part-*.parquet
...
```

## 🚀 Try it Out

Clone and run this project:

```bash
git clone https://github.com/Blandusblaze/special-broccoli.git
cd special-broccoli
# Follow instructions in the repo to bring up services and run jobs
```

## 🔗 GitHub Repo

👉 [https://github.com/Blandusblaze/special-broccoli](https://github.com/Blandusblaze/special-broccoli)

## 📢 LinkedIn Post Snippet

> This weekend, I experimented with a streaming-first mini data engineering pipeline combining Apache Kafka, PySpark, and Parquet. I call it **Special Broccoli** — a balanced mix of tools that just works! 🥦✨
>
> The dataset is based on customer subscriptions across streaming platforms, including churn probability, and is saved as partitioned Parquet files. A twisted but solid pipeline built with clean joins and transformations.
>
> Check it out on GitHub ⬇️

## 📌 Hashtags

```
#DataEngineering #ApacheKafka #PySpark #Parquet #StreamingData #OpenSource #KafkaPipeline #WeekendProject
```

---

Built with ❤️ by [Bharath Kuppusamy](https://www.linkedin.com/in/bharathkuppusamy)