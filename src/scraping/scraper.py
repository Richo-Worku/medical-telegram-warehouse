from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from dotenv import load_dotenv
import os
from datetime import datetime

# Project modules
from src.scraping.channels import CHANNELS
from src.scraping.image_downloader import get_image_path
from src.storage.data_lake import save_channel_messages
from src.utils.logger import logger

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("medical_session", api_id, api_hash)


# -----------------------------
# Resolve Channel Safely
# -----------------------------
def resolve_channel(channel_name):
    try:
        entity = client.get_entity(channel_name)

        # Optional: force metadata loading
        try:
            client(GetFullChannelRequest(entity))
        except Exception:
            pass

        return entity

    except Exception as e:
        logger.error(f"Failed to resolve channel {channel_name}: {e}")
        return None


# -----------------------------
# Scrape One Channel
# -----------------------------
def scrape_channel(channel_name, limit=200):
    logger.info(f"Scraping started: {channel_name}")

    entity = resolve_channel(channel_name)

    if not entity:
        logger.error(f"Channel not found: {channel_name}")
        return []

    messages = []

    try:
        for msg in client.iter_messages(entity, limit=limit):

            image_path = None

            # Download image if exists
            if msg.photo:
                image_path = get_image_path(channel_name, msg.id)
                client.download_media(msg, file=image_path)

            messages.append({
                "message_id": msg.id,
                "channel_name": channel_name,
                "message_date": msg.date,
                "message_text": msg.text,
                "views": msg.views,
                "forwards": msg.forwards,
                "has_media": msg.media is not None,
                "image_path": image_path,

                # RAW TELEGRAM STRUCTURE (DATA LAKE REQUIREMENT)
                "raw": msg.to_dict()
            })

        logger.info(f"Completed {channel_name} | messages scraped: {len(messages)}")

    except Exception as e:
        logger.error(f"Error scraping {channel_name}: {e}")

    return messages


# -----------------------------
# Scrape All Channels
# -----------------------------
def scrape_all_channels():
    client.start()

    logger.info("🚀 Telegram scraping pipeline started")

    all_data = []
    today = datetime.now().strftime("%Y-%m-%d")

    for channel in CHANNELS:
        logger.info(f"Starting channel: {channel}")

        data = scrape_channel(channel, limit=200)

        # Save Data Lake JSON (raw storage)
        save_channel_messages(today, channel, data)

        all_data.extend(data)

    client.disconnect()

    logger.info(f"🎯 Pipeline finished | Total messages: {len(all_data)}")

    return all_data


# -----------------------------
# Main Entry
# -----------------------------
if __name__ == "__main__":
    scrape_all_channels()