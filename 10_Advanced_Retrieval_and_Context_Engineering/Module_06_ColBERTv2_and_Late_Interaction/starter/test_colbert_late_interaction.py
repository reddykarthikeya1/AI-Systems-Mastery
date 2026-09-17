from __future__ import annotations

import numpy as np
from colbert_late_interaction import ColBERTMaxSimEngine


def test_colbert_maxsim_identical_vectors():
    # Query with 3 tokens of dim 4
    q = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], dtype=np.float32)
    # Document contains exact matches for all 3 tokens plus extra tokens
    d = np.array([[0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], dtype=np.float32)

    score = ColBERTMaxSimEngine.maxsim_score(q, d)
    # Each query token should achieve max similarity 1.0 -> total sum = 3.0
    assert abs(score - 3.0) < 1e-3


def test_colbert_maxsim_orthogonal_vectors():
    q = np.array([[1, 0, 0, 0]], dtype=np.float32)
    d = np.array([[0, 1, 0, 0], [0, 0, 1, 0]], dtype=np.float32)

    score = ColBERTMaxSimEngine.maxsim_score(q, d)
    # Orthogonal vectors have dot product 0.0
    assert abs(score - 0.0) < 1e-3
