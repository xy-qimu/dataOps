{{
  config(
    post_hook="{{ drop_tmp_tables(this.schema,this.name) }}",
    materialized='incremental',
    unique_key='customer_id',
    incremental_strategy='merge'
  )
}}

SELECT *
FROM {{ ref("ods_customers") }}
