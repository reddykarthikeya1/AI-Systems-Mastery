"""Starter template for DynamicBatchingQueue and DataDriftDetector."""
from __future__ import annotations

import numpy as np


class DynamicBatchingQueue:
    """Collects individual requests and packs them into optimal GPU inference batches."""

    def __init__(self, max_batch_size: int = 16):
        self.max_batch_size = max_batch_size
        raise NotImplementedError

    def pack_batch(self, items: list[np.ndarray]) -> tuple[np.ndarray, list[int]]:
        """Pack list of 1D feature arrays into 2D batch array and return item lengths."""
        raise NotImplementedError


class DataDriftDetector:
    """Detects feature distribution shifts using Kolmogorov-Smirnov two-sample statistic."""

    @staticmethod
    def compute_ks_statistic(sample_ref: np.ndarray, sample_prod: np.ndarray) -> float:
        """Compute two-sample Kolmogorov-Smirnov distance: max|CDF_ref(x) - CDF_prod(x)|."""
        raise NotImplementedError
