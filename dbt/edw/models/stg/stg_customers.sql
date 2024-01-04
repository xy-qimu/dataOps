-- Example of a pre-hook to truncate a staging table
{{ config(
  pre_hook="TRUNCATE TABLE {{ this }}"
) }}

WITH source AS (

    {#-
    Normally we would select from the table here, but we are using seeds to load
    our data in this project
    #}
    SELECT * FROM {{ ref('raw_customers') }}

),

renamed AS (

    SELECT
        id AS customer_id,
        first_name,
        last_name

    FROM source

)

SELECT * FROM renamed
