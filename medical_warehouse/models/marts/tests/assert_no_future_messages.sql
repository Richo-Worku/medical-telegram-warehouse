-- assert_no_future_messages.sql

select *
from {{ ref('stg_telegram_messages') }}
where message_date > now()