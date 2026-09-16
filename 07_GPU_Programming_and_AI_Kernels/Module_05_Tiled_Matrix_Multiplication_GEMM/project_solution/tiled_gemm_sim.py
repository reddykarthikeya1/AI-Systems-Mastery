"""Production reference implementation for Tiled GEMM Simulator."""
from __future__ import annotations

import numpy as np


def calculate_gemm_arithmetic_intensity(
    m: int, n: int, k: int, tile_size: int, elem_bytes: int = 4
) -> tuple[float, float]:
    """Calculate arithmetic intensity for naive vs tiled GEMM.

    Total FLOPs = 2 * M * N * K.
    Naive memory traffic = (M * N * K * 2 + M * N) * elem_bytes.
    Tiled memory traffic = ((M * K * (N / tile_size)) + (K * N * (M / tile_size)) + M * N) * elem_bytes.
    Returns:
        tuple of (naive_intensity, tiled_intensity).
    """
    total_flops = 2.0 * m * n * k

    # Naive reads: Each element of C reads row of A (length K) and col of B (length K)
    naive_bytes = (2.0 * m * n * k + m * n) * elem_bytes
    naive_intensity = total_flops / naive_bytes

    # Tiled reads: Each tile is read (N / tile_size) or (M / tile_size) times
    tiled_bytes = (m * k * (n / float(tile_size)) + k * n * (m / float(tile_size)) + m * n) * elem_bytes
    tiled_intensity = total_flops / tiled_bytes

    return naive_intensity, tiled_intensity


def tiled_gemm_2d(
    a: np.ndarray, b: np.ndarray, tile_size: int = 16
) -> tuple[np.ndarray, int, int]:
    """Simulate 2D tiled GEMM, tracking global and shared memory reads.

    C = A @ B.
    A has shape (M, K), B has shape (K, N), C has shape (M, N).
    Simulates block tiling where each block loads (tile_size x tile_size) chunks of A and B
    into shared memory, syncs, and computes partial dot products.

    Returns:
        tuple of (c_matrix, global_memory_reads, shared_memory_reads).
    """
    if a.ndim != 2 or b.ndim != 2 or a.shape[1] != b.shape[0]:
        raise ValueError("Incompatible matrix shapes for multiplication.")

    m, k = a.shape
    _, n = b.shape

    c = np.zeros((m, n), dtype=np.float64)

    # Pad to multiples of tile_size
    pad_m = (tile_size - (m % tile_size)) % tile_size
    pad_k = (tile_size - (k % tile_size)) % tile_size
    pad_n = (tile_size - (n % tile_size)) % tile_size

    a_padded = np.pad(a, ((0, pad_m), (0, pad_k)), mode="constant")
    b_padded = np.pad(b, ((0, pad_k), (0, pad_n)), mode="constant")

    pm, pk = a_padded.shape
    _, pn = b_padded.shape

    num_tiles_m = pm // tile_size
    num_tiles_n = pn // tile_size
    num_phases = pk // tile_size

    global_reads = 0
    shared_reads = 0

    # Iterate over thread blocks
    for bm in range(num_tiles_m):
        for bn in range(num_tiles_n):
            accum = np.zeros((tile_size, tile_size), dtype=np.float64)

            # Phase loop across K
            for phase in range(num_phases):
                # 1. Global memory -> Shared Memory load
                s_a = a_padded[bm * tile_size : (bm + 1) * tile_size, phase * tile_size : (phase + 1) * tile_size]
                s_b = b_padded[phase * tile_size : (phase + 1) * tile_size, bn * tile_size : (bn + 1) * tile_size]
                global_reads += s_a.size + s_b.size

                # 2. Compute in Shared Memory (each thread accesses tile_size elements)
                for tx in range(tile_size):
                    for ty in range(tile_size):
                        dot_val = np.dot(s_a[ty, :], s_b[:, tx])
                        accum[ty, tx] += dot_val
                        shared_reads += 2 * tile_size

            # Store result back
            r_start, r_end = bm * tile_size, min((bm + 1) * tile_size, m)
            c_start, c_end = bn * tile_size, min((bn + 1) * tile_size, n)
            valid_h = r_end - r_start
            valid_w = c_end - c_start
            if valid_h > 0 and valid_w > 0:
                c[r_start:r_end, c_start:c_end] = accum[:valid_h, :valid_w]

    return c, global_reads, shared_reads
