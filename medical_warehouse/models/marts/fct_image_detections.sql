{{ config(materialized='table') }}

SELECT
    d.message_id,
    m.channel_key,
    m.date_key,
    d.detected_class,
    d.confidence_score,
    d.image_category
FROM {{ ref('stg_yolo_detections') }} d
JOIN {{ ref('fct_messages') }} m
  ON d.message_id = m.message_id
