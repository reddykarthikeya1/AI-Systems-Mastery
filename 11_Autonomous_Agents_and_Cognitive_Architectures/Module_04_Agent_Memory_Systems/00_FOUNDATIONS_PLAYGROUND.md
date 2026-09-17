# 🐣 Interactive Foundations Playground: Agent Memory Systems

> *"Short-term memory is a scratchpad on your desk; long-term memory is a filing cabinet in the archive."*

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
from collections import deque
```

---

## 1. Sliding Window Buffer Truncation

A bounded FIFO buffer keeps the most recent $K$ conversation turns while preventing context overflow.

```python
buffer = deque(maxlen=3)
buffer.append("turn 1: Hello")
buffer.append("turn 2: How can I help?")
buffer.append("turn 3: Check my order")
buffer.append("turn 4: Order #1234 is shipped")

assert len(buffer) == 3
assert "turn 1" not in buffer, "Oldest turn evicted"
assert buffer[0] == "turn 2: How can I help?"
print(f"Current working memory window: {list(buffer)}")
```

---

## 2. Episodic Fact Extraction and Storage

Extracting key user facts and storing them in a persistent dictionary across sessions.

```python
user_profile = {}
fact = ("preferred_language", "Python")
user_profile[fact[0]] = fact[1]

assert user_profile["preferred_language"] == "Python"
assert len(user_profile) == 1
print(f"Persisted episodic memory: {user_profile}")
```

---

## 3. Context Injection Assembly

Assembling long-term profile facts and short-term dialogue into the final prompt payload.

```python
profile_context = f"User preference: language={user_profile['preferred_language']}"
dialogue_context = "\n".join(buffer)
full_prompt = f"{profile_context}\n---\n{dialogue_context}"

assert "Python" in full_prompt
assert "turn 4" in full_prompt
print(f"Prompt assembled with hybrid memory ({len(full_prompt)} chars).")
```

---
