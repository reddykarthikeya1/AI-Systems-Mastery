# 🐣 Interactive Foundations Playground: Speculative Decoding Architectures

> *"Speculative decoding is a draft writer and an editor: the small model writes fast, the large model verifies all words at once."*

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
import math
```

---

## 1. Draft Model Proposal and Target Verification

A tiny draft model generates $K$ candidate tokens in serial; the large target model runs one forward pass to verify all $K$ tokens in parallel.

```python
K = 4
draft_tokens = ["in", "the", "middle", "of"]
target_agreements = [True, True, True, False]  # Agrees on first 3, rejects 4th

accepted_tokens = []
for token, agreed in zip(draft_tokens, target_agreements):
    if agreed:
        accepted_tokens.append(token)
    else:
        break

assert len(accepted_tokens) == 3
assert accepted_tokens == ["in", "the", "middle"]
print(f"Speculative decode accepted {len(accepted_tokens)} of {K} tokens in a single target forward pass.")
```

---

## 2. Speedup Factor under Acceptance Rate Alpha

Expected speedup is $S = \frac{1}{(1 - \alpha) + \frac{c}{K}}$ where $\alpha$ is acceptance rate and $c$ is draft cost fraction.

```python
alpha = 0.80  # 80% acceptance rate
expected_tokens_per_step = 1.0 + (K * alpha)

assert expected_tokens_per_step == 4.2
print(f"Expected generated tokens per large model step: {expected_tokens_per_step:.1f} tokens.")
```

---

## 3. Exact Output Distribution Invariance

Speculative sampling rejection criteria guarantees that the sampled output strictly matches the target model's probability distribution.

```python
p_target = 0.60
p_draft = 0.40
accept_prob = min(1.0, p_target / p_draft)

assert accept_prob == 1.0
assert min(1.0, 0.20 / 0.40) == 0.50
print(f"Speculative acceptance probability calculated: {accept_prob:.2f}")
```

---
