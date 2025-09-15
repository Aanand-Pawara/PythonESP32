import torch
from ultralytics import YOLO

def load_model(weights_path):
    try:
        print("🧠 Loading YOLO model...")
        model = YOLO(weights_path).to("cuda" if torch.cuda.is_available() else "cpu")
        print("✅ Model loaded.")
        return model
    except Exception as e:
        print(f"❌ Model load failed: {e}")
        raise