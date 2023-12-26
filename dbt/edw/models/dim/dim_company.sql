{{
  config(
    materialized='incremental',
    unique_key='cid',
    incremental_strategy='merge'
  )
}}
select
        cid as cid
        ,'{{ var("etl_date")}}' as cname
        ,to_char(now(),'yyyy-mm-dd hh24:mi:ss')  as DATA_LOAD_TIME
from  {{ ref("ods_company")}}