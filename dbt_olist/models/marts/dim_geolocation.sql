SELECT DISTINCT

    geolocation_zip_code_prefix,

    geolocation_city,

    geolocation_state,

    geolocation_lat,

    geolocation_lng

FROM {{ ref('stg_geolocation') }}