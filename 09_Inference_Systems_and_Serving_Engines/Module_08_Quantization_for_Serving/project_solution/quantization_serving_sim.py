from __future__ import annotations

import dataclasses
import numpy as np


@dataclasses.dataclass
class QuantResult:
    q_tensor: np.ndarray
    scale: float
    reconstructed: np.ndarray
    mse_error: float
    compression_ratio: float


class UniformQuantizer:
    """Simulates symmetric INT8 and INT4 quantization and dequantization."""

    @staticmethod
    def quantize_symmetric(x: np.ndarray, bits: int = 8) -> QuantResult:
        qmin = -(2 ** (bits - 1))
        qmax = (2 ** (bits - 1)) - 1

        max_val = np.max(np.abs(x))
        scale = float(max_val / qmax) if max_val > 0 else 1.0

        q = np.clip(np.round(x / scale), qmin, qmax).astype(np.int8 if bits == 8 else np.int32)
        reconstructed = (q * scale).astype(np.float32)
        mse = float(np.mean((x - reconstructed) ** 2))

        # FP32 original is 32 bits, target is bits
        compression = 32.0 / bits

        return QuantResult(
            q_tensor=q,
            scale=scale,
            reconstructed=reconstructed,
            mse_error=round(mse, 6),
            compression_ratio=compression,
        )

    @staticmethod
    def apply_smoothquant_transform(
        act: np.ndarray,
        weights: np.ndarray,
        alpha: float = 0.5,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Migrates dynamic range difficulty from activations to weights."""
        # act: (B, H), weights: (H, Out)
        act_max = np.max(np.abs(act), axis=0) + 1e-6
        weight_max = np.max(np.abs(weights), axis=1) + 1e-6

        scale = (np.power(act_max, alpha) / np.power(weight_max, 1.0 - alpha)).astype(np.float32)

        smoothed_act = act / scale
        smoothed_weights = weights * scale[:, np.newaxis]

        return smoothed_act, smoothed_weights
