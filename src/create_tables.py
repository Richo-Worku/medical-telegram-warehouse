from sqlalchemy import text
from database import engine

create_table_query = """
CREATE TABLE IF NOT EXISTS raw_messages (
    message_id BIGINT,
    channel_name VARCHAR(255),
    message_date TIMESTAMP,
    message_text TEXT,
    has_media BOOLEAN,
    image_path TEXT,
    views INTEGER,
    forwards INTEGER
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query))
    conn.commit()

print("raw_messages table created successfully!")