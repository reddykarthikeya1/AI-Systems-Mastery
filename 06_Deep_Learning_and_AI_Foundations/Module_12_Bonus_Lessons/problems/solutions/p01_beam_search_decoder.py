"""Reference Solution — Problem 01: Beam Search Decoder

Topic: 12 Bonus Lessons
"""

from __future__ import annotations


def beam_search_decoder(initial_candidates: list[tuple[list[int], float]], vocab_logprobs: list[list[float]], beam_width: int = 2) -> list[tuple[list[int], float]]:
    expanded = []
    probs = vocab_logprobs[0] if vocab_logprobs else []
    for seq, score in initial_candidates:
        for token_id, lp in enumerate(probs):
            expanded.append((seq + [token_id], round(score + lp, 4)))
    expanded.sort(key=lambda x: x[1], reverse=True)
    return expanded[:beam_width]
