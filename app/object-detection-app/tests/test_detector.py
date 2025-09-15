import unittest
from src.core.detector import ObjectDetector

class TestObjectDetector(unittest.TestCase):
    
    def setUp(self):
        self.detector = ObjectDetector(model_path='models/best.pt')

    def test_model_loading(self):
        self.assertIsNotNone(self.detector.model, "Model should be loaded successfully.")

    def test_detection(self):
        test_frame = ...  # Replace with a valid test frame
        detections = self.detector.detect(test_frame)
        self.assertIsInstance(detections, list, "Detections should be a list.")
        for detection in detections:
            self.assertIn('box', detection, "Detection should contain 'box'.")
            self.assertIn('confidence', detection, "Detection should contain 'confidence'.")
            self.assertIn('class_id', detection, "Detection should contain 'class_id'.")

if __name__ == '__main__':
    unittest.main()