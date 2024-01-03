WITH stg_company AS (
    SELECT * FROM {{ ref("stg_company") }}
)

SELECT
    cid AS cid,
    cname AS cname,
    '{{ var("etl_date")}}' AS etl_date,      -- 获取 airflow dag 中的etl_date变量值
    to_char(now(), 'yyyy-mm-dd hh24:mi:ss') AS data_load_time
FROM stg_company
