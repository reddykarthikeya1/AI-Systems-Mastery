# 🐣 Interactive Foundations Playground: LLM Evaluation Science & Metrics

> *"If you cannot measure model performance quantitatively, you are flying an aircraft blind in a storm."*

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

## 1. Exact Match (EM) Binary Metric

Exact Match scores 1.0 if normalized prediction text matches normalized reference text character-for-character, else 0.0.

```python
def exact_match(pred, ref):
    return 1.0 if pred.strip().lower() == ref.strip().lower() else 0.0

assert exact_match("Paris", "paris") == 1.0
assert exact_match("Paris.", "paris") == 0.0
assert exact_match("Rome", "Paris") == 0.0
print("Exact match evaluation metric confirmed.")
```

---

## 2. ROUGE-L Longest Common Subsequence Metric

ROUGE-L measures sentence-level structure by computing longest common subsequence overlap between prediction and reference.

```python
def lcs_len(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = 1 + dp[i-1][j-1] if s1[i-1] == s2[j-1] else max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

pred_tokens = ["the", "quick", "brown", "fox"]
ref_tokens = ["the", "fast", "brown", "fox"]
lcs = lcs_len(pred_tokens, ref_tokens)
rouge_l_recall = lcs / len(ref_tokens)

assert lcs == 3  # "the", "brown", "fox"
assert rouge_l_recall == 0.75
print(f"ROUGE-L Recall: {rouge_l_recall:.2%}")
```

---

## 3. Token Perplexity from Cross-Entropy Loss

Perplexity computes geometric branching factor: $\text{PPL} = \exp\left(\frac{1}{N} \sum -\log P(w_i)\right)$.

```python
neg_log_probs = [0.5, 0.8, 0.2, 1.1]
mean_loss = sum(neg_log_probs) / len(neg_log_probs)
ppl = math.exp(mean_loss)

assert abs(mean_loss - 0.65) < 1e-6
assert ppl > 1.0
print(f"Evaluation Perplexity: {ppl:.2f} (from mean loss {mean_loss:.2f})")
```

---
