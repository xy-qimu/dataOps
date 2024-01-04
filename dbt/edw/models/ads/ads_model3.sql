-- Example of a pre-hook to truncate a staging table
{{ config(
  pre_hook="TRUNCATE TABLE {{ this }}"
) }}

SELECT * FROM {{ ref("ods_customers")}}
