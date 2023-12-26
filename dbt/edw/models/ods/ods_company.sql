select
        cid as cid
        , cname as cname
        ,'{{ var("etl_date")}}' as etl_date      -- 获取 airflow dag 中的etl_date变量值
        , to_char(now(),'yyyy-mm-dd hh24:mi:ss')  as DATA_LOAD_TIME
from   {{ ref("stg_company") }}