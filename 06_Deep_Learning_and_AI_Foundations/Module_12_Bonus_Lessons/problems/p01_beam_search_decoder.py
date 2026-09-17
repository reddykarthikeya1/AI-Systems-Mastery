"""Problem 01 — Beam Search Decoder

Topic: 12 Bonus Lessons
Target: Production-grade implementation

Top-k beam search tracking highest likelihood token hypotheses.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def beam_search_decoder(initial_candidates: list[tuple[list[int], float]], vocab_logprobs: list[list[float]], beam_width: int = 2) -> list[tuple[list[int], float]]:
    """For one decoding step, expand each candidate sequence by all tokens in vocab_logprobs[0].
    Score is cumulative logprob sum.
    Prune to top `beam_width` highest scoring sequences.
    Returns list of (token_sequence, cumulative_score).
    """
    raise NotImplementedError("Implement beam_search_decoder")
