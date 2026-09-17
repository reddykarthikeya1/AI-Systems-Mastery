"""Reference Solution — Problem 01: Point In Time Recovery

Topic: 24 Production DBRE Backups Migrations HA
"""

from __future__ import annotations


def point_in_time_recovery(base_snapshot: dict[str, str], wal_stream: list[tuple[int, str, str]], target_ts: int) -> dict[str, str]:
    state = dict(base_snapshot)
    for ts, k, v in wal_stream:
        if ts <= target_ts:
            state[k] = v
    return state
