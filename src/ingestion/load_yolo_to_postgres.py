import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_URL)

# YOLO detections
detections = pd.read_csv("data/enriched/yolo_detections.csv")

# Image classifications
classifications = pd.read_csv("data/enriched/image_classifications.csv")

# Join classifications onto detections
final_df = detections.merge(
    classifications[
        ["message_id", "image_category"]
    ],
    on="message_id",
    how="left"
)

final_df.rename(
    columns={
        "object_name": "detected_class"
    },
    inplace=True
)

final_df.to_sql(
    "yolo_detections",
    engine,
    schema="raw",
    if_exists="append",
    index=False
)

print(f"Loaded {len(final_df)} YOLO records")