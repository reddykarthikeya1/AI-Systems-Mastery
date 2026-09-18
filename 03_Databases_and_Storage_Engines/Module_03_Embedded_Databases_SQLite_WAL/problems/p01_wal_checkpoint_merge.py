"""Problem 01 — Wal Checkpoint Merge

Topic: 03 Embedded Databases SQLite WAL
Target: Production-grade implementation

Replay WAL frames into database pages keeping latest committed page version.

Example:
    >>> pages = {1: b"page1_v0", 2: b"page2_v0"}
    >>> frames = [
    ...     (1, 1, b"page1_v1", False),
    ...     (2, 2, b"page2_v1", True),
    ...     (3, 1, b"page1_uncommitted", False),
    ... ]
    >>> wal_checkpoint_merge(pages, frames)
    {1: b'page1_v1', 2: b'page2_v1'}

Hints:
    Hint 1: Frames don't apply to the database directly — they belong to a
        transaction, and only a transaction that reaches its commit frame
        is allowed to change what a reader sees.
    Hint 2: Accumulate writes from the frames seen so far into a pending
        buffer (a dict keyed by page_no); only fold that buffer into the
        result pages, and clear it, when a frame's is_commit flag is True.
    Hint 3: Any frames left pending after the loop ends belong to a
        transaction that never committed and must be discarded entirely —
        even though they touch pages that already exist in db_pages.
"""

from __future__ import annotations


def wal_checkpoint_merge(db_pages: dict[int, bytes], wal_frames: list[tuple[int, int, bytes, bool]]) -> dict[int, bytes]:
    """Replay WAL frames: list of (frame_id, page_no, content, is_commit).
    Only committed transactions are merged into db_pages.
    Returns updated db_pages.
    """
    raise NotImplementedError("Implement wal_checkpoint_merge")
