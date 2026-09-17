"""Problem 01 — Checkpoint Time Travel Fork

Topic: 07 Human in the Loop and Time Travel
Target: Production-grade implementation

Fork execution history from specific checkpoint ID and discard newer turns.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def checkpoint_time_travel_fork(history: list[dict], fork_checkpoint_id: str) -> list[dict]:
    """history: list of {'checkpoint_id': str, 'state': dict}.
    Return sublist of history up to and including the fork_checkpoint_id.
    Raise KeyError("Checkpoint not found") if not present.
    """
    raise NotImplementedError("Implement checkpoint_time_travel_fork")
