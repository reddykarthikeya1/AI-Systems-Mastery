"""Production reference implementation for FlashAttention Engine."""
from __future__ import annotations

import numpy as np


def flash_attention_forward(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    block_r: int = 16,
    block_c: int = 16,
) -> tuple[np.ndarray, int, int]:
    """Execute IO-aware FlashAttention forward algorithm (Tri Dao et al.).

    Given Q, K, V in R^{N x d}:
    Computes O = softmax(Q @ K.T / sqrt(d)) @ V
    without materializing the N x N attention matrix in global memory (HBM).

    Tiling parameters:
    - block_r: block size for Q and O (rows)
    - block_c: block size for K and V (columns)

    Returns:
        tuple of (O, hbm_reads, hbm_writes).
    """
    if q.ndim != 2 or k.ndim != 2 or v.ndim != 2:
        raise ValueError("Q, K, V must be 2D matrices (N, d).")

    n, d = q.shape
    if k.shape != (n, d) or v.shape != (n, d):
        raise ValueError("Q, K, V must have identical (N, d) dimensions.")

    scale = 1.0 / np.sqrt(d)
    out = np.zeros((n, d), dtype=np.float64)

    # Running statistics per query row: running max m and running normalizer l
    # Initialize m to -infinity and l to 0
    m = np.full(n, -1e9, dtype=np.float64)
    l_sum = np.zeros(n, dtype=np.float64)

    tr = (n + block_r - 1) // block_r
    tc = (n + block_c - 1) // block_c

    hbm_reads = 0
    hbm_writes = 0

    # FlashAttention-2 style: outer loop over Q blocks, inner loop over K, V blocks
    for i in range(tr):
        r_start = i * block_r
        r_end = min(r_start + block_r, n)
        curr_br = r_end - r_start

        # Load Qi from HBM into SRAM
        q_i = q[r_start:r_end]
        hbm_reads += q_i.size

        # Accumulator for Oi in SRAM/registers
        o_i = np.zeros((curr_br, d), dtype=np.float64)
        m_i = m[r_start:r_end].copy()
        l_i = l_sum[r_start:r_end].copy()

        for j in range(tc):
            c_start = j * block_c
            c_end = min(c_start + block_c, n)

            # Load Kj, Vj from HBM into SRAM
            k_j = k[c_start:c_end]
            v_j = v[c_start:c_end]
            hbm_reads += k_j.size + v_j.size

            # Compute block attention scores: S_ij = Q_i @ K_j.T * scale (in SRAM)
            s_ij = (q_i @ k_j.T) * scale

            # Online Softmax update for block
            m_ij = np.max(s_ij, axis=1)  # max across columns
            m_new = np.maximum(m_i, m_ij)

            # Rescale factors
            alpha = np.exp(m_i - m_new)  # (curr_br,)
            p_ij = np.exp(s_ij - m_new[:, None])  # (curr_br, curr_bc)

            # Update normalizer l_i
            l_new = l_i * alpha + np.sum(p_ij, axis=1)

            # Update output accumulator O_i
            # O_i = diag(alpha) * O_i + P_ij @ V_j
            o_i = o_i * alpha[:, None] + (p_ij @ v_j)

            m_i = m_new
            l_i = l_new

        # Final normalization for block i: O_i = O_i / l_i
        o_i = o_i / l_i[:, None]
        out[r_start:r_end] = o_i
        hbm_writes += o_i.size

    return out, hbm_reads, hbm_writes
