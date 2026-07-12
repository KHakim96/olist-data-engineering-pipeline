SELECT DISTINCT

    CAST(order_purchase_timestamp AS DATE) AS order_date

FROM {{ ref('stg_orders') }}

WHERE order_purchase_timestamp IS NOT NULL