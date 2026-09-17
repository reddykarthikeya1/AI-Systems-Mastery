"""Beginner playground for Module 01 - Agent Cognitive Architectures and Loops.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import json

# -------------------------------------------- 1. The ReAct (Reason + Act) State Machine
history = []
def add_step(role, content):
    history.append({"role": role, "content": content})

add_step("Thought", "User wants current weather in Tokyo. I must call get_weather tool.")
add_step("Action", "call:get_weather(city='Tokyo')")
add_step("Observation", "{'temp': 22, 'condition': 'Sunny'}")
add_step("Thought", "Now I have the answer. Formulating final response.")

assert len(history) == 4
assert history[1]["content"].startswith("call:")
print(f"ReAct trajectory successfully recorded: {len(history)} steps.")

# -------------------------------------------- 2. Termination Condition & Maximum Step Guard
max_steps = 5
step_count = 0
done = False

while not done and step_count < max_steps:
    step_count += 1
    if step_count == 3:
        done = True

assert done is True
assert step_count == 3
assert step_count <= max_steps
print(f"Agent finished in {step_count} steps (within budget of {max_steps}).")

# -------------------------------------------- 3. Final Answer Extraction
response = "Thought: verified calculations.\nFinal Answer: The distance is 42 km."
parts = response.split("Final Answer:")
final_answer = parts[1].strip()

assert final_answer == "The distance is 42 km."
assert "Thought:" in parts[0]
print(f"Extracted final answer: '{final_answer}'")

print()
print("All checks passed.")
