"""Problem 01 — Iteration Level Scheduler

Topic: 05 Continuous and Dynamic Batching
Target: Production-grade implementation

Schedule iteration batch admitting waiting requests up to max_tokens budget.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def iteration_level_scheduler(running_requests: list[str], waiting_requests: list[tuple[str, int]], max_batch_tokens: int) -> tuple[list[str], list[tuple[str, int]]]:
    """Each running request consumes 1 token per decode step.
    Admit waiting requests (req_id, prompt_len) while (running_count + prompt_len) <= max_batch_tokens.
    Returns (new_running_ids, remaining_waiting_requests).
    """
    raise NotImplementedError("Implement iteration_level_scheduler")
