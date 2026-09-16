"""Starter template for NCCL Collectives Simulator."""
from __future__ import annotations

import numpy as np


def ring_allreduce(tensors: list[np.ndarray]) -> tuple[list[np.ndarray], int]:
    """Execute Ring AllReduce simulation across N rank tensors."""
    raise NotImplementedError("Implement ring_allreduce")


def ring_reducescatter(tensors: list[np.ndarray]) -> list[np.ndarray]:
    """Execute ReduceScatter: rank i receives reduced chunk i."""
    raise NotImplementedError("Implement ring_reducescatter")


def ring_allgather(chunks: list[np.ndarray]) -> list[np.ndarray]:
    """Execute AllGather: concatenates chunks across all ranks."""
    raise NotImplementedError("Implement ring_allgather")


def alpha_beta_cost_model(
    size_bytes: int,
    num_ranks: int,
    alpha_latency_s: float = 1e-6,
    beta_inv_bw: float = 2e-11,
) -> float:
    """Calculate Ring AllReduce transfer time using (alpha, beta) model."""
    raise NotImplementedError("Implement alpha_beta_cost_model")
