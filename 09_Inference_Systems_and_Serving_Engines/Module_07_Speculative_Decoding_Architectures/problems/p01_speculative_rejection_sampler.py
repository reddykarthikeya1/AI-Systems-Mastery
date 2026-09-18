"""Problem 01 — Speculative Rejection Sampler

Topic: 07 Speculative Decoding Architectures
Target: Production-grade implementation

Determine accepted draft tokens comparing target model and draft model probabilities.

Example:
    >>> speculative_rejection_sampler([0.8, 0.8], [0.9, 0.4], [0.5, 0.6])
    1

Hints:
    Hint 1: A draft token is accepted only if it's at least as likely under
        the target model as under the draft, and this is a strictly
        sequential process — once one token is rejected, nothing after it
        gets evaluated.
    Hint 2: Iterate the three parallel sequences together (`zip`), compute
        an acceptance ratio `min(1.0, target_probs[i] / draft_probs[i])` at
        each step, compare it against `rand_draws[i]`, and `break` on the
        first rejection.
    Hint 3: A `draft_probs[i]` of 0.0 would divide by zero, so the ratio
        must default to 1.0 (auto-accept) in that case; the ratio is also
        clamped at 1.0 even when the target assigns higher probability than
        the draft; and rejection is a hard stop, not a skip — later
        would-be-accepted tokens must not be counted once one draw fails.
"""

from __future__ import annotations


def speculative_rejection_sampler(draft_probs: list[float], target_probs: list[float], rand_draws: list[float]) -> int:
    """Evaluate accepted draft tokens in sequence:
    Accept token i if rand_draws[i] <= min(1.0, target_probs[i] / draft_probs[i]).
    First rejected token halts evaluation.
    Returns count of accepted tokens.
    """
    raise NotImplementedError("Implement speculative_rejection_sampler")
