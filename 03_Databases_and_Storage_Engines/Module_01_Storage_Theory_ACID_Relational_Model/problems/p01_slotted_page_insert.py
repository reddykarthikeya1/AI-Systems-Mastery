"""Problem 01 — Slotted Page Insert

Topic: 01 Storage Theory ACID Relational Model
Target: Production-grade implementation

Insert record bytes into a slotted page. Returns page dict with 'slots' and 'free_space'.

Example:
    >>> page = {'capacity': 100, 'slots': [], 'free_offset': 100}
    >>> slotted_page_insert(page, b'hello')
    0
    >>> page
    {'capacity': 100, 'slots': [(95, 5)], 'free_offset': 95}

Hints:
    Hint 1: The page grows from both ends at once: the slot directory grows
        forward from the front while record bytes grow backward from
        free_offset, so free space is whatever is left between them.
    Hint 2: Track free space as free_offset minus the space already claimed
        by existing slot entries (8 bytes each: 4 for offset, 4 for length),
        then append the new (offset, length) tuple to the slots list.
    Hint 3: A candidate insert needs room for the record bytes AND the new
        8-byte slot entry itself; if that check fails, return -1 without
        mutating page['slots'] or page['free_offset'] at all.
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
