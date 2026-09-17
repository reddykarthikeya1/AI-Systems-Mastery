"""Reference Solution — Problem 01: Triton Pointer Offset Math

Topic: 06 OpenAI Triton Programming Fundamentals
"""

from __future__ import annotations


def triton_pointer_offset_math(pid: int, block_size: int, n_elements: int) -> tuple[list[int], list[bool]]:
    start = pid * block_size
    offsets = [start + i for i in range(block_size)]
    masks = [o < n_elements for o in offsets]
    return (offsets, masks)
