SELECT

    order_id,

    review_score,

    review_creation_date

FROM {{ ref('stg_order_reviews') }}