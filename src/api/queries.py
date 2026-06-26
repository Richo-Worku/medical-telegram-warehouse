# src/api/queries.py


# -------------------------
# 1. TOP PRODUCTS
# -------------------------
def get_top_products(limit=10):
    return f"""
    SELECT
        word AS product,
        COUNT(*) AS mentions
    FROM (
        SELECT
            LOWER(REGEXP_SPLIT_TO_TABLE(message_text, '\\s+')) AS word
        FROM raw.fct_messages
        WHERE message_text IS NOT NULL
    ) t
    WHERE LENGTH(word) > 3
    GROUP BY word
    ORDER BY mentions DESC
    LIMIT {limit};
    """


# -------------------------
# 2. CHANNEL ACTIVITY (FIXED)
#    - NO message_date column (you only have date_key)
#    - return date as TEXT to avoid Pydantic issues
# -------------------------
def get_channel_activity(channel_name):
    return f"""
    SELECT
        c.channel_name,
        TO_CHAR(d.full_date, 'YYYY-MM-DD') AS date,
        COUNT(m.message_id) AS total_messages,
        ROUND(AVG(m.views), 2) AS avg_views,
        COALESCE(SUM(m.forwards), 0) AS total_forwards
    FROM raw.fct_messages m
    JOIN raw.dim_channels c
        ON m.channel_key = c.channel_key
    JOIN raw.dim_dates d
        ON m.date_key = d.date_key
    WHERE c.channel_name = '{channel_name}'
    GROUP BY c.channel_name, d.full_date
    ORDER BY d.full_date;
    """


# -------------------------
# 3. MESSAGE SEARCH
# -------------------------
def search_messages(query, limit=20):
    return f"""
    SELECT
        m.message_id,
        c.channel_name,
        TO_CHAR(d.full_date, 'YYYY-MM-DD') AS date,
        m.message_text,
        m.views,
        m.forwards
    FROM raw.fct_messages m
    JOIN raw.dim_channels c
        ON m.channel_key = c.channel_key
    JOIN raw.dim_dates d
        ON m.date_key = d.date_key
    WHERE LOWER(m.message_text) LIKE LOWER('%{query}%')
    ORDER BY m.views DESC
    LIMIT {limit};
    """


# -------------------------
# 4. VISUAL CONTENT STATS
# -------------------------
def get_visual_content_stats():
    return """
    SELECT
        c.channel_name,

        COUNT(*) AS total_images,

        COUNT(CASE WHEN d.image_category = 'promotional' THEN 1 END) AS promotional_images,
        COUNT(CASE WHEN d.image_category = 'product_display' THEN 1 END) AS product_display_images,
        COUNT(CASE WHEN d.image_category = 'lifestyle' THEN 1 END) AS lifestyle_images,
        COUNT(CASE WHEN d.image_category = 'other' THEN 1 END) AS other_images

    FROM raw.fct_image_detections d
    JOIN raw.fct_messages m
        ON d.message_id = m.message_id
    JOIN raw.dim_channels c
        ON m.channel_key = c.channel_key
    GROUP BY c.channel_name
    ORDER BY total_images DESC;
    """