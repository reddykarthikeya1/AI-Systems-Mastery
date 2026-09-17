"""Problem 01 — Triton Pointer Offset Math

Topic: 06 OpenAI Triton Programming Fundamentals
Target: Production-grade implementation

Compute linear pointer offsets and boundary mask for Triton block kernel.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def triton_pointer_offset_math(pid: int, block_size: int, n_elements: int) -> tuple[list[int], list[bool]]:
    """pid: program ID.
    offsets = pid * block_size + range(block_size).
    mask = [offset < n_elements for offset in offsets].
    Returns (list_of_offsets, list_of_masks).
    """
    raise NotImplementedError("Implement triton_pointer_offset_math")
