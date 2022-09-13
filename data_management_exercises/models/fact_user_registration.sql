{{ 
    config(
        materialized = 'incremental',
        transient=false
        ) 
}} 

select
    cast({{ dbt_utils.surrogate_key(['username', 'updated_timestamp']) }} as varchar(128)) as event_sk,
    cast(username as varchar(30)) username,
    cast(email_address as varchar(320)) email_address,
    cast(first_name as varchar(100)) first_name,
    cast(last_name as varchar(100)) last_name,
    cast(created_by as varchar(10)) created_by,
    cast(created_timestamp as timestamp) created_timestamp,
    cast(updated_by as varchar(10)) updated_by,
    cast(updated_timestamp as timestamp) updated_timestamp,
    {{ get_audit_columns() }}
from {{ source ('raw_layer', 'raw_user_registration_events') }}

{% if is_incremental() %}

  where cast(load_timestamp as date) = cast(current_date as date)

{% endif %}
