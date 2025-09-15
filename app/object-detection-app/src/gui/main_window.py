from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QStatusBar
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from src.gui.widgets.VideoDisplay import VideoDisplay
from src.gui.widgets.controls import ControlPanel
from src.core.ESP32Camera import ESP32Camera
from src.core.detector import ObjectDetector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupDetector()
        self.setupCamera()

    def initUI(self):
        self.setWindowTitle("Object Detection System")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Camera connection controls
        camera_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter ESP32-CAM IP address")
        self.connect_button = QPushButton("Connect Camera")
        self.connect_button.clicked.connect(self.toggle_camera)
        camera_layout.addWidget(self.ip_input)
        camera_layout.addWidget(self.connect_button)
        layout.addLayout(camera_layout)

        # Video display
        self.video_display = VideoDisplay()
        layout.addWidget(self.video_display)

        # Detection controls
        self.control_panel = ControlPanel()
        layout.addWidget(self.control_panel)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def setupDetector(self):
        try:
            self.detector = ObjectDetector()
            self.statusBar.showMessage("Model loaded successfully")
        except Exception as e:
            self.statusBar.showMessage(f"Error loading model: {str(e)}")

    def setupCamera(self):
        self.camera = ESP32Camera()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def toggle_camera(self):
        if not self.camera.is_connected:
            ip = self.ip_input.text()
            if self.camera.connect(ip):
                self.connect_button.setText("Disconnect")
                self.statusBar.showMessage("Connected to ESP32-CAM")
                self.timer.start(30)  # 30ms = ~33fps
            else:
                self.statusBar.showMessage("Failed to connect to ESP32-CAM")
        else:
            self.camera.disconnect()
            self.timer.stop()
            self.connect_button.setText("Connect Camera")
            self.statusBar.showMessage("Disconnected from ESP32-CAM")
            self.video_display.clear()

    def update_frame(self):
        if not self.camera.is_connected:
            return

        success, frame = self.camera.get_frame()
        if not success:
            return

        # Process frame with detector
        processed_frame = self.detector.process_frame(
            frame,
            conf_threshold=self.control_panel.conf_slider.value() / 100
        )

        # Convert to Qt format and display
        h, w, ch = processed_frame.shape
        qt_image = QImage(processed_frame.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(self.video_display.size(), Qt.KeepAspectRatio)
        self.video_display.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        if self.camera.is_connected:
            self.camera.disconnect()
        event.accept()