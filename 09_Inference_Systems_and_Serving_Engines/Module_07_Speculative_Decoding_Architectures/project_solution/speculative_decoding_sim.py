from __future__ import annotations

import dataclasses
import numpy as np


@dataclasses.dataclass
class SpeculativeResult:
    accepted_tokens: list[int]
    total_accepted: int
    acceptance_rate: float
    theoretical_speedup: float


class SpeculativeDecodingSimulator:
    """Simulates Speculative Decoding token generation and rejection sampling."""

    @staticmethod
    def rejection_sample_step(
        draft_tokens: list[int],
        p_target_probs: list[float],
        q_draft_probs: list[float],
        target_cost_ms: float = 30.0,
        draft_cost_ms: float = 3.0,
    ) -> SpeculativeResult:
        gamma = len(draft_tokens)
        accepted = []

        for i in range(gamma):
            p = p_target_probs[i]
            q = q_draft_probs[i]
            # Acceptance probability: min(1, p / q)
            alpha = min(1.0, p / max(q, 1e-9))
            roll = np.random.rand()
            if roll < alpha:
                accepted.append(draft_tokens[i])
            else:
                # Token rejected, stop checking subsequent tokens
                break

        total_accepted = len(accepted) + 1  # +1 for target bonus token
        acc_rate = len(accepted) / gamma if gamma > 0 else 0.0

        # Speedup formula: (total_accepted * target_cost) / (gamma * draft_cost + target_cost)
        total_time = (gamma * draft_cost_ms) + target_cost_ms
        standard_time = total_accepted * target_cost_ms
        speedup = standard_time / total_time

        return SpeculativeResult(
            accepted_tokens=accepted,
            total_accepted=total_accepted,
            acceptance_rate=round(acc_rate, 2),
            theoretical_speedup=round(speedup, 2),
        )
