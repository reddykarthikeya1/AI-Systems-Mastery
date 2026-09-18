"""Problem 01 — Iteration Level Scheduler

Topic: 05 Continuous and Dynamic Batching
Target: Production-grade implementation

Schedule iteration batch admitting waiting requests up to max_tokens budget.

Example:
    >>> iteration_level_scheduler(['r1', 'r2'], [('w1', 5), ('w2', 10)], 8)
    (['r1', 'r2', 'w1'], [('w2', 10)])

Hints:
    Hint 1: Each already-running request consumes exactly one token slot per
        decode step, so the token budget starts pre-spent by
        `len(running_requests)` before you even look at the waiting queue.
    Hint 2: Walk `waiting_requests` in order with a running token counter —
        a simple loop with an append and a threshold check, no heap or
        sorting required, just first-fit admission against a shrinking
        budget.
    Hint 3: The fit check must use the UPDATED token count after each
        admission, not the original one; a request that doesn't fit does
        NOT stop the scan — later, smaller requests can still be admitted
        around it — and every rejected request lands in
        `remaining_waiting_requests` in its original relative order.
"""

from __future__ import annotations


def iteration_level_scheduler(running_requests: list[str], waiting_requests: list[tuple[str, int]], max_batch_tokens: int) -> tuple[list[str], list[tuple[str, int]]]:
    """Each running request consumes 1 token per decode step.
    Admit waiting requests (req_id, prompt_len) while (running_count + prompt_len) <= max_batch_tokens.
    Returns (new_running_ids, remaining_waiting_requests).
    """
    raise NotImplementedError("Implement iteration_level_scheduler")
