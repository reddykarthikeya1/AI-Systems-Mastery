"""Problem 01 — Checkpoint Time Travel Fork

Topic: 07 Human in the Loop and Time Travel
Target: Production-grade implementation

Fork execution history from specific checkpoint ID and discard newer turns.

Example:
    >>> hist = [{'checkpoint_id': 'cp1', 'state': {'turn': 1}}, {'checkpoint_id': 'cp2', 'state': {'turn': 2}}, {'checkpoint_id': 'cp3', 'state': {'turn': 3}}]
    >>> checkpoint_time_travel_fork(hist, 'cp2')
    [{'checkpoint_id': 'cp1', 'state': {'turn': 1}}, {'checkpoint_id': 'cp2', 'state': {'turn': 2}}]

Hints:
    Hint 1: "Forking" here just means truncating — find the position you
        forked from and cut everything after it, keeping that checkpoint
        itself as the new last entry.
    Hint 2: Scan history for the entry whose 'checkpoint_id' matches
        fork_checkpoint_id, note its index, and slice history up to and
        including that index.
    Hint 3: If no entry matches fork_checkpoint_id, raise
        KeyError("Checkpoint not found") rather than returning an empty
        list or None — and if the id could appear more than once, stop at
        the first match found scanning front-to-back.
"""

from __future__ import annotations


def checkpoint_time_travel_fork(history: list[dict], fork_checkpoint_id: str) -> list[dict]:
    """history: list of {'checkpoint_id': str, 'state': dict}.
    Return sublist of history up to and including the fork_checkpoint_id.
    Raise KeyError("Checkpoint not found") if not present.
    """
    raise NotImplementedError("Implement checkpoint_time_travel_fork")
