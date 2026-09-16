from __future__ import annotations

import numpy as np
from speculative_decoding_sim import SpeculativeDecodingSimulator


def test_speculative_full_acceptance():
    np.random.seed(42)
    # Draft probabilities match target probabilities (alpha = 1.0)
    draft_toks = [101, 102, 103, 104]
    p_probs = [0.8, 0.9, 0.7, 0.85]
    q_probs = [0.8, 0.9, 0.7, 0.85]

    res = SpeculativeDecodingSimulator.rejection_sample_step(
        draft_tokens=draft_toks,
        p_target_probs=p_probs,
        q_draft_probs=q_probs,
        target_cost_ms=30.0,
        draft_cost_ms=3.0,
    )
    # All 4 draft tokens accepted + 1 bonus = 5 tokens
    assert res.total_accepted == 5
    assert res.acceptance_rate == 1.0
    assert res.theoretical_speedup > 3.0


def test_speculative_early_rejection():
    # First token has very low target probability -> immediate reject
    draft_toks = [101, 102, 103]
    p_probs = [0.0001, 0.9, 0.9]
    q_probs = [0.9, 0.9, 0.9]

    res = SpeculativeDecodingSimulator.rejection_sample_step(
        draft_tokens=draft_toks,
        p_target_probs=p_probs,
        q_draft_probs=q_probs,
    )
    # Token 1 rejected -> 0 draft accepted + 1 target bonus token = 1
    assert res.total_accepted == 1
    assert len(res.accepted_tokens) == 0
