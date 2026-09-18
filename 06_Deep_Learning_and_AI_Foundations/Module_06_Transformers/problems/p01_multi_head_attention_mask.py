"""Problem 01 — Multi Head Attention Mask

Topic: 06 Transformers
Target: Production-grade implementation

Apply causal autoregressive upper triangular mask to attention scores.

Example:
    >>> multi_head_attention_mask([[1.0, 2.0], [3.0, 4.0]])
    [[1.0, -1000000000.0], [3.0, 4.0]]

Hints:
    Hint 1: Causal masking encodes "a token can only attend to itself and
        earlier tokens" — position (i, j) is a future token relative to i
        exactly when its column index j exceeds the row index i.
    Hint 2: Walk every (i, j) cell of the square matrix; keep `scores[i][j]`
        unchanged when `j <= i`, and overwrite it with `neg_inf` when
        `j > i` (the strict upper triangle).
    Hint 3: Use `neg_inf` (default -1e9) rather than 0 or a smaller negative
        number for masked positions — after a softmax later in the
        pipeline, a merely-small value would still leak nonzero attention
        weight onto future tokens, whereas -1e9 drives that weight to
        (numerically) zero.
"""

from __future__ import annotations


def multi_head_attention_mask(scores: list[list[float]], neg_inf: float = -1e9) -> list[list[float]]:
    """Mask positions where j > i with neg_inf.
    scores is square N x N matrix.
    Returns masked matrix.
    """
    raise NotImplementedError("Implement multi_head_attention_mask")
