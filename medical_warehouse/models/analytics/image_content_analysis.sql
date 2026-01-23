{{ config(
    materialized='view'
) }}

-- Analysis of YOLO image detections

with image_data as (

    select
        i.message_id,
        i.detected_class,
        i.confidence_score,
        i.image_category,
        m.channel_key,
        m.date_key
    from {{ ref('fct_image_detections') }} i
    join {{ ref('fct_messages') }} m
        on i.message_id = m.message_id

)

select
    image_category,
    count(distinct message_id) as total_images,   -- unique messages with images
    count(*) as total_detections                  -- total detected objects
from image_data
group by image_category
order by total_images desc   -- no semicolon here
