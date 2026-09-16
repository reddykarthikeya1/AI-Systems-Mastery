from __future__ import annotations


class RadixTreeKVCache:
    def __init__(self, max_cached_blocks: int = 100):
        raise NotImplementedError("Implement RadixTreeKVCache")

    def match_prefix(self, tokens: list[int]) -> tuple[int, list[int]]:
        raise NotImplementedError("Implement match_prefix")

    def insert(self, tokens: list[int], block_ids: list[int]) -> None:
        raise NotImplementedError("Implement insert")
