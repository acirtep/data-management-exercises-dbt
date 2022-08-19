{% macro get_audit_columns() %}
current_timestamp as dbt_inserted_timestamp,
cast('{{ invocation_id }}' as varchar(128)) as dbt_execution_id
{% endmacro %}