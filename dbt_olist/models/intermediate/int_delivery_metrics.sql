SELECT

    order_id,

    order_purchase_timestamp,

    order_delivered_customer_date,

    DATE_DIFF(
        'day',
        order_purchase_timestamp,
        order_delivered_customer_date
    ) AS delivery_days

FROM {{ ref('stg_orders') }}