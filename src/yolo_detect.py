from ultralytics import YOLO
from pathlib import Path
import pandas as pd

# Load YOLO model
model = YOLO("yolov8n.pt")

IMAGE_ROOT = Path("data/raw/images")

results_data = []

for channel_dir in IMAGE_ROOT.iterdir():

    if not channel_dir.is_dir():
        continue

    channel_name = channel_dir.name

    for image_file in channel_dir.glob("*.jpg"):

        message_id = image_file.stem

        print(f"Processing: {image_file}")

        try:
            results = model(str(image_file))

            for result in results:

                if len(result.boxes) == 0:
                    results_data.append({
                        "message_id": message_id,
                        "channel_name": channel_name,
                        "image_path": str(image_file),
                        "object_name": None,
                        "confidence_score": None
                    })

                else:
                    for box in result.boxes:

                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])

                        results_data.append({
                            "message_id": message_id,
                            "channel_name": channel_name,
                            "image_path": str(image_file),
                            "object_name": model.names[class_id],
                            "confidence_score": round(confidence, 4)
                        })

        except Exception as e:
            print(f"Error processing {image_file}: {e}")

# Save to CSV
output_dir = Path("data/enriched")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "yolo_detections.csv"

df = pd.DataFrame(results_data)
df.to_csv(output_file, index=False)

print("\n=================================")
print(f"Processed images: {df['message_id'].nunique()}")
print(f"Detection records: {len(df)}")
print(f"Saved CSV: {output_file}")
print("=================================")