from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class NIAHTestResult:
    context_length_words: int
    needle_depth_percent: float
    needle_found: bool


class ContextOptimizerNIAH:
    @staticmethod
    def reorder_context_u_shaped(ranked_docs: list[str]) -> list[str]:
        raise NotImplementedError("Implement reorder_context_u_shaped")

    @staticmethod
    def run_synthetic_niah(
        haystack_words: int,
        needle: str,
        depth_percent: float,
    ) -> tuple[str, NIAHTestResult]:
        raise NotImplementedError("Implement run_synthetic_niah")
