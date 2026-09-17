"""Problem 01 — Atomic File Write Commit

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def atomic_commit_payload(staging_dir: dict, target_file: str, payload: str) -> bool:
    tmp_key = f"{target_file}.tmp"
    staging_dir[tmp_key] = payload
    # atomic rename
    staging_dir[target_file] = staging_dir.pop(tmp_key)
    return True
