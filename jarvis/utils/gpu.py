"""GPU detection and acceleration helpers."""

from __future__ import annotations

from dataclasses import dataclass

from jarvis.core.logging import get_logger

log = get_logger(__name__)


@dataclass
class GPUInfo:
    name: str
    memory_total_mb: int
    memory_used_mb: int
    utilization_percent: float
    driver_version: str


def detect_gpu() -> GPUInfo | None:
    """Detect the primary GPU and return its info."""
    # Try NVIDIA via nvidia-smi
    try:
        import subprocess

        result = subprocess.run(  # noqa: S603, S607
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.used,utilization.gpu,driver_version",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        parts = result.stdout.strip().split(", ")
        if len(parts) >= 5:
            return GPUInfo(
                name=parts[0],
                memory_total_mb=int(float(parts[1])),
                memory_used_mb=int(float(parts[2])),
                utilization_percent=float(parts[3]),
                driver_version=parts[4],
            )
    except Exception:
        pass

    log.debug("no_gpu_detected")
    return None


def is_cuda_available() -> bool:
    """Check if CUDA is available for GPU acceleration."""
    try:
        import subprocess

        result = subprocess.run(  # noqa: S603, S607
            ["nvidia-smi"],
            capture_output=True,
            check=True,
        )
        return result.returncode == 0
    except Exception:
        return False


def get_onnx_providers() -> list[str]:
    """Return available ONNX Runtime execution providers."""
    try:
        import onnxruntime

        return list(onnxruntime.get_available_providers())
    except ImportError:
        return ["CPUExecutionProvider"]
