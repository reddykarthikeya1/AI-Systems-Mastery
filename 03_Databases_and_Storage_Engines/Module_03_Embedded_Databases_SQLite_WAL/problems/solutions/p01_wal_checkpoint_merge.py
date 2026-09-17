"""Reference Solution — Problem 01: Wal Checkpoint Merge

Topic: 03 Embedded Databases SQLite WAL
"""

from __future__ import annotations


def wal_checkpoint_merge(db_pages: dict[int, bytes], wal_frames: list[tuple[int, int, bytes, bool]]) -> dict[int, bytes]:
    res = dict(db_pages)
    pending = {}
    for frame_id, page_no, content, is_commit in wal_frames:
        pending[page_no] = content
        if is_commit:
            res.update(pending)
            pending = {}
    return res
