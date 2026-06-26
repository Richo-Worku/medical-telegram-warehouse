import os

def get_image_path(channel_name, message_id):
    base_dir = "data/raw/images"
    channel_dir = os.path.join(base_dir, channel_name)

    os.makedirs(channel_dir, exist_ok=True)

    return os.path.join(channel_dir, f"{message_id}.jpg")