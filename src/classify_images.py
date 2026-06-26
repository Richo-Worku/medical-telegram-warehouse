import pandas as pd
from pathlib import Path

INPUT_FILE = "data/enriched/yolo_detections.csv"

df = pd.read_csv(INPUT_FILE)

PRODUCT_OBJECTS = {
    "bottle",
    "cup",
    "bowl",
    "box"
}

image_groups = []

for image_path, group in df.groupby("image_path"):

    detected_objects = (
        group["object_name"]
        .dropna()
        .astype(str)
        .str.lower()
        .tolist()
    )

    has_person = "person" in detected_objects

    has_product = any(
        obj in PRODUCT_OBJECTS
        for obj in detected_objects
    )

    if has_person and has_product:
        category = "promotional"

    elif has_product and not has_person:
        category = "product_display"

    elif has_person and not has_product:
        category = "lifestyle"

    else:
        category = "other"

    image_groups.append({
        "message_id": group.iloc[0]["message_id"],
        "channel_name": group.iloc[0]["channel_name"],
        "image_path": image_path,
        "image_category": category
    })

result_df = pd.DataFrame(image_groups)

output_path = "data/enriched/image_classifications.csv"
result_df.to_csv(output_path, index=False)

print(f"Saved classifications to {output_path}")
print(result_df["image_category"].value_counts())