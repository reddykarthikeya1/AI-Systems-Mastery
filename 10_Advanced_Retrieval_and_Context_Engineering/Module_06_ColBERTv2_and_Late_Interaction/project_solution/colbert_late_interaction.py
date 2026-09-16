from __future__ import annotations

import numpy as np


class ColBERTMaxSimEngine:
    """Simulates ColBERT Late Interaction token-level MaxSim scoring."""

    @staticmethod
    def maxsim_score(query_embeddings: np.ndarray, doc_embeddings: np.ndarray) -> float:
        """Computes S(Q, D) = sum_i(max_j(E_q[i] . E_d[j]^T)).

        query_embeddings: (Q_tokens, dim)
        doc_embeddings: (D_tokens, dim)
        """
        # Normalize vectors to unit length
        q_norm = query_embeddings / (np.linalg.norm(query_embeddings, axis=-1, keepdims=True) + 1e-9)
        d_norm = doc_embeddings / (np.linalg.norm(doc_embeddings, axis=-1, keepdims=True) + 1e-9)

        # Cross-token similarity matrix: (Q, D)
        sim_matrix = np.matmul(q_norm, d_norm.T)

        # For each query token, take maximum similarity across all doc tokens
        max_per_query_token = np.max(sim_matrix, axis=1)

        # Sum of maximum similarities
        total_score = float(np.sum(max_per_query_token))
        return round(total_score, 4)
