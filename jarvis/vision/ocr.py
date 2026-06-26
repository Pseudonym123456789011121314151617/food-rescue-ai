"""Optical character recognition from images / camera frames."""

from __future__ import annotations

import cv2
import numpy as np

from jarvis.core.logging import get_logger

log = get_logger(__name__)


class OCREngine:
    """Extract text from images using preprocessing + optional Tesseract."""

    def __init__(self) -> None:
        self._tesseract_available = False
        try:
            import pytesseract  # noqa: F401

            self._tesseract_available = True
        except ImportError:
            log.info("pytesseract_not_installed_ocr_limited")

    def extract_text(self, image: np.ndarray) -> str:
        """Extract text from a BGR image."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        if self._tesseract_available:
            import pytesseract

            return str(pytesseract.image_to_string(gray)).strip()

        log.warning("ocr_unavailable_without_tesseract")
        return ""

    def extract_from_region(
        self,
        image: np.ndarray,
        x: int,
        y: int,
        w: int,
        h: int,
    ) -> str:
        """Extract text from a specific region of the image."""
        roi = image[y : y + h, x : x + w]
        return self.extract_text(roi)
