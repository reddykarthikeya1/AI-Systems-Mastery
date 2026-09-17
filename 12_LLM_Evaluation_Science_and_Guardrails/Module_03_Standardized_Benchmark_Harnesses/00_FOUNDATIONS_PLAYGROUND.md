# 🐣 Interactive Foundations Playground: Standardized Benchmark Harnesses

> *"Standardized benchmarks (MMLU, GSM8K, HumanEval) provide reproducible scoreboards for AI capability."*

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

## 1. Few-Shot Prompt Construction

Structuring standardized prompts with $k$ static exemplar demonstrations followed by the target test question.

```python
exemplars = [
    {"q": "What is 2+2?", "a": "4"},
    {"q": "What is 3+5?", "a": "8"}
]
test_q = "What is 7+4?"
prompt = ""
for ex in exemplars:
    prompt += f"Q: {ex['q']}\nA: {ex['a']}\n\n"
prompt += f"Q: {test_q}\nA:"

assert "2+2" in prompt
assert "7+4" in prompt
assert prompt.endswith("A:")
print(f"Standard 2-shot benchmark prompt assembled:\n{prompt}")
```

---

## 2. Multiple-Choice Log-Likelihood Evaluation

Instead of freeform text parsing, evaluate log-probability of answer tokens ('A', 'B', 'C', 'D') directly.

```python
log_probs = {"A": -1.2, "B": -0.3, "C": -2.5, "D": -3.1}
best_choice = max(log_probs, key=log_probs.get)

assert best_choice == "B"
assert log_probs[best_choice] == -0.3
print(f"Highest probability choice selected: Option {best_choice}")
```

---

## 3. Pass@K Metric Math (HumanEval)

Pass@K computes the probability that at least one of $k$ generated code samples passes unit tests: $1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}$.

```python
n = 10  # 10 samples generated
c = 3   # 3 correct samples
# Pass@1 = c / n
pass_at_1 = c / n
assert pass_at_1 == 0.30
print(f"HumanEval Pass@1: {pass_at_1:.1%}")
```

---
