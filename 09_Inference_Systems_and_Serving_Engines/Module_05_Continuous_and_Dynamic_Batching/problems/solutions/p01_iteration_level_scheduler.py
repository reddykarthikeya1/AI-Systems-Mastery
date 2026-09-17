"""Reference Solution — Problem 01: Iteration Level Scheduler

Topic: 05 Continuous and Dynamic Batching
"""

from __future__ import annotations


def iteration_level_scheduler(running_requests: list[str], waiting_requests: list[tuple[str, int]], max_batch_tokens: int) -> tuple[list[str], list[tuple[str, int]]]:
    current_running = list(running_requests)
    rem_waiting = []
    used_tokens = len(current_running)
    for req_id, p_len in waiting_requests:
        if used_tokens + p_len <= max_batch_tokens:
            current_running.append(req_id)
            used_tokens += p_len
        else:
            rem_waiting.append((req_id, p_len))
    return (current_running, rem_waiting)
