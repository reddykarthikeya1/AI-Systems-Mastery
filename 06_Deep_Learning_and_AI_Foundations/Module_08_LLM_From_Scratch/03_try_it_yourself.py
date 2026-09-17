"""Beginner playground for Module 08 - LLM from Scratch & Tokenization.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import Counter

# -------------------------------------------- 1. Byte-Pair Encoding (BPE) Pair Counting
corpus = ["l o w </w>", "l o w e r </w>", "n e w e s t </w>", "w i d e s t </w>"]
pairs = Counter()
for word in corpus:
    tokens = word.split()
    for i in range(len(tokens) - 1):
        pairs[(tokens[i], tokens[i+1])] += 1

most_common_pair, count = pairs.most_common(1)[0]
assert count >= 2
assert isinstance(most_common_pair, tuple)
print(f"Most frequent consecutive token pair: {most_common_pair} (frequency: {count})")

# -------------------------------------------- 2. Causal Autoregressive Masking
seq_len = 3
causal_mask = [[1 if col <= row else 0 for col in range(seq_len)] for row in range(seq_len)]

assert causal_mask[0] == [1, 0, 0], "Token 0 can only attend to Token 0"
assert causal_mask[1] == [1, 1, 0], "Token 1 can attend to Token 0 and 1"
assert causal_mask[2] == [1, 1, 1], "Token 2 can attend to all previous tokens"
print(f"Causal lower-triangular mask generated: {causal_mask}")

# -------------------------------------------- 3. Greedy Token Generation Loop
vocab = {0: "<pad>", 1: "The", 2: "cat", 3: "sat"}
logits_step1 = [0.1, 0.8, 0.05, 0.05]
next_token_id = logits_step1.index(max(logits_step1))

assert next_token_id == 1
assert vocab[next_token_id] == "The"
print(f"Greedy decode selected: token {next_token_id} ('{vocab[next_token_id]}')")

print()
print("All checks passed.")
