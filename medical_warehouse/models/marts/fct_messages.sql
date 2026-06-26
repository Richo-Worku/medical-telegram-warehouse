with messages as (

    select *
    from {{ ref('stg_telegram_messages') }}

),

channels as (

    select *
    from {{ ref('dim_channels') }}

),

dates as (

    select *
    from {{ ref('dim_dates') }}

)

select
    m.message_id,
    c.channel_key,
    d.date_key,

    m.message_text,
    m.message_length,

    -- FIX: handle missing values safely
    coalesce(m.views, 0) as views,
    coalesce(m.forwards, 0) as forwards,

    m.has_image

from messages m

left join channels c
    on m.channel_name = c.channel_name

left join dates d
    on cast(m.message_date as date) = d.full_date