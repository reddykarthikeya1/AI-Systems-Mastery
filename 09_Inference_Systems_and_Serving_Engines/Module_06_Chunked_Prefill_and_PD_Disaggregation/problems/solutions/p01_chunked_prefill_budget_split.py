"""Reference Solution — Problem 01: Chunked Prefill Budget Split

Topic: 06 Chunked Prefill and PD Disaggregation
"""

from __future__ import annotations


def chunked_prefill_budget_split(prompt_tokens: list[int], chunk_size: int = 4) -> list[list[int]]:
    if not prompt_tokens:
        return []
    return [prompt_tokens[i:i + chunk_size] for i in range(0, len(prompt_tokens), chunk_size)]
