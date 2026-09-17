# 🐣 Interactive Foundations Playground: Reasoning Under Uncertainty

> *"Probability is quantifying what you do not know until observation collapses the distribution."*

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

## 1. Sample Space and Probability Axioms

Probabilities are non-negative real numbers whose sum across all mutually exclusive outcomes in the sample space equals exactly 1.0.

```python
sample_space = {"heads": 0.5, "tails": 0.5}
assert sum(sample_space.values()) == 1.0
assert all(0.0 <= p <= 1.0 for p in sample_space.values())
print(f"Valid probability distribution over {list(sample_space.keys())}")
```

---

## 2. Conditional Probability and Bayes' Theorem

Bayes' Theorem updates the prior probability of hypothesis $H$ given observed evidence $E$: $P(H|E) = \frac{P(E|H) P(H)}{P(E)}$.

```python
p_disease = 0.01          # Prior P(D)
p_pos_given_disease = 0.95 # Sensitivity P(+|D)
p_pos_given_healthy = 0.05 # False positive rate P(+|H)

p_healthy = 1.0 - p_disease
p_pos = p_pos_given_disease * p_disease + p_pos_given_healthy * p_healthy
p_disease_given_pos = (p_pos_given_disease * p_disease) / p_pos

assert 0.15 < p_disease_given_pos < 0.20
assert p_disease_given_pos > p_disease, "Posterior must exceed prior on positive test"
print(f"Prior: {p_disease:.1%}, Posterior given positive test: {p_disease_given_pos:.1%}")
```

---

## 3. Independence of Random Variables

Two events $A$ and $B$ are statistically independent if and only if $P(A \cap B) = P(A) \cdot P(B)$.

```python
p_a = 0.4
p_b = 0.5
p_a_and_b = 0.2

is_independent = abs(p_a_and_b - (p_a * p_b)) < 1e-6
assert is_independent is True
assert (p_a * p_b) == 0.2
print(f"Events A and B are independent: P(A)*P(B) = {p_a * p_b} == P(A and B) = {p_a_and_b}")
```

---
