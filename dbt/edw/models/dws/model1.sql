{{
  config(
    materialized='view'
  )
}}

select * from {{ ref("ods_company")}}