"""Starter stub for LLM Judge Calibrator."""

from __future__ import annotations
from typing import Any, Callable


class LLMJudgeCalibrator:
    def __init__(self) -> None:
        raise NotImplementedError("LLMJudgeCalibrator is not implemented yet.")

    def evaluate_pairwise(self, query: str, response_a: str, response_b: str, judge_fn: Callable) -> Any:
        raise NotImplementedError
