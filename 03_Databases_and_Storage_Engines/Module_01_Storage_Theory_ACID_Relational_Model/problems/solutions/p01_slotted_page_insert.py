"""Reference Solution — Problem 01: Slotted Page Insert

Topic: 01 Storage Theory ACID Relational Model
"""

from __future__ import annotations


def slotted_page_insert(page: dict, record_bytes: bytes) -> int:
    rec_len = len(record_bytes)
    slot_overhead = 8  # 4 bytes offset, 4 bytes length
    available = page['free_offset'] - (len(page['slots']) * slot_overhead)
    if available < rec_len + slot_overhead:
        return -1
    new_free_offset = page['free_offset'] - rec_len
    page['free_offset'] = new_free_offset
    slot_idx = len(page['slots'])
    page['slots'].append((new_free_offset, rec_len))
    return slot_idx
