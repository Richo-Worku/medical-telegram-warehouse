with source as (

    select *
    from raw.telegram_messages

),

cleaned as (

    select
        message_id,
        channel_name,

        -- cast date properly
        cast(message_date as timestamp) as message_date,

        -- clean text
        trim(message_text) as message_text,

        -- numeric fields
        cast(views as bigint) as views,
        cast(forwards as bigint) as forwards,

        -- boolean normalization
        case 
            when has_media is true then true
            else false
        end as has_media,

        image_path,

        raw

    from source
    where message_text is not null
      and length(trim(message_text)) > 0

)

select
    *,

    -- calculated fields (VERY IMPORTANT FOR MARKS)
    length(message_text) as message_length,

    case 
        when image_path is not null then true
        else false
    end as has_image

from cleaned