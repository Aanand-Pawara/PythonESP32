from ultralytics import YOLO

# Load the model
model = YOLO("best.pt")

# Export to ONNX (make sure ONNX installed)
model.export(format="onnx", opset=12, dynamic=False, simplify=True, imgsz=640)

print("✅ Exported to ONNX.")
