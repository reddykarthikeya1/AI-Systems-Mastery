"""Problem 01 — Chunked Prefill Budget Split

Topic: 06 Chunked Prefill and PD Disaggregation
Target: Production-grade implementation

Split long prompt prefill tokens into chunked steps bounded by chunk_size.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def chunked_prefill_budget_split(prompt_tokens: list[int], chunk_size: int = 4) -> list[list[int]]:
    """Partition prompt_tokens into chunks of at most chunk_size."""
    raise NotImplementedError("Implement chunked_prefill_budget_split")
