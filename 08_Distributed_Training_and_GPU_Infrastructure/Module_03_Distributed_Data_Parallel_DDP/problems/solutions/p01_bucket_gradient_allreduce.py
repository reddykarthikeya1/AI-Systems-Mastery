"""Reference Solution — Problem 01: Bucket Gradient Allreduce

Topic: 03 Distributed Data Parallel DDP
"""

from __future__ import annotations


def bucket_gradient_allreduce(param_sizes_mb: list[float], bucket_cap_mb: float = 25.0) -> list[list[int]]:
    n = len(param_sizes_mb)
    buckets = []
    curr_bucket = []
    curr_size = 0.0
    for i in range(n - 1, -1, -1):
        sz = param_sizes_mb[i]
        if curr_bucket and curr_size + sz > bucket_cap_mb:
            buckets.append(curr_bucket)
            curr_bucket = [i]
            curr_size = sz
        else:
            curr_bucket.append(i)
            curr_size += sz
    if curr_bucket:
        buckets.append(curr_bucket)
    return buckets
