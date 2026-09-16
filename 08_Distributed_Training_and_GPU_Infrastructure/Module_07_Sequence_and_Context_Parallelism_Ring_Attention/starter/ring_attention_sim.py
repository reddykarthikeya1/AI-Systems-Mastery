from __future__ import annotations

import numpy as np


class RingAttentionSimulator:
    def __init__(self, seq_len: int, head_dim: int, num_ranks: int, causal: bool = False):
        raise NotImplementedError("Implement RingAttentionSimulator")

    def run_monolithic_reference(self, q: np.ndarray, k: np.ndarray, v: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Implement run_monolithic_reference")

    def run_ring_attention(self, q_full: np.ndarray, k_full: np.ndarray, v_full: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Implement run_ring_attention")
