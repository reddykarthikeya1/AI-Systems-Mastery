"""Starter template for Parallel Reduction and Scan Engine."""
from __future__ import annotations

import numpy as np


def warp_shuffle_down_reduce(vals: list[float]) -> float:
    """Simulate __shfl_down_sync tree reduction within a 32-thread warp."""
    raise NotImplementedError("Implement warp_shuffle_down_reduce")


def block_tree_reduce(arr: np.ndarray, block_size: int = 256) -> float:
    """Simulate block reduction using sequential addressing."""
    raise NotImplementedError("Implement block_tree_reduce")


def blelloch_scan_inclusive(arr: np.ndarray) -> np.ndarray:
    """Compute inclusive parallel prefix sum."""
    raise NotImplementedError("Implement blelloch_scan_inclusive")


def blelloch_scan_exclusive(arr: np.ndarray) -> np.ndarray:
    """Compute exclusive parallel prefix sum (first element is 0)."""
    raise NotImplementedError("Implement blelloch_scan_exclusive")
