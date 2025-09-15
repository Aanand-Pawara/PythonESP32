import cv2
from ultralytics import YOLO
import torch

class ObjectDetector:
    def __init__(self, model_path="best.pt"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = YOLO(model_path).to(self.device)
    
    def process_frame(self, frame, conf_threshold=0.5):
        results = self.model(frame, verbose=False)
        result = results[0]
        
        # Draw detections
        for box in result.boxes:
            if box.conf < conf_threshold:
                continue
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf)
            cls = int(box.cls)
            name = self.model.names[cls]
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{name} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame