import cv2
import threading

class CameraStream:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.ret, self.frame = self.cap.read()
        self.lock = threading.Lock()
        self.running = True
        threading.Thread(target=self._update, daemon=True).start()
    
    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            with self.lock:
                self.ret = ret
                self.frame = frame
    
    def read(self):
        with self.lock:
            if self.frame is None:
                return None
            return cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    
    def is_opened(self):
        return self.cap.isOpened()
    
    def release(self):
        self.running = False
        if self.cap:
            self.cap.release()