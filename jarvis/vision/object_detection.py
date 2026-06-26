"""Object and hand detection using OpenCV DNN."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from jarvis.core.logging import get_logger

log = get_logger(__name__)


@dataclass
class DetectedObject:
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]


class ObjectDetector:
    """Detect objects in camera frames using DNN models."""

    # Common COCO labels subset
    COCO_LABELS: list[str] = [
        "person",
        "bicycle",
        "car",
        "motorbike",
        "aeroplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "backpack",
        "umbrella",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "sofa",
        "potted plant",
        "bed",
        "dining table",
        "toilet",
        "tv monitor",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair dryer",
        "toothbrush",
    ]

    def __init__(self) -> None:
        self._net: cv2.dnn.Net | None = None

    def detect(
        self,
        frame: np.ndarray,
        confidence_threshold: float = 0.5,
    ) -> list[DetectedObject]:
        """Detect objects in a BGR frame (fallback to contour-based detection)."""
        # Without a pre-loaded DNN model, fall back to simple contour detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        edges = cv2.Canny(blurred, 30, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        results: list[DetectedObject] = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 500:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            results.append(
                DetectedObject(
                    label="object",
                    confidence=min(1.0, area / 10000),
                    bbox=(x, y, x + w, y + h),
                )
            )
        return results


class HandDetector:
    """Simple skin-color-based hand detection."""

    def detect_hands(self, frame: np.ndarray) -> list[tuple[int, int, int, int]]:
        """Return bounding boxes of detected hand regions."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 48, 80], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask, kernel, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        hands: list[tuple[int, int, int, int]] = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 3000:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            hands.append((x, y, x + w, y + h))
        return hands
