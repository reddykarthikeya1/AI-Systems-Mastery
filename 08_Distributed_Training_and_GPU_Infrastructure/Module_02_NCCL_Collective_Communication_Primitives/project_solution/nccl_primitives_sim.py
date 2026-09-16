"""Production reference implementation for NCCL Collectives Simulator."""
from __future__ import annotations

import numpy as np


def ring_allreduce(tensors: list[np.ndarray]) -> tuple[list[np.ndarray], int]:
    """Execute Ring AllReduce simulation across N rank tensors.

    Each tensor has size S.
    Phase 1: Scatter-Reduce (N-1 steps)
    Phase 2: AllGather (N-1 steps)
    Returns:
        tuple of (reduced_tensors, total_bytes_sent_per_rank).
    """
    num_ranks = len(tensors)
    if num_ranks < 1:
        raise ValueError("Must have at least 1 rank.")

    shape = tensors[0].shape

    for t in tensors:
        if t.shape != shape:
            raise ValueError("All rank tensors must have identical shape.")

    flat_tensors = [t.ravel().copy() for t in tensors]
    s = flat_tensors[0].size

    # Split into N chunks
    chunk_size = (s + num_ranks - 1) // num_ranks
    padded_len = chunk_size * num_ranks

    padded = [np.pad(ft, (0, padded_len - s), mode="constant") for ft in flat_tensors]

    # chunks[rank][chunk_id]
    chunks = [[p[c * chunk_size : (c + 1) * chunk_size].copy() for c in range(num_ranks)] for p in padded]

    # Phase 1: Scatter-Reduce
    for step in range(num_ranks - 1):
        for rank in range(num_ranks):
            send_chunk_idx = (rank - step) % num_ranks
            recv_rank = (rank + 1) % num_ranks
            chunks[recv_rank][send_chunk_idx] += chunks[rank][send_chunk_idx]

    # Phase 2: AllGather
    for step in range(num_ranks - 1):
        for rank in range(num_ranks):
            send_chunk_idx = (rank - step + 1) % num_ranks
            recv_rank = (rank + 1) % num_ranks
            chunks[recv_rank][send_chunk_idx] = chunks[rank][send_chunk_idx].copy()

    # Reconstruct outputs
    outputs = []
    for rank in range(num_ranks):
        flat_res = np.concatenate(chunks[rank])[:s].reshape(shape)
        outputs.append(flat_res)

    bytes_per_chunk = chunk_size * tensors[0].itemsize
    total_bytes_sent = 2 * (num_ranks - 1) * bytes_per_chunk

    return outputs, total_bytes_sent


def ring_reducescatter(tensors: list[np.ndarray]) -> list[np.ndarray]:
    """Execute ReduceScatter: rank i receives reduced chunk i."""
    reduced_full, _ = ring_allreduce(tensors)
    num_ranks = len(tensors)
    out_chunks = []
    chunk_size = (tensors[0].size + num_ranks - 1) // num_ranks
    for rank in range(num_ranks):
        start = rank * chunk_size
        end = min(start + chunk_size, tensors[0].size)
        out_chunks.append(reduced_full[rank].ravel()[start:end])
    return out_chunks


def ring_allgather(chunks: list[np.ndarray]) -> list[np.ndarray]:
    """Execute AllGather: concatenates chunks across all ranks."""
    concat = np.concatenate(chunks)
    return [concat.copy() for _ in range(len(chunks))]


def alpha_beta_cost_model(
    size_bytes: int,
    num_ranks: int,
    alpha_latency_s: float = 1e-6,
    beta_inv_bw: float = 2e-11,
) -> float:
    """Calculate Ring AllReduce transfer time using (alpha, beta) model.

    T = 2 * (N - 1) * alpha + 2 * ((N - 1) / N) * S * beta.
    """
    if num_ranks <= 1:
        return 0.0
    latency_term = 2.0 * (num_ranks - 1) * alpha_latency_s
    bandwidth_term = 2.0 * ((num_ranks - 1) / float(num_ranks)) * size_bytes * beta_inv_bw
    return latency_term + bandwidth_term
