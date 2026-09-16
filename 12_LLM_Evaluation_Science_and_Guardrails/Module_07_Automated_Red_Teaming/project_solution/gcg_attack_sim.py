"""Greedy Coordinate Gradient (GCG) White-Box Adversarial Suffix Attack Simulator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List


@dataclass
class GCGStepRecord:
    step: int
    current_suffix: str
    loss: float


class GCGAttackSimulator:
    """Simulates GCG token substitution gradient descent to bypass safety filters."""

    CANDIDATE_TOKENS = ["!", "===", "please", "hypothetically", "override", "root", "dev_mode", "bypass"]

    def __init__(self, target_loss_threshold: float = 0.20) -> None:
        self.target_loss_threshold = target_loss_threshold

    def optimize_suffix(
        self,
        base_prompt: str,
        loss_fn: Callable[[str], float],
        max_steps: int = 15,
    ) -> tuple[str, List[GCGStepRecord]]:
        """Greedy coordinate search iterating over token substitutions."""
        suffix_tokens = ["===", "dev_mode", "!"]
        history = []

        for step in range(max_steps):
            curr_suffix = " ".join(suffix_tokens)
            full_prompt = f"{base_prompt} {curr_suffix}"
            loss = loss_fn(full_prompt)
            history.append(GCGStepRecord(step=step, current_suffix=curr_suffix, loss=loss))

            if loss <= self.target_loss_threshold:
                return curr_suffix, history

            best_idx = 0
            best_tok = suffix_tokens[0]
            best_loss = loss

            for i in range(len(suffix_tokens)):
                for candidate in self.CANDIDATE_TOKENS:
                    cand_tokens = list(suffix_tokens)
                    cand_tokens[i] = candidate
                    cand_loss = loss_fn(f"{base_prompt} {' '.join(cand_tokens)}")
                    if cand_loss < best_loss:
                        best_loss = cand_loss
                        best_idx = i
                        best_tok = candidate

            suffix_tokens[best_idx] = best_tok

        return " ".join(suffix_tokens), history
