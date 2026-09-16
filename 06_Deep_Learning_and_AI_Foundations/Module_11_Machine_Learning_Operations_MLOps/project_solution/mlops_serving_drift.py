"""Production solution for DynamicBatchingQueue and DataDriftDetector."""
from __future__ import annotations

import numpy as np


class DynamicBatchingQueue:
    """Collects individual requests and packs them into optimal GPU inference batches."""

    def __init__(self, max_batch_size: int = 16):
        self.max_batch_size = max_batch_size

    def pack_batch(self, items: list[np.ndarray]) -> tuple[np.ndarray, list[int]]:
        assert len(items) > 0, "Cannot pack empty batch."
        batch_slice = items[: self.max_batch_size]
        lengths = [len(item) for item in batch_slice]
        stacked = np.stack(batch_slice, axis=0)
        return stacked, lengths


class DataDriftDetector:
    """Detects feature distribution shifts using Kolmogorov-Smirnov two-sample statistic."""

    @staticmethod
    def compute_ks_statistic(sample_ref: np.ndarray, sample_prod: np.ndarray) -> float:
        ref = np.sort(np.asarray(sample_ref, dtype=float))
        prod = np.sort(np.asarray(sample_prod, dtype=float))

        # Union of all evaluation points
        all_points = np.concatenate([ref, prod])
        # Compute empirical CDFs
        cdf_ref = np.searchsorted(ref, all_points, side="right") / len(ref)
        cdf_prod = np.searchsorted(prod, all_points, side="right") / len(prod)

        # Maximum vertical gap
        return float(np.max(np.abs(cdf_ref - cdf_prod)))
