import cv2
import logging
import requests
import threading
import numpy as np
from typing import Optional, Tuple


class ESP32Camera:
    def __init__(self):
        self.stream = None
        self.is_connected = False
        self.running = False
        self.current_frame = None
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def connect(self, ip_address: str) -> bool:
        try:
            # Don’t strip http:// if user gives full URL
            if ip_address.startswith("http"):
                base_url = ip_address.rstrip("/")
            else:
                base_url = f"http://{ip_address}"

            # Some sketches serve on / or /stream, not always :81
            test_url = f"{base_url}/"
            stream_url = f"{base_url}/stream"

            self.logger.info(f"Testing connection to {test_url}")
            response = requests.get(test_url, timeout=5)

            if response.status_code != 200:
                raise Exception("ESP32-CAM not responding")

            self.logger.info(f"Opening video stream from {stream_url}")
            self.stream = cv2.VideoCapture(stream_url)

            if not self.stream.isOpened():
                raise Exception("Could not open video stream")

            self.is_connected = True
            self.running = True
            threading.Thread(target=self._capture_loop, daemon=True).start()
            self.logger.info(f"Connected to ESP32-CAM at {base_url}")
            return True

        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            return False

    def disconnect(self) -> None:
        self.running = False
        if self.stream:
            self.stream.release()
        self.is_connected = False
        self.current_frame = None
        self.logger.info("Disconnected from ESP32-CAM")

    def get_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        with self.lock:
            if self.current_frame is None:
                return False, None
            return True, self.current_frame.copy()

    def _capture_loop(self) -> None:
        while self.running:
            try:
                ret, frame = self.stream.read()
                if ret:
                    with self.lock:
                        self.current_frame = frame
            except Exception as e:
                self.logger.error(f"Frame capture error: {e}")
                self.disconnect()
                break