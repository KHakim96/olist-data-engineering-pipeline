# Data Dictionary

## Overview

This document describes the datasets used throughout the Olist Data Engineering Pipeline.

The data originates from the Brazilian Olist E-Commerce public dataset and is processed through multiple stages:

- Raw CSV Files
- PostgreSQL
- Parquet Data Lake
- DuckDB Warehouse
- dbt Analytics Marts

---

# Dataset Summary

| Table | Description | Primary Key | Rows |
|--------|-------------|-------------|------:|
| category_translation | Portuguese to English product category mapping | product_category_name | 71 |
| customers | Customer master data | customer_id | 99,441 |
| sellers | Seller master data | seller_id | 3,095 |
| products | Product catalogue | product_id | 32,951 |
| geolocation | Brazilian postal code geolocation | None | 1,000,163 |
| orders | Customer orders | order_id | 99,441 |
| order_items | Individual order line items | *(order_id, order_item_id)* | 112,650 |
| order_payments | Payment transactions | *(order_id, payment_sequential)* | 103,886 |
| order_reviews | Customer reviews | review_id | 100,000 |

---

# Table Details

## category_translation

Maps Portuguese product category names to English.

### Columns

| Column | Description |
|---------|-------------|
| product_category_name | Original Portuguese category |
| product_category_name_english | English translation |

---

## customers

Contains customer information.

### Columns

| Column | Description |
|---------|-------------|
| customer_id | Primary key |
| customer_unique_id | Unique customer identifier |
| customer_zip_code_prefix | Postal code |
| customer_city | Customer city |
| customer_state | Brazilian state |

---

## sellers

Contains seller information.

### Columns

| Column | Description |
|---------|-------------|
| seller_id | Primary key |
| seller_zip_code_prefix | Postal code |
| seller_city | Seller city |
| seller_state | Brazilian state |

---

## products

Contains product catalogue information.

### Columns

| Column | Description |
|---------|-------------|
| product_id | Primary key |
| product_category_name | Product category |
| product_name_length | Product name length |
| product_description_length | Description length |
| product_photos_qty | Number of photos |
| product_weight_g | Product weight |
| product_length_cm | Length |
| product_height_cm | Height |
| product_width_cm | Width |

---

## geolocation

Brazilian ZIP code geolocation reference.

### Columns

| Column | Description |
|---------|-------------|
| geolocation_zip_code_prefix | Postal code |
| geolocation_lat | Latitude |
| geolocation_lng | Longitude |
| geolocation_city | City |
| geolocation_state | State |

---

## orders

Customer order information.

### Columns

| Column | Description |
|---------|-------------|
| order_id | Primary key |
| customer_id | Customer reference |
| order_status | Order status |
| order_purchase_timestamp | Purchase timestamp |
| order_approved_at | Approval timestamp |
| order_delivered_carrier_date | Carrier dispatch |
| order_delivered_customer_date | Customer delivery |
| order_estimated_delivery_date | Estimated delivery |

---

## order_items

Individual items purchased in each order.

### Columns

| Column | Description |
|---------|-------------|
| order_id | Order reference |
| order_item_id | Line item number |
| product_id | Product reference |
| seller_id | Seller reference |
| shipping_limit_date | Shipping deadline |
| price | Item price |
| freight_value | Shipping cost |

---

## order_payments

Payment information.

### Columns

| Column | Description |
|---------|-------------|
| order_id | Order reference |
| payment_sequential | Payment sequence |
| payment_type | Payment method |
| payment_installments | Number of installments |
| payment_value | Payment amount |

---

## order_reviews

Customer review information.

### Columns

| Column | Description |
|---------|-------------|
| review_id | Primary key |
| order_id | Order reference |
| review_score | Rating (1–5) |
| review_comment_title | Review title |
| review_comment_message | Review message |
| review_creation_date | Review date |
| review_answer_timestamp | Response timestamp |

---

# Relationships

```
customers
      │
      ▼
orders
      │
      ▼
order_items
      ├──────────► products
      │
      └──────────► sellers

orders
      ├──────────► order_payments
      └──────────► order_reviews
```

---

# Data Quality

The datasets were validated before ingestion using automated checks.

Validation included:

- Dataset availability
- Required columns
- Duplicate detection
- Primary key validation
- Foreign key validation
- NULL value inspection
- Referential integrity verification

All validation reports are available under:

```
docs/
```