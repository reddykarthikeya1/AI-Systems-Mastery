"""Problem 01 — Beam Search Decoder

Topic: 12 Bonus Lessons
Target: Production-grade implementation

Top-k beam search tracking highest likelihood token hypotheses.

Example:
    >>> beam_search_decoder([([1], -0.5)], [[-1.0, -0.1, -2.0]], beam_width=2)
    [([1, 1], -0.6), ([1, 0], -1.5)]

Hints:
    Hint 1: Beam search only ever keeps a bounded number of the most
        promising hypotheses alive at once — every candidate is expanded
        first, and pruning to survive happens only afterward.
    Hint 2: For every existing `(seq, score)` candidate, branch it once per
        vocabulary token by appending that token's id to `seq` and adding
        its log-probability to `score` (log-probs sum, unlike raw
        probabilities which would multiply), then sort all the expanded
        hypotheses by score.
    Hint 3: Log-probabilities are negative, and "highest likelihood" means
        the score CLOSEST TO ZERO — sort in descending order (largest,
        i.e. least negative, first), not ascending, then truncate to the
        top `beam_width` entries. Round each cumulative score to 4
        decimal places as you build it.
"""

from __future__ import annotations


def beam_search_decoder(initial_candidates: list[tuple[list[int], float]], vocab_logprobs: list[list[float]], beam_width: int = 2) -> list[tuple[list[int], float]]:
    """For one decoding step, expand each candidate sequence by all tokens in vocab_logprobs[0].
    Score is cumulative logprob sum.
    Prune to top `beam_width` highest scoring sequences.
    Returns list of (token_sequence, cumulative_score).
    """
    raise NotImplementedError("Implement beam_search_decoder")
