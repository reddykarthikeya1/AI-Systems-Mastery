"""Beginner playground for Module 04 - Agent Memory Systems.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import deque

# -------------------------------------------- 1. Sliding Window Buffer Truncation
buffer = deque(maxlen=3)
buffer.append("turn 1: Hello")
buffer.append("turn 2: How can I help?")
buffer.append("turn 3: Check my order")
buffer.append("turn 4: Order #1234 is shipped")

assert len(buffer) == 3
assert "turn 1" not in buffer, "Oldest turn evicted"
assert buffer[0] == "turn 2: How can I help?"
print(f"Current working memory window: {list(buffer)}")

# -------------------------------------------- 2. Episodic Fact Extraction and Storage
user_profile = {}
fact = ("preferred_language", "Python")
user_profile[fact[0]] = fact[1]

assert user_profile["preferred_language"] == "Python"
assert len(user_profile) == 1
print(f"Persisted episodic memory: {user_profile}")

# -------------------------------------------- 3. Context Injection Assembly
profile_context = f"User preference: language={user_profile['preferred_language']}"
dialogue_context = "\n".join(buffer)
full_prompt = f"{profile_context}\n---\n{dialogue_context}"

assert "Python" in full_prompt
assert "turn 4" in full_prompt
print(f"Prompt assembled with hybrid memory ({len(full_prompt)} chars).")

print()
print("All checks passed.")
