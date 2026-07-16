# Phase 07 — Analytics Dashboard

## Objective

Build a modern Business Intelligence application on top of the curated DuckDB warehouse.

The dashboard serves as the presentation layer of the data platform, allowing business users to explore operational and commercial insights through interactive visualizations.

---

# Architecture Position

```
Raw CSV
    │
    ▼
PostgreSQL
    │
    ▼
Parquet Data Lake
    │
    ▼
DuckDB Warehouse
    │
    ▼
dbt Transformations
    │
    ▼
Analytics Marts
    │
    ▼
Streamlit Dashboard
```

The dashboard consumes only curated warehouse tables produced by dbt.

No visualizations query raw datasets directly.

---

# Technologies Used

- Streamlit
- Plotly Express
- DuckDB
- Python
- SQL

---

# Dashboard Design Principles

The application was designed following modern BI dashboard practices.

Design goals:

- Clean enterprise layout
- Dark theme
- Responsive design
- Executive-friendly KPIs
- Consistent styling across all pages
- Reusable utility functions
- Interactive Plotly visualizations

Common layout:

- Header
- KPI Cards
- Trend Analysis
- Breakdown Charts
- Supporting Visualizations

---

# Shared Components

A common utility module was created.

utils.py

Contains:

- DuckDB connection
- SQL execution helper
- Shared CSS loader

All dashboards reuse these utilities.

---

# Dashboard Pages

## 1. Home

Purpose

Landing page introducing the project.

Contents

- Project overview
- Technology stack
- Architecture summary
- Dashboard navigation

---

## 2. Executive Dashboard

Purpose

Provide a high-level overview of business performance.

KPIs

- Total Revenue
- Total Orders
- Unique Customers
- Average Order Value

Charts

- Monthly Revenue Trend
- Business Highlights
- Top Product Categories
- Revenue by State

Business Value

Allows management to understand overall business health.

---

## 3. Sales Dashboard

Purpose

Analyze commercial performance.

KPIs

- Revenue
- Orders
- Average Order Value
- Delivered Orders

Charts

- Monthly Revenue
- Revenue by Category
- Revenue by Payment Method
- Daily Sales Trend
- Revenue by State
- Orders by Status

Business Value

Provides insight into sales performance, payment behavior and order fulfillment.

---

## 4. Customers Dashboard

Purpose

Understand customer distribution and purchasing behavior.

KPIs

- Customers
- States
- Cities
- Average Orders per Customer

Charts

- Monthly Customer Growth
- Orders per Customer
- Customers by State
- Top Customer Cities

Business Value

Supports customer segmentation and regional analysis.

---

## 5. Products Dashboard

Purpose

Measure product and catalog performance.

KPIs

- Products
- Average Price
- Average Freight
- Categories

Charts

- Revenue by Category
- Top Selling Products
- Price Distribution
- Freight Distribution
- Product Weight Distribution

Business Value

Provides insight into pricing strategy and product portfolio.

---

## 6. Delivery Dashboard

Purpose

Analyze operational logistics performance.

KPIs

- Delivered Orders
- Average Delivery Days
- Average Shipping Days
- On-Time Delivery Rate

Charts

- Monthly Delivery Trend
- Delivery Status
- Delivery Delay Distribution

Supporting dbt Model

int_delivery_metrics

Metrics

- delivery_days
- shipping_days
- delay_days
- delivery_status

Business Value

Measures logistics efficiency and customer fulfillment performance.

---

## 7. Reviews Dashboard

Purpose

Analyze customer satisfaction.

KPIs

- Total Reviews
- Average Rating
- Five-Star Reviews
- One-Star Reviews

Charts

- Rating Distribution
- Monthly Review Trend
- Delivery Days vs Rating
- Average Rating by State

Business Value

Demonstrates the relationship between operational performance and customer satisfaction.

---

## 8. Geography Dashboard

Purpose

Analyze regional business performance.

KPIs

- States
- Cities
- Customers
- Sellers

Visualizations

- Interactive Brazil Revenue Choropleth Map
- Customers by State
- Sellers by State
- Top Customer Cities
- Top Seller Cities

Map

The dashboard uses a Brazil GeoJSON file to render an interactive choropleth map.

Hover Information

- Revenue
- Orders
- Customers
- Average Rating

Business Value

Provides geographic insight into commercial performance across Brazil.

---

# Interactive Features

Implemented

- Hover tooltips
- Zoomable charts
- Responsive layout
- Dynamic SQL queries
- Interactive choropleth map
- KPI cards
- Plotly visualizations

---

# Styling

Common theme

Dark enterprise dashboard

Consistent

- Typography
- Colors
- KPI cards
- Containers
- Margins
- Chart sizes
- Sidebar
- Icons

---

# Data Sources

Dashboard queries consume curated warehouse tables.

Examples

Fact Tables

- fact_orders
- fact_order_items
- fact_payments
- fact_reviews

Dimension Tables

- dim_customer
- dim_product
- dim_seller
- dim_date
- dim_geolocation

Intermediate Models

- int_delivery_metrics
- int_customer_orders
- int_product_sales
- int_review_metrics

Mart

- executive_dashboard

---

# Key Improvements During Development

Implemented

✓ Unified dashboard theme

✓ Shared utility functions

✓ Consistent KPI card design

✓ Responsive Plotly layouts

✓ Enterprise page structure

✓ Delivery analytics model

✓ Geography dashboard with Brazil choropleth map

✓ Interactive dashboard navigation

✓ Professional business-focused visualizations

---

# Folder Structure

dashboard/

```
dashboard/

├── Home.py

├── utils.py

├── styles.py

├── assets/
│   └── brazil_states.geojson

└── pages/

    ├── 1_Executive.py

    ├── 2_Sales.py

    ├── 3_Customers.py

    ├── 4_Products.py

    ├── 5_Delivery.py

    ├── 6_Reviews.py

    └── 7_Geography.py
```

---

# Deliverables

Completed

- Enterprise Streamlit application
- Eight dashboard pages
- Shared styling
- Shared utilities
- Interactive visualizations
- Business KPI monitoring
- Geographic analytics
- Customer analytics
- Sales analytics
- Operational analytics

---

# Outcome

Phase 07 successfully delivered a complete Business Intelligence application built on top of the modern data engineering pipeline.

The dashboard demonstrates how raw transactional data can be transformed into executive-level insights through PostgreSQL, Parquet, DuckDB, dbt, Apache Airflow and Streamlit.

The completed analytics layer serves as the final presentation tier of the platform and provides an interactive interface for exploring business performance across sales, customers, products, logistics, customer reviews and geographic regions.