with base as (

    select *
    from {{ ref('stg_telegram_messages') }}

),

channel_stats as (

    select
        channel_name,

        count(*) as total_posts,
        avg(views) as avg_views,
        min(message_date) as first_post_date,
        max(message_date) as last_post_date

    from base
    group by channel_name

)

select
    row_number() over () as channel_key,   -- surrogate key

    channel_name,

    case 
        when channel_name ilike '%pharma%' then 'Pharmaceutical'
        when channel_name ilike '%cosmetic%' then 'Cosmetics'
        else 'Medical'
    end as channel_type,

    first_post_date,
    last_post_date,
    total_posts,
    avg_views

from channel_stats