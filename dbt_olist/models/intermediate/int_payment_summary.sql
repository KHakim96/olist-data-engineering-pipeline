SELECT

    order_id,

    COUNT(*) AS payment_count,

    SUM(payment_value) AS total_payment,

    MAX(payment_installments) AS max_installments

FROM {{ ref('stg_order_payments') }}

GROUP BY order_id