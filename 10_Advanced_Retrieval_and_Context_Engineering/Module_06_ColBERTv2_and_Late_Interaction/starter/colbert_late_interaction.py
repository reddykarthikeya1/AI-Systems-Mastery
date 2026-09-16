from __future__ import annotations

import numpy as np


class ColBERTMaxSimEngine:
    @staticmethod
    def maxsim_score(query_embeddings: np.ndarray, doc_embeddings: np.ndarray) -> float:
        raise NotImplementedError("Implement maxsim_score")
