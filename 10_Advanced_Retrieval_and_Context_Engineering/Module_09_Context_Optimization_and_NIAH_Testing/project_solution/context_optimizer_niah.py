from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class NIAHTestResult:
    context_length_words: int
    needle_depth_percent: float
    needle_found: bool


class ContextOptimizerNIAH:
    """Simulates U-shaped context reordering and Needle-in-a-Haystack testing."""

    @staticmethod
    def reorder_context_u_shaped(ranked_docs: list[str]) -> list[str]:
        """Places top-ranked documents at the beginning and end, weakest in middle."""
        if len(ranked_docs) <= 2:
            return ranked_docs

        # Reorder: [doc_2, doc_4, ..., doc_3, doc_1]
        left_side = []
        right_side = []

        for idx, doc in enumerate(ranked_docs):
            if idx % 2 == 0:
                # 0, 2, 4 -> right side (appended in reverse at end)
                right_side.append(doc)
            else:
                # 1, 3, 5 -> left side
                left_side.append(doc)

        right_side.reverse()
        return left_side + right_side

    @staticmethod
    def run_synthetic_niah(
        haystack_words: int,
        needle: str,
        depth_percent: float,
    ) -> tuple[str, NIAHTestResult]:
        """Generates a synthetic haystack and inserts a needle at depth_percent."""
        total_words = ["word"] * haystack_words
        insert_idx = int((depth_percent / 100.0) * haystack_words)
        insert_idx = min(insert_idx, len(total_words))

        total_words.insert(insert_idx, needle)
        haystack_text = " ".join(total_words)

        found = needle in haystack_text
        result = NIAHTestResult(
            context_length_words=len(total_words),
            needle_depth_percent=depth_percent,
            needle_found=found,
        )
        return haystack_text, result
