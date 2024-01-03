{{
  config(
    materialized='incremental',
    unique_key='cid',
    incremental_strategy='merge'
  )
}}
SELECT
    cid AS cid,
    to_char(now(), 'yyyy-mm-dd hh24:mi:ss') AS data_load_time
FROM {{ ref("ods_company")}}
