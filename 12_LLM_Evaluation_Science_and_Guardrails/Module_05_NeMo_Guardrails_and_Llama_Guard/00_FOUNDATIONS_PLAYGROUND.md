# 🐣 Interactive Foundations Playground: NeMo Guardrails & Llama Guard

> *"Llama Guard is an LLM trained solely on trust and safety guidelines to act as an automated moderator."*

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
import json
```

---

## 1. Safety Category Classification

Llama Guard maps violations to standard hazard codes (S1: Violent Crimes, S2: Non-Violent Crimes, S3: Sex Crimes, etc.).

```python
categories = {
    "S1": "Violent Crimes",
    "S2": "Non-Violent Crimes",
    "S3": "Sex-Related Crimes",
    "S4": "Child Exploitation",
    "S5": "Defamation"
}
assert len(categories) == 5
assert categories["S1"] == "Violent Crimes"
print(f"Safety taxonomy mapped {len(categories)} hazard categories.")
```

---

## 2. Colang Flow Control Simulation

NeMo Guardrails uses Colang to define programmable conversation flows that steer the bot away from off-topic subjects.

```python
def colang_guard(user_intent):
    if user_intent == "ask_about_competitor":
        return "I can only discuss our company's product features."
    return "proceed"

action = colang_guard("ask_about_competitor")
assert action.startswith("I can only discuss")
assert colang_guard("ask_pricing") == "proceed"
print(f"Colang flow redirected off-topic intent: '{action}'")
```

---

## 3. Binary Safe/Unsafe Classification Parsing

Parsing the canonical 'safe' vs 'unsafe\nS1' response format from safety classifier models.

```python
classifier_output = "unsafe\nS2"
lines = classifier_output.split("\n")
is_safe = lines[0].strip() == "safe"
violated_category = lines[1].strip() if not is_safe else None

assert is_safe is False
assert violated_category == "S2"
print(f"Moderation verdict: safe={is_safe}, violation={violated_category}")
```

---
