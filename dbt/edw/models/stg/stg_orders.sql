{{ config(
  post_hook="select now()"
) }}


WITH source AS (

    {#-
    Normally we would select from the table here, but we are using seeds to load
    our data in this project
    #}
    SELECT * FROM {{ source('pos','raw_orders') }}

),

renamed AS (

    SELECT
        id AS order_id,
        user_id AS customer_id,
        order_date::varchar,
        status

    FROM source

)

SELECT * FROM renamed
