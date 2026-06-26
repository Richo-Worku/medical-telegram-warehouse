import os
import json

BASE_PATH = "data/raw/telegram_messages"


def save_channel_messages(date, channel_name, messages):
    folder_path = os.path.join(BASE_PATH, date, channel_name)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"{channel_name}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2, default=str)

    return file_path