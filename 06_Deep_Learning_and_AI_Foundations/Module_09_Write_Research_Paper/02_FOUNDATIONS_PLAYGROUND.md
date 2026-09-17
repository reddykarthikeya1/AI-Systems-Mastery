# 🐣 Interactive Foundations Playground: Research Paper Implementation & Metrics

> *"Good empirical research demands reproducible baselines and statistically grounded metrics."*

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
import math
```

---

## 1. Precision, Recall, and F1 Score

Accuracy can be deceptive on imbalanced datasets; F1 harmonizes precision $\frac{TP}{TP+FP}$ and recall $\frac{TP}{TP+FN}$.

```python
tp, fp, fn = 80, 20, 10
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * (precision * recall) / (precision + recall)

assert precision == 0.8
assert abs(recall - 80 / 90) < 1e-6
assert 0.8 < f1 < 0.9
print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.4f}")
```

---

## 2. BLEU Score N-gram Precision

BLEU measures how many candidate n-grams appear in the human reference translation.

```python
candidate = "the cat sat on the mat".split()
reference = "the cat is on the mat".split()

cand_bigrams = [tuple(candidate[i:i+2]) for i in range(len(candidate)-1)]
ref_bigrams = set(tuple(reference[i:i+2]) for i in range(len(reference)-1))

matches = sum(1 for bg in cand_bigrams if bg in ref_bigrams)
p2 = matches / len(cand_bigrams)

assert len(cand_bigrams) == 5
assert matches == 3  # ('the', 'cat'), ('on', 'the'), ('the', 'mat')
assert p2 == 0.6
print(f"Bigram precision: {p2:.2f} ({matches}/{len(cand_bigrams)})")
```

---

## 3. Perplexity Calculation from Cross-Entropy

Perplexity measures the effective branching factor: $\text{PPL} = \exp(\text{Loss})$. Lower is better.

```python
cross_entropy_loss = 1.386  # ln(4)
perplexity = math.exp(cross_entropy_loss)

assert abs(perplexity - 4.0) < 0.01
assert perplexity > 1.0
print(f"Cross-entropy {cross_entropy_loss} corresponds to perplexity ~{perplexity:.2f}")
```

---
