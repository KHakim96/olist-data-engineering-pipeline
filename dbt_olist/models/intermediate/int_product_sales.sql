SELECT

    product_id,

    COUNT(*) AS total_items_sold,

    SUM(price) AS total_sales,

    AVG(price) AS average_price

FROM {{ ref('stg_order_items') }}

GROUP BY product_id