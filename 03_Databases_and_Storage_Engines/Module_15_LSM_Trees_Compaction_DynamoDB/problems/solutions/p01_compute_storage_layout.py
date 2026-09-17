"""Reference Solution — Problem 01: compute_storage_layout

Topic: LSM Trees Compaction DynamoDB
"""

from __future__ import annotations

def compute_storage_layout(record_sizes: list[int], block_size: int = 4096) -> list[tuple[int, int]]:
    layout = []
    current_block = 0
    current_offset = 0
    for size in record_sizes:
        if current_offset + size > block_size:
            current_block += 1
            current_offset = 0
        layout.append((current_block, current_offset))
        current_offset += size
    return layout

