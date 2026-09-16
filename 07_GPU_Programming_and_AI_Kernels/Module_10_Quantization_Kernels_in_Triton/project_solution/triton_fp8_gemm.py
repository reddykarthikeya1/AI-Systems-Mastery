"""FP8 Matrix Multiplication Simulator and Triton Kernel Emulation."""

from __future__ import annotations

import numpy as np


class FP8GemmSimulator:
    """Simulates FP8 (E4M3 and E5M2) scaled GEMM with FP32 accumulation."""

    @staticmethod
    def quantize_fp8_e4m3(tensor: np.ndarray, scale: float = 1.0) -> np.ndarray:
        """Quantizes to E4M3 range [-448, 448]."""
        scaled = tensor * scale
        clamped = np.clip(scaled, -448.0, 448.0)
        step = 448.0 / (2**7)
        quantized = np.round(clamped / step) * step
        return quantized / scale

    @staticmethod
    def quantize_fp8_e5m2(tensor: np.ndarray, scale: float = 1.0) -> np.ndarray:
        """Quantizes to E5M2 range [-57344, 57344]."""
        scaled = tensor * scale
        clamped = np.clip(scaled, -57344.0, 57344.0)
        step = 57344.0 / (2**6)
        quantized = np.round(clamped / step) * step
        return quantized / scale

    @classmethod
    def matmul_fp8(
        cls,
        a: np.ndarray,
        b: np.ndarray,
        scale_a: float = 1.0,
        scale_b: float = 1.0,
        format_type: str = "e4m3",
    ) -> np.ndarray:
        """Simulates Tensor Core GEMM with FP8 inputs and FP32 accumulation."""
        if format_type == "e4m3":
            q_a = cls.quantize_fp8_e4m3(a, scale_a)
            q_b = cls.quantize_fp8_e4m3(b, scale_b)
        else:
            q_a = cls.quantize_fp8_e5m2(a, scale_a)
            q_b = cls.quantize_fp8_e5m2(b, scale_b)

        c = np.matmul(q_a.astype(np.float32), q_b.astype(np.float32))
        return c
