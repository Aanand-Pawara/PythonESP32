import cv2
import traceback
from ultralytics import YOLO
import threading
import time
import torch

class CameraStream:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.lock = threading.Lock()
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            with self.lock:
                self.ret = ret
                self.frame = frame

    def read(self):
        with self.lock:
            return self.ret, self.frame.copy()

    def release(self):
        self.running = False
        self.cap.release()

def draw_shadow_text(img, text, pos, font=cv2.FONT_HERSHEY_SIMPLEX, scale=0.8):
    x, y = pos
    (w, h), _ = cv2.getTextSize(text, font, scale, 1)
    cv2.rectangle(img, (x - 5, y - h - 5), (x + w + 5, y + 5), (0, 0, 0), -1)
    cv2.putText(img, text, (x, y), font, scale, (255, 255, 255), 1, cv2.LINE_AA)

def detect_objects_from_camera():
    print("🎥 Starting threaded webcam...")
    stream = CameraStream()
    
    if not stream.cap.isOpened():
        print("❌ Cannot access webcam.")
        return

    try:
        print("🧠 Loading YOLOv8 model...")
        model = YOLO("best.pt").to("cuda" if torch.cuda.is_available() else "cpu")
        print("✅ Model loaded.")
    except Exception as e:
        print(f"❌ Model load failed: {e}")
        traceback.print_exc()
        return

    print("🚀 Detection started. Press 'q' to quit.")
    prev_time = time.time()
    
    while True:
        ret, frame = stream.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        resized = cv2.resize(frame, (640, 360))

        try:
            results = model(resized, verbose=False)
        except Exception as e:
            print(f"❌ Inference failed: {e}")
            traceback.print_exc()
            break

        result = results[0]
        boxes = result.boxes.xyxy.cpu().numpy()
        confs = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()
        names = model.names

        scale_x = frame.shape[1] / resized.shape[1]
        scale_y = frame.shape[0] / resized.shape[0]

        for i, box in enumerate(boxes):
            conf = confs[i]
            if conf < 0.5:
                continue
            class_id = int(classes[i])
            x1, y1, x2, y2 = map(int, [box[0]*scale_x, box[1]*scale_y, box[2]*scale_x, box[3]*scale_y])
            label = f"{names[class_id]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        fps = 1 / (time.time() - prev_time)
        prev_time = time.time()
        draw_shadow_text(frame, f"FPS: {fps:.2f}", (10, 30))
        draw_shadow_text(frame, "@Aditi", (10, 60))

        cv2.imshow("Optimized Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("👋 Exiting...")
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_objects_from_camera()
