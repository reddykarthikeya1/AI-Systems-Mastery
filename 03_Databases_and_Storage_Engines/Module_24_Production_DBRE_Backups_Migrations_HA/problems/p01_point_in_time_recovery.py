"""Problem 01 — Point In Time Recovery

Topic: 24 Production DBRE Backups Migrations HA
Target: Production-grade implementation

Apply base snapshot and replay WAL logs up to target recovery timestamp.

Example:
    >>> base = {'k1': 'v1_initial', 'k2': 'v2_initial'}
    >>> wal = [
    ...     (100, 'k1', 'v1_updated'),
    ...     (200, 'k2', 'v2_updated'),
    ...     (300, 'k1', 'v1_corrupted'),
    ... ]
    >>> point_in_time_recovery(base, wal, target_ts=250)
    {'k1': 'v1_updated', 'k2': 'v2_updated'}

Hints:
    Hint 1: PITR is a timeline cutoff, not a filter on which keys changed —
        you replay history up to a moment in time and simply stop there,
        as if later WAL entries never happened.
    Hint 2: Start from a copy of base_snapshot (don't mutate the caller's
        dict) and apply wal_stream entries in order with a plain dict
        assignment, state[key] = val, for each entry whose timestamp
        qualifies.
    Hint 3: The cutoff is inclusive (ts <= target_ts, so an entry exactly at
        target_ts still applies) and any entry with a later timestamp — like
        the corrupting write at ts=300 above — must be skipped entirely,
        leaving the last qualifying value for that key in place.
"""

from __future__ import annotations


def point_in_time_recovery(base_snapshot: dict[str, str], wal_stream: list[tuple[int, str, str]], target_ts: int) -> dict[str, str]:
    """wal_stream has entries: (timestamp, key, val).
    Replay WAL entries from wal_stream onto base_snapshot up to and including target_ts.
    Returns recovered state dict.
    """
    raise NotImplementedError("Implement point_in_time_recovery")
