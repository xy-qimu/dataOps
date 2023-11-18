{{
  config(
    materialized='incremental',
    unique_key='cid',
    incremental_strategy='merge'
  )
}}

select  cid,'{{ var("etl_date")}}' as cname from {{ ref('stg_company')}}