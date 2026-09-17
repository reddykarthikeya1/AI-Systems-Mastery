"""Reference Solution — Problem 01: Checkpoint Time Travel Fork

Topic: 07 Human in the Loop and Time Travel
"""

from __future__ import annotations


def checkpoint_time_travel_fork(history: list[dict], fork_checkpoint_id: str) -> list[dict]:
    idx = -1
    for i, item in enumerate(history):
        if item.get('checkpoint_id') == fork_checkpoint_id:
            idx = i
            break
    if idx == -1:
        raise KeyError("Checkpoint not found")
    return list(history[:idx + 1])
