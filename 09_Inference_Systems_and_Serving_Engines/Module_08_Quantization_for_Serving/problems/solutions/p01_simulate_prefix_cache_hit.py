"""Reference Solution — Problem 01: simulate_prefix_cache_hit

Topic: Quantization for Serving
"""

from __future__ import annotations

def simulate_prefix_cache_hit(cached_prompts: list[list[int]], incoming_prompt: list[int]) -> int:
    max_prefix_len = 0
    for cached in cached_prompts:
        match_len = 0
        for t_c, t_in in zip(cached, incoming_prompt):
            if t_c == t_in:
                match_len += 1
            else:
                break
        if match_len > max_prefix_len:
            max_prefix_len = match_len
    return max_prefix_len

