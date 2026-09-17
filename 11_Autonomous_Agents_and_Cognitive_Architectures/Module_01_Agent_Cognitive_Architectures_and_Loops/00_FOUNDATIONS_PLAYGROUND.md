# 🐣 Interactive Foundations Playground: Agent Cognitive Architectures and Loops

> *"A ReAct agent is a detective: it Thinks about the clues, Takes Action, and Observes the result before deciding next steps."*

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

## 1. The ReAct (Reason + Act) State Machine

The agent iterates through a Thought -> Action -> Observation loop until the final answer is reached.

```python
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
```

---

## 2. Termination Condition & Maximum Step Guard

A hard iteration ceiling prevents infinite loops when an agent encounters unexpected tool errors.

```python
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
```

---

## 3. Final Answer Extraction

Extracting the final user-facing response once the model outputs the designated final answer marker.

```python
response = "Thought: verified calculations.\nFinal Answer: The distance is 42 km."
parts = response.split("Final Answer:")
final_answer = parts[1].strip()

assert final_answer == "The distance is 42 km."
assert "Thought:" in parts[0]
print(f"Extracted final answer: '{final_answer}'")
```

---
