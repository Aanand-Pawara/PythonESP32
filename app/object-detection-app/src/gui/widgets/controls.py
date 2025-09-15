from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, 
    QLabel, QComboBox, QSlider, QFrame,
    QGridLayout, QSpinBox, QProgressBar, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Detection Control Panel")
        title.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(title)
        
        # Add separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Detection controls group
        detection_group = QFrame()
        detection_layout = QVBoxLayout(detection_group)
        
        # Start/Stop button with icon
        self.start_button = QPushButton("▶️ Start Detection")
        detection_layout.addWidget(self.start_button)
        
        # Model selection group
        model_label = QLabel("Model Configuration:")
        model_label.setFont(QFont('Arial', 10, QFont.Bold))
        detection_layout.addWidget(model_label)
        
        model_grid = QGridLayout()
        
        # Model dropdown
        model_type_label = QLabel("Select Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItem("YOLOv8")
        self.model_combo.addItem("YOLOv8-nano")
        self.model_combo.addItem("YOLOv8-small")
        model_grid.addWidget(model_type_label, 0, 0)
        model_grid.addWidget(self.model_combo, 0, 1)
        
        detection_layout.addLayout(model_grid)
        
        # Add separator
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        detection_layout.addWidget(line2)
        
        # Detection parameters
        params_label = QLabel("Detection Parameters:")
        params_label.setFont(QFont('Arial', 10, QFont.Bold))
        detection_layout.addWidget(params_label)
        
        # Confidence threshold
        conf_layout = QVBoxLayout()
        conf_header = QHBoxLayout()
        conf_label = QLabel("Confidence Threshold:")
        self.conf_value = QLabel("50%")
        conf_header.addWidget(conf_label)
        conf_header.addWidget(self.conf_value)
        conf_layout.addLayout(conf_header)
        
        self.conf_slider = QSlider(Qt.Horizontal)
        self.conf_slider.setRange(0, 100)
        self.conf_slider.setValue(50)
        self.conf_slider.valueChanged.connect(
            lambda v: self.conf_value.setText(f"{v}%")
        )
        conf_layout.addWidget(self.conf_slider)
        detection_layout.addLayout(conf_layout)
        
        # FPS control
        fps_layout = QHBoxLayout()
        fps_label = QLabel("Target FPS:")
        self.fps_spinbox = QSpinBox()
        self.fps_spinbox.setRange(1, 60)
        self.fps_spinbox.setValue(30)
        fps_layout.addWidget(fps_label)
        fps_layout.addWidget(self.fps_spinbox)
        detection_layout.addLayout(fps_layout)
        
        layout.addWidget(detection_group)
        
        # Statistics group
        stats_group = QFrame()
        stats_layout = QVBoxLayout(stats_group)
        
        stats_label = QLabel("Detection Statistics:")
        stats_label.setFont(QFont('Arial', 10, QFont.Bold))
        stats_layout.addWidget(stats_label)
        
        # Current FPS
        self.fps_label = QLabel("Current FPS: 0")
        stats_layout.addWidget(self.fps_label)
        
        # Detection count
        self.detection_count = QLabel("Detections: 0")
        stats_layout.addWidget(self.detection_count)
        
        # Processing time
        self.process_time = QLabel("Processing Time: 0 ms")
        stats_layout.addWidget(self.process_time)
        
        layout.addWidget(stats_group)
        
        # GPU Memory usage
        memory_label = QLabel("GPU Memory Usage:")
        layout.addWidget(memory_label)
        
        self.memory_bar = QProgressBar()
        self.memory_bar.setRange(0, 100)
        self.memory_bar.setValue(0)
        layout.addWidget(self.memory_bar)
        
        layout.addStretch()
        
        # Set styles
        self.setStyleSheet("""
            QPushButton {
                min-height: 30px;
                padding: 5px;
                background-color: #2196F3;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
            QComboBox {
                min-height: 30px;
                padding: 5px;
            }
            QLabel {
                color: #333333;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #DDDDDD;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                border: 2px solid #2196F3;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QProgressBar {
                border: 2px solid #DDDDDD;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
            }
            QFrame {
                border: 2px solid #DDDDDD;
                border-radius: 6px;
                padding: 5px;
            }
        """)
    
    def update_stats(self, fps, detections, process_time, memory_usage):
        """Update detection statistics"""
        self.fps_label.setText(f"Current FPS: {fps:.1f}")
        self.detection_count.setText(f"Detections: {detections}")
        self.process_time.setText(f"Processing Time: {process_time:.1f} ms")
        self.memory_bar.setValue(int(memory_usage))