SELECT

    COUNT(DISTINCT fo.order_id) AS total_orders,

    COUNT(DISTINCT dc.customer_id) AS total_customers,

    SUM(fp.total_payment) AS total_revenue,

    AVG(fp.total_payment) AS average_order_value

FROM {{ ref('fact_orders') }} AS fo

LEFT JOIN {{ ref('dim_customer') }} AS dc

    ON fo.customer_id = dc.customer_id

LEFT JOIN {{ ref('fact_payments') }} AS fp

    ON fo.order_id = fp.order_id