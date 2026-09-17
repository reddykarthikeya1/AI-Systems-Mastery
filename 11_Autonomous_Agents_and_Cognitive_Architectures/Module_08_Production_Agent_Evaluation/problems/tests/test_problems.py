"""Tests for Trajectory Accuracy Evaluator."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_trajectory_accuracy_evaluator import trajectory_accuracy_evaluator
except ImportError:
    from p01_trajectory_accuracy_evaluator import trajectory_accuracy_evaluator


def test_trajectory_accuracy_evaluator():
    agent = ["search", "scrape", "summarize"]
    golden = ["search", "scrape", "summarize"]
    assert trajectory_accuracy_evaluator(agent, golden) == 1.0
    agent_err = ["search", "summarize"]
    assert trajectory_accuracy_evaluator(agent_err, golden) < 1.0
