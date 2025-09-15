import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import traceback
from ultralytics import YOLO
import time
import torch
from main import CameraStream

class DetectionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Object Detection")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create video display label
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        # Controls
        self.start_button = QPushButton("Start Detection")
        self.start_button.clicked.connect(self.toggle_detection)
        self.layout.addWidget(self.start_button)

        # Initialize variables
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.is_detecting = False
        self.stream = None
        self.model = None
        self.prev_time = time.time()

        try:
            print("🧠 Loading YOLOv8 model...")
            self.model = YOLO("best.pt").to("cuda" if torch.cuda.is_available() else "cpu")
            print("✅ Model loaded.")
        except Exception as e:
            print(f"❌ Model load failed: {e}")
            traceback.print_exc()

    def toggle_detection(self):
        if not self.is_detecting:
            self.start_detection()
        else:
            self.stop_detection()

    def start_detection(self):
        self.stream = CameraStream()
        if not self.stream.cap.isOpened():
            print("❌ Cannot access webcam.")
            return

        self.start_button.setText("Stop Detection")
        self.is_detecting = True
        self.timer.start(30)  # Update every 30ms

    def stop_detection(self):
        self.timer.stop()
        if self.stream:
            self.stream.release()
        self.start_button.setText("Start Detection")
        self.is_detecting = False
        self.video_label.clear()

    def update_frame(self):
        ret, frame = self.stream.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        resized = cv2.resize(frame, (640, 360))

        try:
            results = self.model(resized, verbose=False)
            result = results[0]
            boxes = result.boxes.xyxy.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()
            names = self.model.names

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

            fps = 1 / (time.time() - self.prev_time)
            self.prev_time = time.time()

            # Convert for Qt display
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            qt_image = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio)
            self.video_label.setPixmap(scaled_pixmap)

        except Exception as e:
            print(f"❌ Inference failed: {e}")
            traceback.print_exc()
            self.stop_detection()

    def closeEvent(self, event):
        self.stop_detection()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DetectionGUI()
    window.show()
    sys.exit(app.exec_())