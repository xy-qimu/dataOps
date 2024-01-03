{{
  config(
    materialized='view'
  )
}}

SELECT
    cid AS cid,
    cname AS cname
FROM {{ ref("ods_company") }}
