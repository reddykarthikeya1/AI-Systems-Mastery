"""Problem 01 — Wal Checkpoint Merge

Topic: 03 Embedded Databases SQLite WAL
Target: Production-grade implementation

Replay WAL frames into database pages keeping latest committed page version.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def wal_checkpoint_merge(db_pages: dict[int, bytes], wal_frames: list[tuple[int, int, bytes, bool]]) -> dict[int, bytes]:
    """Replay WAL frames: list of (frame_id, page_no, content, is_commit).
    Only committed transactions are merged into db_pages.
    Returns updated db_pages.
    """
    raise NotImplementedError("Implement wal_checkpoint_merge")
