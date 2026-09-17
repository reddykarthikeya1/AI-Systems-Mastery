"""Unit tests for LLM Judge Calibrator."""

from __future__ import annotations

import pytest
from llm_judge_calibrator import LLMJudgeCalibrator


@pytest.fixture
def calibrator() -> LLMJudgeCalibrator:
    return LLMJudgeCalibrator()


def test_consistent_winner_no_bias(calibrator: LLMJudgeCalibrator):
    # Judge consistently prefers Model A (whether presented 1st or 2nd)
    def unbiased_judge(query: str, c1: str, c2: str) -> str:
        return "FIRST" if c1 == "Superior Answer" else "SECOND"

    res = calibrator.evaluate_pairwise("Q", "Superior Answer", "Inferior Answer", unbiased_judge)
    assert res.winner == "MODEL_A"
    assert res.bias_detected is False


def test_position_bias_neutralized_to_tie(calibrator: LLMJudgeCalibrator):
    # Judge ALWAYS prefers the FIRST candidate regardless of text
    def position_biased_judge(query: str, c1: str, c2: str) -> str:
        return "FIRST"

    res = calibrator.evaluate_pairwise("Q", "Answer X", "Answer Y", position_biased_judge)
    assert res.winner == "TIE"
    assert res.bias_detected is True
    assert res.forward_winner == "MODEL_A"
    assert res.swapped_winner == "MODEL_B"


def test_cohens_kappa_perfect_agreement(calibrator: LLMJudgeCalibrator):
    h = ["A", "B", "A", "TIE", "B"]
    j = ["A", "B", "A", "TIE", "B"]
    kappa = calibrator.compute_cohens_kappa(h, j)
    assert pytest.approx(kappa, 0.01) == 1.0


def test_cohens_kappa_partial_agreement(calibrator: LLMJudgeCalibrator):
    h = ["A", "A", "B", "B"]
    j = ["A", "B", "B", "B"]
    kappa = calibrator.compute_cohens_kappa(h, j)
    assert 0.0 < kappa < 1.0
