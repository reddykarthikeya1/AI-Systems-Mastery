"""Problem 01 — Slotted Page Insert

Topic: 01 Storage Theory ACID Relational Model
Target: Production-grade implementation

Insert record bytes into a slotted page. Returns page dict with 'slots' and 'free_space'.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def slotted_page_insert(page: dict, record_bytes: bytes) -> int:
    """Insert record bytes into a 4KB slotted page.
    
    Page layout:
    - page['capacity']: int (e.g. 4096)
    - page['slots']: list of (offset, length)
    - page['free_offset']: pointer where tuple storage grows upwards from bottom
    
    Returns slot index, or -1 if insufficient space (needs record_length + 8 bytes for slot).
    """
    raise NotImplementedError("Implement slotted_page_insert")
