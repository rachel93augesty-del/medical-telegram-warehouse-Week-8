import torch
from ultralytics.nn.tasks import DetectionModel
from ultralytics.nn.modules import Conv, Bottleneck, C3, SPPF, DWConv, Focus, Detect

torch.serialization.add_safe_globals([
    DetectionModel,
    Conv,
    Bottleneck,
    C3,
    SPPF,
    DWConv,
    Focus,
    Detect
])

from ultralytics import YOLO

model = YOLO("yolov8n.pt")

# ✅ Confirm it loaded
print("✅ YOLOv8 model loaded successfully!")
print("Detected class names:", model.names)
