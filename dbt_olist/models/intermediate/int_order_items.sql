SELECT

    oi.order_id,

    oi.order_item_id,

    oi.product_id,

    p.product_category_name,

    oi.seller_id,

    s.seller_city,

    s.seller_state,

    oi.price,

    oi.freight_value

FROM {{ ref('stg_order_items') }} AS oi

LEFT JOIN {{ ref('stg_products') }} AS p
    ON oi.product_id = p.product_id

LEFT JOIN {{ ref('stg_sellers') }} AS s
    ON oi.seller_id = s.seller_id