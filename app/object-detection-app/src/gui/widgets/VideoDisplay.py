import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPaintEvent

class VideoDisplay(QLabel):
    """Video display widget for showing camera feed"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self) -> None:
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(640, 480)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        font = QFont('Arial', 12)
        self.setFont(font)
        
        self.setStyleSheet("""
            QLabel {
                color: #666666;
                background-color: #1e1e1e;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        self.setText("No video input")
    
    def minimumSizeHint(self) -> QSize:
        return QSize(640, 480)

    def sizeHint(self) -> QSize:
        return QSize(800, 600)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        
        if not self.pixmap():
            painter = QPainter(self)
            painter.setPen(QPen(QColor('#666666')))
            painter.drawText(
                self.rect(), 
                Qt.AlignmentFlag.AlignCenter,
                "No video input"
            )
    
    @pyqtSlot()
    def clear(self) -> None:
        super().clear()
        self.setText("No video input")