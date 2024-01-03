-- tests/stg_company_test.sql

--
WITH test_data AS (
    SELECT
        count(*) AS total_num,
        count(DISTINCT cid) AS primary_num
    FROM {{ref("stg_company")}}
)

-- 实际测试逻辑
SELECT
    'stg_company_test' AS test_name,
    CASE
        WHEN total_num = primary_num THEN 'pass'  -- 检查结果是否符合预期
        ELSE 'fail'
    END AS status
FROM test_data
WHERE total_num != primary_num
