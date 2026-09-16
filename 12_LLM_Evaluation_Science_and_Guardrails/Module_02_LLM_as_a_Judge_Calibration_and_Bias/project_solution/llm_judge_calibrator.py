"""LLM Judge Calibration Engine with Swap-Pair Debiasing and Agreement Metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List


@dataclass
class PairwiseResult:
    winner: str  # "MODEL_A", "MODEL_B", or "TIE"
    margin: float
    forward_winner: str
    swapped_winner: str
    bias_detected: bool


class LLMJudgeCalibrator:
    """Calibrates LLM Judge outputs against positional and verbosity biases."""

    def __init__(self, verbosity_penalty_ratio: float = 1.5) -> None:
        self.verbosity_penalty_ratio = verbosity_penalty_ratio

    def evaluate_pairwise(
        self,
        query: str,
        response_a: str,
        response_b: str,
        judge_fn: Callable[[str, str, str], str],
    ) -> PairwiseResult:
        """Executes swap-pair evaluation to eliminate position bias.
        judge_fn(query, candidate_1, candidate_2) returns 'FIRST' or 'SECOND'.
        """
        # Forward trial: response_a is FIRST, response_b is SECOND
        res_forward = judge_fn(query, response_a, response_b).strip().upper()
        # Swapped trial: response_b is FIRST, response_a is SECOND
        res_swapped = judge_fn(query, response_b, response_a).strip().upper()

        winner_fwd = "MODEL_A" if "FIRST" in res_forward else "MODEL_B"
        # In swapped trial: FIRST is model_b, SECOND is model_a
        winner_swap = "MODEL_B" if "FIRST" in res_swapped else "MODEL_A"

        if winner_fwd == winner_swap:
            final_winner = winner_fwd
            bias_detected = False
        else:
            final_winner = "TIE"
            bias_detected = True

        return PairwiseResult(
            winner=final_winner,
            margin=1.0 if final_winner != "TIE" else 0.0,
            forward_winner=winner_fwd,
            swapped_winner=winner_swap,
            bias_detected=bias_detected,
        )

    def compute_cohens_kappa(self, labels_1: List[str], labels_2: List[str]) -> float:
        """Computes Cohen's Kappa coefficient between two annotators/judges."""
        if len(labels_1) != len(labels_2) or not labels_1:
            return 0.0

        n = len(labels_1)
        categories = list(set(labels_1).union(set(labels_2)))

        # Observed agreement
        observed_agreements = sum(1 for a, b in zip(labels_1, labels_2) if a == b)
        po = observed_agreements / n

        # Chance agreement
        pe = 0.0
        for cat in categories:
            p1 = sum(1 for x in labels_1 if x == cat) / n
            p2 = sum(1 for x in labels_2 if x == cat) / n
            pe += p1 * p2

        if pe == 1.0:
            return 1.0

        kappa = (po - pe) / (1.0 - pe)
        return kappa
