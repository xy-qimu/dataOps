{{
  config(
    materialized='incremental',
    unique_key='customer_id',
    incremental_strategy='merge'
  )
}}

SELECT *
FROM {{ ref("ods_customers") }}
