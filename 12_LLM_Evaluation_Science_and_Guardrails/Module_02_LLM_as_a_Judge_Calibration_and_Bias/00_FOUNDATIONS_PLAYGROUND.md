# 🐣 Interactive Foundations Playground: LLM as a Judge Calibration & Bias

> *"When using an LLM to grade another LLM, watch out for position bias, verbosity bias, and self-enhancement bias."*

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

## 1. Position Bias Detection via Order Swapping

Testing whether judge LLM always prefers Candidate A over Candidate B regardless of quality by swapping presentation order.

```python
# Swap inputs: score(A, B) vs score(B, A)
trial1_winner = "Candidate A"  # Model 1 was in position A
trial2_winner = "Candidate A"  # Model 2 was in position A

position_bias_detected = (trial1_winner == "Candidate A" and trial2_winner == "Candidate A")
assert position_bias_detected is True, "Judge always votes for position A regardless of content"
print("Position bias confirmed: order swapping detected primacy effect.")
```

---

## 2. Verbosity Bias Length Normalization

Judges favor longer answers even when padded with fluff; length normalization penalizes excessive verbosity.

```python
raw_score = 9.0
word_count = 600
target_length = 200

length_penalty = max(0.0, (word_count - target_length) * 0.005)
calibrated_score = raw_score - length_penalty

assert length_penalty == 2.0
assert calibrated_score == 7.0
print(f"Calibrated score: {calibrated_score} (down from raw {raw_score} after length penalty)")
```

---

## 3. Cohen's Kappa Inter-Rater Agreement

Cohen's Kappa measures agreement between LLM Judge and Human ground truth while accounting for chance agreement.

```python
p_observed = 0.85
p_chance = 0.50
kappa = (p_observed - p_chance) / (1.0 - p_chance)

assert kappa == 0.70
assert kappa > 0.60, "Substantial agreement"
print(f"Inter-rater agreement Cohen's Kappa: {kappa:.2f}")
```

---
