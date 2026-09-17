"""Beginner playground for Module 04 - RadixAttention & Prefix Caching.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import defaultdict

# -------------------------------------------- 1. Radix Trie Prefix Matching
class RadixTrie:
    def __init__(self):
        self.root = {}
    def insert(self, tokens):
        node = self.root
        for t in tokens:
            node = node.setdefault(t, {})
        node['#'] = True
    def match_prefix(self, tokens):
        node = self.root
        matched = []
        for t in tokens:
            if t not in node:
                break
            matched.append(t)
            node = node[t]
        return matched

trie = RadixTrie()
system_prompt = [101, 202, 303, 404]
trie.insert(system_prompt)

user_query = [101, 202, 303, 404, 505, 606]
matched = trie.match_prefix(user_query)

assert matched == system_prompt
assert len(matched) == 4
print(f"Matched {len(matched)} cached prefix tokens: {matched}")

# -------------------------------------------- 2. Prefill Compute Avoidance Ratio
total_prompt_tokens = len(user_query)
cached_tokens = len(matched)
prefill_savings = cached_tokens / total_prompt_tokens

assert prefill_savings == 4 / 6
assert round(prefill_savings, 2) == 0.67
print(f"Prefix cache saved {prefill_savings:.1%} of prefill compute!")

# -------------------------------------------- 3. LRU Radix Node Eviction
active_nodes = {"doc_a": 10, "doc_b": 50, "doc_c": 5}
oldest_node = min(active_nodes, key=active_nodes.get)

assert oldest_node == "doc_c"
print(f"Evicted least recently used prefix node: '{oldest_node}'")

print()
print("All checks passed.")
