with raw_messages as (
    select
        message_id,
        channel_name,
        date::timestamp as message_date,
        text_content,
        views::int as view_count,
        forwards::int as forward_count,
        has_image::boolean
    from raw.telegram_messages
    where message_id is not null
      and text_content is not null
)

select
    message_id,
    channel_name,
    message_date,
    text_content,
    view_count,
    forward_count,
    has_image,
    length(text_content) as message_length
from raw_messages
