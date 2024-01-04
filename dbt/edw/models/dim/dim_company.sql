{{
  config(
    materialized='incremental',
    unique_key='cid',
    incremental_strategy='merge'
  )
}}

SELECT *
FROM {{ ref("ods_customers") }}
