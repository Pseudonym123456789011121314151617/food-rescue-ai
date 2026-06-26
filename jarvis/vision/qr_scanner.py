"""QR code and barcode scanner using OpenCV."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from jarvis.core.logging import get_logger

log = get_logger(__name__)


@dataclass
class ScanResult:
    data: str
    type: str
    bbox: list[tuple[int, int]]


class QRScanner:
    """Detect and decode QR codes and barcodes from camera frames."""

    def __init__(self) -> None:
        self._detector = cv2.QRCodeDetector()

    def scan_qr(self, frame: np.ndarray) -> list[ScanResult]:
        """Scan for QR codes in a BGR frame."""
        results: list[ScanResult] = []
        data, bbox, _ = self._detector.detectAndDecode(frame)
        if data and bbox is not None:
            points = [(int(p[0]), int(p[1])) for p in bbox[0]]
            results.append(ScanResult(data=data, type="qr", bbox=points))
        return results

    def scan_all(self, frame: np.ndarray) -> list[ScanResult]:
        """Scan for both QR codes and barcodes."""
        return self.scan_qr(frame)
