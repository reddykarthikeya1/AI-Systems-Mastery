"""Unit tests for Standardized Benchmark Harness."""

from __future__ import annotations

import pytest
from benchmark_harness_sim import BenchmarkHarness, MathBenchmarkItem


def test_extract_numeric_answer():
    text1 = "Let's think step by step. 50 + 25 = 75. #### 75"
    assert BenchmarkHarness.extract_numeric_answer(text1) == 75.0

    text2 = "Total cost is 1,250.50 dollars"
    assert BenchmarkHarness.extract_numeric_answer(text2) == 1250.50

    text3 = "No numbers here"
    assert BenchmarkHarness.extract_numeric_answer(text3) is None


def test_pass_at_k_calculation():
    # n=10, c=2, k=1
    p1 = BenchmarkHarness.compute_pass_at_k(10, 2, 1)
    assert pytest.approx(p1, 0.01) == 0.2

    # n=10, c=10 (all correct)
    p_all = BenchmarkHarness.compute_pass_at_k(10, 10, 5)
    assert p_all == 1.0


def test_ngram_contamination_detection():
    test_q = "The speed of light in vacuum is approximately 299792458 meters per second."
    clean_doc = "Physics involves studying mass, velocity, acceleration and planetary dynamics."
    dirty_doc = "According to relativity, the speed of light in vacuum is approximately 299792458 meters per second in all frames."

    assert BenchmarkHarness.check_ngram_contamination(test_q, [clean_doc], n_gram_size=6) is False
    assert BenchmarkHarness.check_ngram_contamination(test_q, [dirty_doc], n_gram_size=6) is True


def test_evaluate_math_suite():
    harness = BenchmarkHarness()
    items = [
        MathBenchmarkItem("q1", "What is 2 + 2?", 4.0),
        MathBenchmarkItem("q2", "What is 10 * 5?", 50.0),
    ]

    def mock_model(prompt: str) -> str:
        if "2 + 2" in prompt:
            return "2 + 2 is #### 4"
        return "Thinking... answer is #### 49"  # wrong

    res = harness.evaluate_math_suite(items, mock_model)
    assert res["total"] == 2
    assert res["correct"] == 1
    assert res["accuracy"] == 0.5
