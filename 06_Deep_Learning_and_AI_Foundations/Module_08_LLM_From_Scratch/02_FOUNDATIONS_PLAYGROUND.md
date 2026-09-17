# 🐣 Interactive Foundations Playground: LLM from Scratch & Tokenization

> *"An LLM is an advanced next-token prediction engine: it repeatedly answers 'what word comes next?'."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from collections import Counter
```

---

## 1. Byte-Pair Encoding (BPE) Pair Counting

BPE iteratively finds the most frequent pair of consecutive symbols and replaces them with a single new symbol.

```python
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
```

---

## 2. Causal Autoregressive Masking

Causal masking zeros out (or sets to $-\infty$) attention weights to future token positions to ensure generative autoregression.

```python
seq_len = 3
causal_mask = [[1 if col <= row else 0 for col in range(seq_len)] for row in range(seq_len)]

assert causal_mask[0] == [1, 0, 0], "Token 0 can only attend to Token 0"
assert causal_mask[1] == [1, 1, 0], "Token 1 can attend to Token 0 and 1"
assert causal_mask[2] == [1, 1, 1], "Token 2 can attend to all previous tokens"
print(f"Causal lower-triangular mask generated: {causal_mask}")
```

---

## 3. Greedy Token Generation Loop

At each decoding step, take $\text{argmax}$ over vocabulary logits and append the predicted token id to context.

```python
vocab = {0: "<pad>", 1: "The", 2: "cat", 3: "sat"}
logits_step1 = [0.1, 0.8, 0.05, 0.05]
next_token_id = logits_step1.index(max(logits_step1))

assert next_token_id == 1
assert vocab[next_token_id] == "The"
print(f"Greedy decode selected: token {next_token_id} ('{vocab[next_token_id]}')")
```

---
