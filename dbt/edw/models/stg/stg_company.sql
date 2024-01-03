-- Example of a pre-hook to truncate a staging table
{{ config(
  pre_hook="TRUNCATE TABLE {{ this }}"
) }}

SELECT
    1 AS cid,
    'a company' AS cname
UNION
SELECT
    2 AS cid,
    'b company' AS cname
UNION
SELECT
    3 AS cid,
    'c company' AS cname
