-- =========================================================
-- Project  : Olist Data Engineering Pipeline
-- File     : create_olist_tables.sql
-- Database : PostgreSQL
--
-- Purpose:
-- Create the raw PostgreSQL schema for the Olist dataset.
--
-- Notes:
-- - Raw ingestion layer.
-- - Source data is preserved as closely as possible.
-- - Data cleansing and modelling are handled later using dbt.
-- =========================================================



-- =========================================================
-- Drop Existing Tables
-- =========================================================

DROP TABLE IF EXISTS order_reviews CASCADE;
DROP TABLE IF EXISTS order_payments CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS geolocation CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS sellers CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS category_translation CASCADE;



-- =========================================================
-- Lookup Tables
-- =========================================================

CREATE TABLE category_translation (

    product_category_name           VARCHAR(100) PRIMARY KEY,
    product_category_name_english   VARCHAR(100) NOT NULL

);



CREATE TABLE geolocation (

    geolocation_zip_code_prefix     INTEGER NOT NULL,
    geolocation_lat                 DOUBLE PRECISION NOT NULL,
    geolocation_lng                 DOUBLE PRECISION NOT NULL,
    geolocation_city                VARCHAR(100) NOT NULL,
    geolocation_state               CHAR(2) NOT NULL

);

-- =========================================================
-- Master Tables
-- =========================================================

CREATE TABLE customers (

    customer_id                 VARCHAR(32) PRIMARY KEY,
    customer_unique_id          VARCHAR(32) NOT NULL,
    customer_zip_code_prefix    INTEGER NOT NULL,
    customer_city               VARCHAR(100) NOT NULL,
    customer_state              CHAR(2) NOT NULL

);



CREATE TABLE sellers (

    seller_id                   VARCHAR(32) PRIMARY KEY,
    seller_zip_code_prefix      INTEGER NOT NULL,
    seller_city                 VARCHAR(100) NOT NULL,
    seller_state                CHAR(2) NOT NULL

);



CREATE TABLE products (

    product_id                  VARCHAR(32) PRIMARY KEY,
    product_category_name       VARCHAR(100),
    product_name_lenght         INTEGER,
    product_description_lenght  INTEGER,
    product_photos_qty          INTEGER,
    product_weight_g            INTEGER,
    product_length_cm           INTEGER,
    product_height_cm           INTEGER,
    product_width_cm            INTEGER

);

-- =========================================================
-- Transaction Tables
-- =========================================================

CREATE TABLE orders (

    order_id                            VARCHAR(32) PRIMARY KEY,
    customer_id                         VARCHAR(32) NOT NULL,
    order_status                        VARCHAR(20) NOT NULL,
    order_purchase_timestamp            TIMESTAMP NOT NULL,
    order_approved_at                   TIMESTAMP,
    order_delivered_carrier_date        TIMESTAMP,
    order_delivered_customer_date       TIMESTAMP,
    order_estimated_delivery_date       TIMESTAMP NOT NULL,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)

);



CREATE TABLE order_items (

    order_id                    VARCHAR(32) NOT NULL,
    order_item_id               INTEGER NOT NULL,
    product_id                  VARCHAR(32) NOT NULL,
    seller_id                   VARCHAR(32) NOT NULL,
    shipping_limit_date         TIMESTAMP NOT NULL,
    price                       NUMERIC(10,2) NOT NULL,
    freight_value               NUMERIC(10,2) NOT NULL,

    CONSTRAINT pk_order_items
        PRIMARY KEY (order_id, order_item_id),

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_order_items_seller
        FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id)

);



CREATE TABLE order_payments (

    order_id                    VARCHAR(32) NOT NULL,
    payment_sequential          INTEGER NOT NULL,
    payment_type                VARCHAR(20) NOT NULL,
    payment_installments        INTEGER NOT NULL,
    payment_value               NUMERIC(10,2) NOT NULL,

    CONSTRAINT pk_order_payments
        PRIMARY KEY (order_id, payment_sequential),

    CONSTRAINT fk_payment_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)

);



CREATE TABLE order_reviews (

    review_id                   VARCHAR(32) NOT NULL,
    order_id                    VARCHAR(32) NOT NULL,
    review_score                INTEGER NOT NULL,
    review_comment_title        VARCHAR(100),
    review_comment_message      TEXT,
    review_creation_date        TIMESTAMP NOT NULL,
    review_answer_timestamp     TIMESTAMP NOT NULL,

    CONSTRAINT pk_order_reviews
        PRIMARY KEY (review_id, order_id),

    CONSTRAINT fk_review_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)

);

-- =========================================================
-- Verification Queries
-- =========================================================

-- Check row counts after data ingestion

SELECT COUNT(*) AS customers_count
FROM customers;

SELECT COUNT(*) AS sellers_count
FROM sellers;

SELECT COUNT(*) AS products_count
FROM products;

SELECT COUNT(*) AS category_translation_count
FROM category_translation;

SELECT COUNT(*) AS geolocation_count
FROM geolocation;

SELECT COUNT(*) AS orders_count
FROM orders;

SELECT COUNT(*) AS order_items_count
FROM order_items;

SELECT COUNT(*) AS order_payments_count
FROM order_payments;

SELECT COUNT(*) AS order_reviews_count
FROM order_reviews;

-- =========================================================
-- Expected Row Counts (Raw Dataset)
-- =========================================================

-- customers              : 99,441
-- sellers                : 3,095
-- products               : 32,951
-- category_translation   : 71
-- geolocation            : 1,000,163
-- orders                 : 99,441
-- order_items            : 112,650
-- order_payments         : 103,886
-- order_reviews          : 100,000