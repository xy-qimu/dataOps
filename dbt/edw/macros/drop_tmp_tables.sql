{% macro drop_tmp_tables(schema_name,tbl_name) -%}
   {%- set table_name = schema_name + '.' + tbl_name + '__dbt_tmp' -%}
   DROP TABLE IF EXISTS {{ table_name }}
{%- endmacro %}