# 🐣 Interactive Foundations Playground: Decorators, Generators & Context Managers

> *"A decorator is like wrapping a birthday gift: the gift inside stays the same, but the wrapping adds festive flair!"*

Welcome to Module 05! Let's explore three of Python's most expressive features in plain English.

---

## 1. What is a Decorator? (The Gift Wrap Model)

A decorator is just a function that takes another function, wraps it with some extra behavior (like logging, timing, or access checks), and returns the enhanced function.

```python
def my_logger(func):
    def wrapper():
        print("[Before] Function is starting...")
        func()
        print("[After] Function finished!")
    return wrapper

# Use the @ syntax to gift-wrap say_hello:
@my_logger
def say_hello():
    print("Hello, world!")

say_hello()
```

### Output:
```text
📢 [Before] Function is starting...
Hello, world!
✅ [After] Function finished!
```

---

## 2. What is a Generator? (`yield` is a Pause Button)

A normal function returns everything at once and terminates. A **generator** produces values **one at a time on demand** using the `yield` keyword:

```python
def countdown(start):
    print("Starting countdown engine...")
    while start > 0:
        yield start  # PAUSES and yields 'start' to the caller!
        start -= 1

# When looped over, it wakes up, runs to the next yield, and pauses again:
for num in countdown(3):
    print(f"Count: {num}")
```

### Why use Generators?
If you generate 10,000,000 numbers in a list, your computer runs out of RAM. A generator generates numbers one-by-one as needed, using virtually **0 MB of RAM**!

---

## 3. Context Managers (`with` blocks)

Ever worry about forgetting to close a file or release a lock? The `with` statement guarantees cleanup:

```python
# The with block opens the file, lets you read it, and automatically closes it:
with open("notes.txt", "w") as f:
    f.write("Remember to buy milk!")
# File is automatically 100% closed here, even if code crashes!
```

---

## 4. Run the Interactive Playground
```bash
python 03_try_it_yourself.py
```
Test an interactive timer decorator and a live countdown generator!

---

## 5. Beginner Quick-Check Drills

### Drill 1: Generator Keyword
Which keyword pauses a function and yields a value instead of terminating?
<details><summary><b>Show Answer</b></summary>
<b><code>yield</code></b>
</details>

---

### Drill 2: Applying a Decorator
What symbol is placed before the decorator name directly above a function?
```python
___my_decorator
def my_function():
    pass
```
<details><summary><b>Show Answer</b></summary>
<b><code>@</code></b> (e.g., <code>@my_decorator</code>)
</details>\n