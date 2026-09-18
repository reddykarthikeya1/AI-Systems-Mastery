"""Problem 01 — Bucket Gradient Allreduce

Topic: 03 Distributed Data Parallel DDP
Target: Production-grade implementation

Partition parameter gradients into fixed-capacity buckets for overlapping AllReduce.

Example:
    >>> bucket_gradient_allreduce([10.0, 15.0, 20.0, 10.0], 25.0)
    [[3], [2], [1, 0]]

Hints:
    Hint 1: Gradients become ready in reverse parameter order during the
        backward pass, so buckets must be filled starting from the *last*
        parameter index and working back toward index 0, not forward.
    Hint 2: Walk indices from `len(param_sizes_mb) - 1` down to `0`, greedily
        appending each one to the current bucket while tracking its running
        size; when adding the next one would exceed `bucket_cap_mb`, close
        the current bucket and start a fresh one.
    Hint 3: A bucket is only closed once it's non-empty and the *next*
        item would overflow it — a single parameter larger than
        `bucket_cap_mb` still gets its own bucket rather than being
        rejected. Don't forget to flush the final in-progress bucket after
        the loop ends.
"""

from __future__ import annotations


def bucket_gradient_allreduce(param_sizes_mb: list[float], bucket_cap_mb: float = 25.0) -> list[list[int]]:
    """Group parameter indices (0..len-1) into buckets of capacity at most bucket_cap_mb.
    Indices are added in reverse order (backward pass executes from last layer to first).
    Returns list of bucket lists containing parameter indices.
    """
    raise NotImplementedError("Implement bucket_gradient_allreduce")
