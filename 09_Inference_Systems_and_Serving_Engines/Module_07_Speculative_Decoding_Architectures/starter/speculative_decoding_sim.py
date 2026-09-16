from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class SpeculativeResult:
    accepted_tokens: list[int]
    total_accepted: int
    acceptance_rate: float
    theoretical_speedup: float


class SpeculativeDecodingSimulator:
    @staticmethod
    def rejection_sample_step(
        draft_tokens: list[int],
        p_target_probs: list[float],
        q_draft_probs: list[float],
        target_cost_ms: float = 30.0,
        draft_cost_ms: float = 3.0,
    ) -> SpeculativeResult:
        raise NotImplementedError("Implement rejection_sample_step")
