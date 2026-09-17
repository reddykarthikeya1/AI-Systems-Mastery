"""Reference Solution — Problem 01: Lsm Leveled Compaction

Topic: 15 LSM Trees Compaction DynamoDB
"""

from __future__ import annotations


def lsm_leveled_compaction(sstable_runs: list[list[tuple[str, str | None, int]]]) -> list[tuple[str, str]]:
    latest = {}
    for run in sstable_runs:
        for k, v, ts in run:
            if k not in latest or ts > latest[k][1]:
                latest[k] = (v, ts)
    res = []
    for k in sorted(latest.keys()):
        val, _ = latest[k]
        if val is not None:
            res.append((k, val))
    return res
