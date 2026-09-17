# 🐣 Interactive Foundations Playground: Functions, Scopes & Closures

> *"Functions are first-class citizens capable of capturing lexical state in closures."*

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
import functools
```

---

## 1. Lexical Scoping and the LEGB Rule

Python resolves names in Local, Enclosing, Global, and Built-in scopes sequentially.

```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        return x
    return inner()

assert outer() == "enclosing"
assert x == "global"
print(f"LEGB resolution: outer returned '{outer()}'")
```

---

## 2. State Retention in Closures

A closure retains access to variables from its enclosing scope even after that scope has finished execution.

```python
def make_counter(start=0):
    count = start
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c = make_counter(10)
assert c() == 11
assert c() == 12
assert c() == 13
print("Closure state persisted across function invocations.")
```

---

## 3. Partial Application with functools

Partial application freezes a subset of function arguments to produce specialized callables.

```python
def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
assert square(5) == 25
assert square(9) == 81
print("Partial function frozen exponent=2 successfully.")
```

---
