SELECT DISTINCT

    customer_id,

    customer_unique_id,

    customer_city,

    customer_state

FROM {{ ref('int_customer_orders') }}