-- assert_positive_views.sql

select *
from {{ ref('stg_telegram_messages') }}
where views < 0