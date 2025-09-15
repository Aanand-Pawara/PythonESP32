import unittest
from src.core.camera import CameraStream

class TestCameraStream(unittest.TestCase):

    def setUp(self):
        self.camera = CameraStream()

    def test_camera_open(self):
        self.camera.open()
        self.assertTrue(self.camera.cap.isOpened(), "Camera should be opened.")

    def test_camera_read(self):
        self.camera.open()
        ret, frame = self.camera.read()
        self.assertTrue(ret, "Frame should be read successfully.")
        self.assertIsNotNone(frame, "Frame should not be None.")

    def test_camera_release(self):
        self.camera.open()
        self.camera.release()
        self.assertFalse(self.camera.cap.isOpened(), "Camera should be released.")

    def tearDown(self):
        self.camera.release()

if __name__ == '__main__':
    unittest.main()