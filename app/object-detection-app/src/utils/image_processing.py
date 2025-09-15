import cv2
import numpy as np
from typing import Tuple, Optional

def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Resize an image to specified dimensions.
    
    Args:
        image (np.ndarray): Input image
        width (int): Target width
        height (int): Target height
    
    Returns:
        np.ndarray: Resized image
    """
    return cv2.resize(image, (width, height))

def convert_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Convert BGR image to RGB format.
    
    Args:
        image (np.ndarray): Input BGR image
    
    Returns:
        np.ndarray: RGB image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def draw_detection_box(
    image: np.ndarray,
    box: Tuple[int, int, int, int],
    label: str,
    confidence: float,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """
    Draw detection box with label on image.
    
    Args:
        image (np.ndarray): Input image
        box (tuple): Box coordinates (x1, y1, x2, y2)
        label (str): Detection label
        confidence (float): Detection confidence
        color (tuple): Box color in BGR
        thickness (int): Line thickness
    
    Returns:
        np.ndarray: Image with drawn detection
    """
    x1, y1, x2, y2 = box
    
    # Draw bounding box
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
    
    # Draw label background
    label_text = f"{label} {confidence:.2f}"
    (text_width, text_height), baseline = cv2.getTextSize(
        label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, thickness
    )
    cv2.rectangle(
        image,
        (x1, y1 - text_height - baseline - 5),
        (x1 + text_width, y1),
        color,
        -1
    )
    
    # Draw label text
    cv2.putText(
        image,
        label_text,
        (x1, y1 - baseline - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        thickness
    )
    
    return image

def preprocess_frame(
    frame: np.ndarray,
    target_size: Tuple[int, int] = (640, 360),
    normalize: bool = True
) -> np.ndarray:
    """
    Preprocess frame for inference.
    
    Args:
        frame (np.ndarray): Input frame
        target_size (tuple): Target size (width, height)
        normalize (bool): Whether to normalize pixel values
    
    Returns:
        np.ndarray: Preprocessed frame
    """
    # Resize frame
    resized_frame = resize_image(frame, target_size[0], target_size[1])
    
    # Convert to RGB
    rgb_frame = convert_to_rgb(resized_frame)
    
    # Normalize if requested
    if normalize:
        rgb_frame = rgb_frame.astype(np.float32) / 255.0
        
    return rgb_frame

def create_overlay(
    image: np.ndarray,
    text: str,
    position: Tuple[int, int],
    font_scale: float = 0.8,
    color: Tuple[int, int, int] = (255, 255, 255),
    thickness: int = 1
) -> np.ndarray:
    """
    Create text overlay with background on image.
    
    Args:
        image (np.ndarray): Input image
        text (str): Text to display
        position (tuple): Text position (x, y)
        font_scale (float): Font scale
        color (tuple): Text color in BGR
        thickness (int): Text thickness
    
    Returns:
        np.ndarray: Image with overlay
    """
    x, y = position
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
    )
    
    # Draw background rectangle
    cv2.rectangle(
        image,
        (x - 5, y - text_height - 5),
        (x + text_width + 5, y + 5),
        (0, 0, 0),
        -1
    )
    
    # Draw text
    cv2.putText(
        image,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
        cv2.LINE_AA
    )
    
    return image