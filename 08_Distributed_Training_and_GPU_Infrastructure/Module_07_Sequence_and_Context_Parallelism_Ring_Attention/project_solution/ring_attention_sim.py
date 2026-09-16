from __future__ import annotations

import numpy as np


class RingAttentionSimulator:
    """Simulates exact Ring Attention with Online Softmax accumulation across N context ranks."""

    def __init__(self, seq_len: int, head_dim: int, num_ranks: int, causal: bool = False):
        if seq_len % num_ranks != 0:
            raise ValueError(f"seq_len ({seq_len}) must be divisible by num_ranks ({num_ranks})")
        self.seq_len = seq_len
        self.d = head_dim
        self.num_ranks = num_ranks
        self.causal = causal
        self.chunk_size = seq_len // num_ranks

    def run_monolithic_reference(self, q: np.ndarray, k: np.ndarray, v: np.ndarray) -> np.ndarray:
        """Reference single-device Attention: softmax(Q @ K.T / sqrt(d)) @ V."""
        scale = 1.0 / np.sqrt(self.d)
        scores = np.matmul(q, k.T) * scale

        if self.causal:
            mask = np.triu(np.ones((self.seq_len, self.seq_len), dtype=bool), k=1)
            scores[mask] = -1e9

        max_scores = np.max(scores, axis=-1, keepdims=True)
        exp_scores = np.exp(scores - max_scores)
        attn_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
        return np.matmul(attn_weights, v)

    def run_ring_attention(self, q_full: np.ndarray, k_full: np.ndarray, v_full: np.ndarray) -> np.ndarray:
        """Simulates Ring Attention across ranks with online softmax tracking."""
        c = self.chunk_size
        scale = 1.0 / np.sqrt(self.d)

        # Slice Q, K, V across ranks
        q_chunks = [q_full[r * c : (r + 1) * c] for r in range(self.num_ranks)]
        k_chunks = [k_full[r * c : (r + 1) * c] for r in range(self.num_ranks)]
        v_chunks = [v_full[r * c : (r + 1) * c] for r in range(self.num_ranks)]

        # Initialize online softmax statistics per rank
        # m: running max, l: running sum of exp, out: running accumulator
        m_list = [np.full((c, 1), -1e9, dtype=np.float32) for _ in range(self.num_ranks)]
        l_list = [np.zeros((c, 1), dtype=np.float32) for _ in range(self.num_ranks)]
        out_list = [np.zeros((c, self.d), dtype=np.float32) for _ in range(self.num_ranks)]

        # Ring steps
        for step in range(self.num_ranks):
            for r in range(self.num_ranks):
                # Partner key-value index for rank r at this step
                kv_idx = (r - step) % self.num_ranks

                if self.causal and kv_idx > r:
                    # Future block in causal attention: entirely masked out
                    continue

                q_local = q_chunks[r]
                k_curr = k_chunks[kv_idx]
                v_curr = v_chunks[kv_idx]

                scores = np.matmul(q_local, k_curr.T) * scale

                if self.causal and kv_idx == r:
                    # Diagonal block: apply causal upper triangular mask
                    diag_mask = np.triu(np.ones((c, c), dtype=bool), k=1)
                    scores[diag_mask] = -1e9

                # Online softmax update
                s_max = np.max(scores, axis=-1, keepdims=True)
                m_new = np.maximum(m_list[r], s_max)

                p_curr = np.exp(scores - m_new)
                alpha = np.exp(m_list[r] - m_new)

                l_new = alpha * l_list[r] + np.sum(p_curr, axis=-1, keepdims=True)
                out_new = alpha * out_list[r] + np.matmul(p_curr, v_curr)

                m_list[r] = m_new
                l_list[r] = l_new
                out_list[r] = out_new

        # Final normalization
        final_chunks = []
        for r in range(self.num_ranks):
            final_chunks.append(out_list[r] / l_list[r])

        return np.concatenate(final_chunks, axis=0)
