"""Problem 01 — Triton Pointer Offset Math

Topic: 06 OpenAI Triton Programming Fundamentals
Target: Production-grade implementation

Compute linear pointer offsets and boundary mask for Triton block kernel.

Example:
    >>> triton_pointer_offset_math(1, 4, 6)
    ([4, 5, 6, 7], [True, True, False, False])

Hints:
    Hint 1: Each program instance (`pid`) owns one contiguous block of
        `block_size` elements; its offsets are just that block's starting
        position plus a local index within the block.
    Hint 2: Compute `start = pid * block_size`, build offsets as `start +
        i` for `i` in `range(block_size)`, then derive the mask elementwise
        by comparing each offset against `n_elements`.
    Hint 3: The last block usually overruns the array — offsets can exceed
        `n_elements - 1`, and it's the mask (`offset < n_elements`), not the
        offsets list itself, that must reflect which lanes are in bounds.
"""

from __future__ import annotations


def triton_pointer_offset_math(pid: int, block_size: int, n_elements: int) -> tuple[list[int], list[bool]]:
    """pid: program ID.
    offsets = pid * block_size + range(block_size).
    mask = [offset < n_elements for offset in offsets].
    Returns (list_of_offsets, list_of_masks).
    """
    raise NotImplementedError("Implement triton_pointer_offset_math")
