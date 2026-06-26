"""Face detection and recognition using OpenCV + optional InsightFace."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np

from jarvis.core.logging import get_logger

log = get_logger(__name__)


@dataclass
class FaceResult:
    bbox: tuple[int, int, int, int]
    confidence: float
    encoding: np.ndarray | None = None
    landmarks: np.ndarray | None = None
    smile_score: float = 0.0


class FaceRecognizer:
    """Detect and encode faces from camera frames."""

    def __init__(self, use_insightface: bool = True) -> None:
        self._use_insightface = use_insightface
        self._insightface_app: Any = None
        self._cascade: cv2.CascadeClassifier | None = None
        self._smile_cascade: cv2.CascadeClassifier | None = None
        self._init_detectors()

    def _init_detectors(self) -> None:
        if self._use_insightface:
            try:
                from insightface.app import FaceAnalysis

                self._insightface_app = FaceAnalysis(
                    name="buffalo_l", providers=["CPUExecutionProvider"]
                )
                self._insightface_app.prepare(ctx_id=0, det_size=(640, 640))
                log.info("insightface_initialized")
                return
            except ImportError:
                log.info("insightface_not_available_falling_back_to_opencv")
            except Exception:
                log.exception("insightface_init_error")

        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  # type: ignore[attr-defined]
        self._cascade = cv2.CascadeClassifier(cascade_path)
        smile_path = cv2.data.haarcascades + "haarcascade_smile.xml"  # type: ignore[attr-defined]
        self._smile_cascade = cv2.CascadeClassifier(smile_path)

    def detect_faces(self, frame: np.ndarray) -> list[FaceResult]:
        """Detect faces in a BGR frame and return results."""
        if self._insightface_app is not None:
            return self._detect_insightface(frame)
        return self._detect_opencv(frame)

    def get_encoding(self, frame: np.ndarray) -> bytes | None:
        """Return the face encoding of the largest face, or None."""
        results = self.detect_faces(frame)
        if not results or results[0].encoding is None:
            return None
        return results[0].encoding.astype(np.float32).tobytes()

    def compare(self, encoding_a: bytes, encoding_b: bytes) -> float:
        """Return the Euclidean distance between two face encodings."""
        a = np.frombuffer(encoding_a, dtype=np.float32)
        b = np.frombuffer(encoding_b, dtype=np.float32)
        return float(np.linalg.norm(a - b))

    def _detect_insightface(self, frame: np.ndarray) -> list[FaceResult]:
        faces = self._insightface_app.get(frame)
        results: list[FaceResult] = []
        for face in faces:
            bbox = tuple(int(v) for v in face.bbox)
            results.append(
                FaceResult(
                    bbox=(bbox[0], bbox[1], bbox[2], bbox[3]),
                    confidence=float(face.det_score),
                    encoding=face.embedding if hasattr(face, "embedding") else None,
                    landmarks=face.landmark_2d_106 if hasattr(face, "landmark_2d_106") else None,
                )
            )
        return results

    def _detect_opencv(self, frame: np.ndarray) -> list[FaceResult]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        assert self._cascade is not None
        faces = self._cascade.detectMultiScale(gray, 1.3, 5)
        results: list[FaceResult] = []
        for x, y, w, h in faces:
            smile_score = 0.0
            if self._smile_cascade is not None:
                roi = gray[y : y + h, x : x + w]
                smiles = self._smile_cascade.detectMultiScale(roi, 1.8, 20)
                smile_score = min(1.0, len(smiles) * 0.5) if len(smiles) > 0 else 0.0
            results.append(
                FaceResult(
                    bbox=(x, y, x + w, y + h),
                    confidence=0.9,
                    smile_score=smile_score,
                )
            )
        return results
