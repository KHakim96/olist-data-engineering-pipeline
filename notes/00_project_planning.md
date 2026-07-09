# Phase 00 — Project Planning

---

# 1. Objective

The objective of this project is to build a complete end-to-end Data Engineering pipeline using the Olist Brazilian E-Commerce dataset.

Instead of analyzing CSV files directly, we will design a production-style pipeline that ingests raw data, stores it in a database, transforms it into an analytics warehouse, models it using dbt, orchestrates everything with Airflow, and visualizes the final business metrics in Looker Studio.

The project is designed to simulate a real-world batch data engineering workflow.

---

# 2. Business Problem

The Olist dataset contains information spread across multiple CSV files.

These files include customers, products, sellers, payments, reviews, orders, and geolocation information.

Business users cannot efficiently analyze multiple raw CSV files because:

* Data is stored in separate files.
* Relationships between datasets are not obvious.
* Raw data is not optimized for analytics.
* Repeating the same cleaning process is inefficient.

Our goal is to automate the entire process so that business-ready datasets are always available.

---

# 3. Dataset Overview

This project uses the following datasets.

| Dataset                               | Description                                        |
| ------------------------------------- | -------------------------------------------------- |
| olist_customers_dataset.csv           | Customer information                               |
| olist_geolocation_dataset.csv         | Customer and seller geolocation                    |
| olist_order_items_dataset.csv         | Products purchased in each order                   |
| olist_order_payments_dataset.csv      | Payment information                                |
| olist_order_reviews_dataset.csv       | Customer review scores and comments                |
| olist_orders_dataset.csv              | Main order lifecycle                               |
| olist_products_dataset.csv            | Product information                                |
| olist_sellers_dataset.csv             | Seller information                                 |
| product_category_name_translation.csv | Portuguese-to-English product category translation |

---

# 4. Project Architecture

```
                         Docker Compose
        ┌────────────────────────────────────────┐
        │                                        │
        │    PostgreSQL           Airflow        │
        │                                        │
        └───────────────┬────────────────────────┘
                        │
                        │ (Airflow orchestrates)
                        ▼
        ┌────────────────────────────────────────┐
        │                                        │
        │ 1. Load CSV → PostgreSQL               │
        │ 2. PostgreSQL → Parquet                │
        │ 3. Parquet → DuckDB                    │
        │ 4. dbt run                             │
        │ 5. dbt test                            │
        └────────────────────────────────────────┘
                        │
                        ▼
                 DuckDB Warehouse
                        │
                        ▼
              dbt Business Marts
                        │
                        ▼
                Looker Studio Dashboard
```

---

# 5. Data Flow

The pipeline follows this sequence.

```
Raw CSV Files
        │
        ▼
PostgreSQL
        │
        ▼
Parquet Files
        │
        ▼
DuckDB
        │
        ▼
dbt
        │
        ▼
Looker Studio
```

---

# 6. Technology Stack

| Technology     | Purpose                          |
| -------------- | -------------------------------- |
| Git            | Version control                  |
| GitHub         | Source code repository           |
| Docker         | Containerization                 |
| Docker Compose | Run multiple services together   |
| PostgreSQL     | Landing database for raw data    |
| Python         | ETL processing                   |
| Parquet        | Columnar storage format          |
| DuckDB         | Analytical data warehouse        |
| dbt            | Data transformation and modeling |
| Apache Airflow | Workflow orchestration           |
| Looker Studio  | Dashboard and reporting          |

---

# 7. Project Folder Structure

The project is organized into dedicated folders so that each component has a single responsibility.

| Folder         | Purpose                       |
| -------------- | ----------------------------- |
| notes          | Project notes for every phase |
| config         | Configuration files           |
| data/raw       | Original CSV datasets         |
| data/processed | Generated Parquet files       |
| warehouse      | DuckDB warehouse              |
| sql            | SQL scripts                   |
| scripts        | Python ETL scripts            |
| dags           | Airflow DAGs                  |
| dbt_olist      | dbt project                   |
| dashboards     | Looker Studio documentation   |
| tests          | Python tests                  |
| docs           | Project documentation         |
| logs           | Pipeline logs                 |

---

# 8. Project Phases

The project will be built in the following order.

| Phase | Description      |
| ----: | ---------------- |
|    00 | Project Planning |
|    01 | Project Setup    |
|    02 | PostgreSQL       |
|    03 | Python ETL       |
|    04 | DuckDB           |
|    05 | dbt              |
|    06 | Airflow          |
|    07 | Looker Studio    |
|    08 | Testing          |
|    09 | Documentation    |

---

# 9. Success Criteria

The project is considered complete when the following objectives have been achieved.

* Docker successfully runs PostgreSQL and Airflow.
* All CSV files are loaded into PostgreSQL.
* PostgreSQL data is exported to Parquet.
* Parquet files are loaded into DuckDB.
* dbt builds staging, intermediate, and mart models successfully.
* Airflow executes the entire pipeline automatically.
* Looker Studio connects to the final business-ready datasets.
* All tests pass successfully.
* Complete project documentation is available.

---

# 10. What We Will Build

By the end of this project, we will have built a complete batch Data Engineering pipeline capable of automatically ingesting raw e-commerce data, transforming it into analytics-ready datasets, and presenting business insights through an interactive dashboard.

The project follows common Data Engineering practices by separating ingestion, storage, transformation, orchestration, testing, and visualization into independent layers.
