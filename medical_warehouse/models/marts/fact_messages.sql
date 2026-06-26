with stg as (

    select *
    from {{ ref('stg_telegram_messages') }}

)

select
    message_id,
    channel_name,
    message_date,

    views,
    forwards,

    message_length,
    has_image,

    -- 🔥 IMPORTANT ANALYTICS METRICS
    (coalesce(views, 0) + coalesce(forwards, 0)) as engagement_score

from stg