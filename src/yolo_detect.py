# src/yolo_detect.py

import os
import pandas as pd
import torch
from ultralytics import YOLO

# -------------------------------
# CONFIG
# -------------------------------
RAW_IMAGE_DIR = "data/raw/images"
OUTPUT_CSV = "data/processed/yolo_detections.csv"

YOLO_MODEL_PATH = "yolov8n.pt"
PRODUCT_CLASSES = ['bottle', 'cup', 'container', 'jar']

# -------------------------------
# LOAD MODEL
# -------------------------------
print("Loading YOLO model...")
model = YOLO(YOLO_MODEL_PATH)

# -------------------------------
# SCAN IMAGES
# -------------------------------
image_files = []
for root, dirs, files in os.walk(RAW_IMAGE_DIR):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_files.append(os.path.join(root, f))

if not image_files:
    print(f"No images found in {RAW_IMAGE_DIR}. Exiting.")
    exit()

print(f"Found {len(image_files)} images.")

# -------------------------------
# RUN DETECTION
# -------------------------------
all_detections = []

for img_path in image_files:
    print(f"Processing {img_path}...")
    results = model(img_path)
    result = results[0]

    # If there are detections
    if result.boxes is not None and len(result.boxes) > 0:
        boxes = result.boxes
        data = {
            'image_file': [os.path.basename(img_path)] * len(boxes),
            'channel': [os.path.basename(os.path.dirname(img_path))] * len(boxes),
            'message_id': [None] * len(boxes),
            'detected_class': [model.names[int(c)] for c in boxes.cls],
            'confidence_score': boxes.conf.tolist()
        }
        df = pd.DataFrame(data)
    else:
        # No detections
        df = pd.DataFrame([{
            'image_file': os.path.basename(img_path),
            'channel': os.path.basename(os.path.dirname(img_path)),
            'message_id': None,
            'detected_class': None,
            'confidence_score': None
        }])

    all_detections.append(df)

# Combine all detections
df_all = pd.concat(all_detections, ignore_index=True, sort=False)

# -------------------------------
# -------------------------------
# IMAGE CLASSIFICATION
# -------------------------------
def classify_image(group):
    classes = group['detected_class'].dropna().tolist()
    has_person = 'person' in classes
    has_product = any(c in PRODUCT_CLASSES for c in classes)

    if has_person and has_product:
        return 'promotional'
    elif has_product and not has_person:
        return 'product_display'
    elif has_person and not has_product:
        return 'lifestyle'
    else:
        return 'other'

# Use transform instead of apply + reindex
df_all['image_category'] = df_all.groupby('image_file')['detected_class'].transform(lambda x: classify_image(df_all[df_all['image_file'] == x.name]))

# -------------------------------
# SAVE RESULTS
# -------------------------------
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df_all.to_csv(OUTPUT_CSV, index=False)
print(f"Detection CSV saved to {OUTPUT_CSV}")
