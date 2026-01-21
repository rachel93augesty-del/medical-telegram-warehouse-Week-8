select message_id, view_count
from {{ ref('fct_messages') }}
where view_count < 0
