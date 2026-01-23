select
    m.message_id,
    m.channel_key,
    m.date_key,
    y.detected_class,
    y.confidence_score,
    y.image_category,
    y.image_file   -- <- make sure this column exists
from {{ ref('stg_telegram_messages') }} m
join {{ ref('yolo_detections') }} y
    on m.message_id = y.message_id
