import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ----------------------------
# LOAD ENV VARIABLES
# ----------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# DEBUG (safe to remove later)
print("DB_HOST:", DB_HOST)
print("DB_USER:", DB_USER)

# ----------------------------
# BUILD DB CONNECTION STRING
# ----------------------------
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("Connecting to PostgreSQL...")

engine = create_engine(DB_URL)


# ----------------------------
# DATA LAKE PATH
# ----------------------------
BASE_PATH = "data/raw/telegram_messages"


def get_latest_folder():
    folders = sorted(os.listdir(BASE_PATH))
    if not folders:
        raise Exception("No data lake folders found")

    return os.path.join(BASE_PATH, folders[-1])


# ----------------------------
# LOAD JSON FILES
# ----------------------------
def load_json_files():
    latest_folder = get_latest_folder()
    records = []

    for channel in os.listdir(latest_folder):
        file_path = os.path.join(latest_folder, channel, f"{channel}.json")

        if not os.path.exists(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            for msg in data:
                records.append({
                    "message_id": msg.get("message_id"),
                    "channel_name": msg.get("channel_name"),
                    "message_date": msg.get("message_date"),
                    "message_text": msg.get("message_text"),
                    "views": msg.get("views"),
                    "forwards": msg.get("forwards"),
                    "has_media": msg.get("has_media"),
                    "image_path": msg.get("image_path"),
                    "raw": json.dumps(msg)   # ✅ FIXED (safe JSONB)
                })

    return records


# ----------------------------
# INSERT INTO POSTGRES
# ----------------------------
def insert_to_postgres(records):
    query = """
    INSERT INTO raw.telegram_messages (
        message_id,
        channel_name,
        message_date,
        message_text,
        views,
        forwards,
        has_media,
        image_path,
        raw
    )
    VALUES (
        :message_id,
        :channel_name,
        :message_date,
        :message_text,
        :views,
        :forwards,
        :has_media,
        :image_path,
        CAST(:raw AS JSONB)
    )
    ON CONFLICT (message_id, channel_name) DO NOTHING;
    """

    with engine.begin() as conn:
        conn.execute(text(query), records)


# ----------------------------
# MAIN PIPELINE
# ----------------------------
if __name__ == "__main__":
    print("Loading JSON data from Data Lake...")

    records = load_json_files()

    print(f"Found {len(records)} records")

    print("Inserting into PostgreSQL raw table...")

    insert_to_postgres(records)

    print("✔ Load complete")