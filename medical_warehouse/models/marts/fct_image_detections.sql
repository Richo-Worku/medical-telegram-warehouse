with detections as (

    select *
    from {{ source('raw', 'yolo_detections') }}

),

messages as (

    select *
    from {{ ref('fct_messages') }}

),

channels as (

    select *
    from {{ ref('dim_channels') }}

)

select

    d.message_id,

    c.channel_key,

    m.date_key,

    d.detected_class,

    d.confidence_score,

    d.image_category

from detections d

left join messages m
    on d.message_id = m.message_id

left join channels c
    on m.channel_key = c.channel_key