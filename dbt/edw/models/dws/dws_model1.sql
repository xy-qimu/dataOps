{{
  config(
    materialized='view'
  )
}}

SELECT *
FROM {{ ref("ods_customers") }}
