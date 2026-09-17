# 🐣 Interactive Foundations Playground: RadixAttention & Prefix Caching

> *"RadixAttention is a shared prefix tree: if five users ask questions about the same document, read the document once."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from collections import defaultdict
```

---

## 1. Radix Trie Prefix Matching

A Radix tree stores token sequences along edges; incoming prompts search for the longest matching cached prefix.

```python
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
```

---

## 2. Prefill Compute Avoidance Ratio

Reusing cached KV tokens bypasses the prefill phase entirely for the matched prefix, slashing TTFT.

```python
total_prompt_tokens = len(user_query)
cached_tokens = len(matched)
prefill_savings = cached_tokens / total_prompt_tokens

assert prefill_savings == 4 / 6
assert round(prefill_savings, 2) == 0.67
print(f"Prefix cache saved {prefill_savings:.1%} of prefill compute!")
```

---

## 3. LRU Radix Node Eviction

When KV cache memory is exhausted, the least-recently used leaf nodes are pruned from the Radix tree.

```python
active_nodes = {"doc_a": 10, "doc_b": 50, "doc_c": 5}
oldest_node = min(active_nodes, key=active_nodes.get)

assert oldest_node == "doc_c"
print(f"Evicted least recently used prefix node: '{oldest_node}'")
```

---
