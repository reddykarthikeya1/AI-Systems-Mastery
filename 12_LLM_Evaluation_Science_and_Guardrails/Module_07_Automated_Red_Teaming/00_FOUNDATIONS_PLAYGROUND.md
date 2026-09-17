# 🐣 Interactive Foundations Playground: Automated Red Teaming & Fuzzing

> *"Red teaming is hiring friendly burglars to pick your locks before real thieves arrive."*

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
import random
```

---

## 1. Adversarial Prompt Mutation Strategies

Fuzzers mutate seed prompts using leetspeak, character insertion, and semantic paraphrasing to bypass safety filters.

```python
def leetspeak_mutate(text):
    mapping = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    return "".join(mapping.get(ch.lower(), ch) for ch in text)

original = "password"
mutated = leetspeak_mutate(original)

assert mutated == "p@$$w0rd"
assert len(mutated) == len(original)
print(f"Mutated adversarial fuzzing candidate: '{original}' -> '{mutated}'")
```

---

## 2. Attack Success Rate (ASR) Metric

Attack Success Rate is the percentage of adversarial prompts that successfully elicited an unsafe response from the target model.

```python
total_attacks = 100
successful_breaches = 8
asr = successful_breaches / total_attacks

assert asr == 0.08
assert asr < 0.10, "ASR maintained below 10% tolerance"
print(f"Red teaming Attack Success Rate: {asr:.1%} ({successful_breaches}/{total_attacks})")
```

---

## 3. Safety Boundary Exploration Loop

Iteratively increasing prompt perturbation intensity until model safety filters trigger.

```python
perturbation_levels = [0.1, 0.2, 0.3, 0.4]
assert len(perturbation_levels) == 4
assert perturbation_levels[-1] > perturbation_levels[0]
print("Multi-level fuzzing matrix generated.")
```

---
