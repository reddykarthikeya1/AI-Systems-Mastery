from __future__ import annotations

import dataclasses
import time


@dataclasses.dataclass
class RadixNode:
    tokens: tuple[int, ...]
    block_ids: list[int]
    children: dict[int, RadixNode] = dataclasses.field(default_factory=dict)
    ref_count: int = 0
    last_accessed: float = dataclasses.field(default_factory=time.time)


class RadixTreeKVCache:
    """Simulates SGLang RadixAttention Trie-based hierarchical prefix caching."""

    def __init__(self, max_cached_blocks: int = 100):
        self.root = RadixNode(tokens=(), block_ids=[])
        self.max_cached_blocks = max_cached_blocks
        self.total_allocated_blocks = 0
        self.next_block_id = 1

    def match_prefix(self, tokens: list[int]) -> tuple[int, list[int]]:
        """Finds longest matching token prefix in tree. Returns (matched_token_count, cached_block_ids)."""
        curr = self.root
        matched_tokens = 0
        cached_blocks = []
        token_idx = 0

        while token_idx < len(tokens):
            lead_tok = tokens[token_idx]
            if lead_tok not in curr.children:
                break
            child = curr.children[lead_tok]
            child.last_accessed = time.time()

            # Check how many tokens match in child.tokens
            child_toks = child.tokens
            match_len = 0
            while (
                match_len < len(child_toks)
                and (token_idx + match_len) < len(tokens)
                and child_toks[match_len] == tokens[token_idx + match_len]
            ):
                match_len += 1

            if match_len == len(child_toks):
                # Full child match
                matched_tokens += match_len
                cached_blocks.extend(child.block_ids)
                token_idx += match_len
                curr = child
            else:
                # Partial match inside child edge
                matched_tokens += match_len
                token_idx += match_len
                break

        return matched_tokens, cached_blocks

    def insert(self, tokens: list[int], block_ids: list[int]) -> None:
        """Inserts a verified sequence into the Radix Tree."""
        if not tokens:
            return
        lead_tok = tokens[0]
        if lead_tok not in self.root.children:
            self.root.children[lead_tok] = RadixNode(
                tokens=tuple(tokens),
                block_ids=list(block_ids),
            )
            self.total_allocated_blocks += len(block_ids)
        else:
            # Overwrite or append child
            child = self.root.children[lead_tok]
            child.tokens = tuple(tokens)
            child.block_ids = list(block_ids)
            child.last_accessed = time.time()
