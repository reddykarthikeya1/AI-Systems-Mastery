# Module 05: Troubleshooting, Decorator Bugs & Generator Traps

This reference guide details common developer pitfalls with decorators, generators, and context managers.

---

## 1. Missing `@functools.wraps` (Function Metadata Erasure)

### The Bug
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        """Wrapper docstring."""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def fetch_user_profile():
    """Fetches user account details."""
    pass

print(fetch_user_profile.__name__)  # 'wrapper'  <-- Function name was erased!
print(fetch_user_profile.__doc__)   # 'Wrapper docstring.' <-- Original docstring lost!
```

### Why It Happens
Without `@functools.wraps(func)`, the decorator replaces the original function object with `wrapper`, destroying debugging info, docstrings, and IDE autocomplete hints.

### The Fix
Always decorate `wrapper` with `@functools.wraps(func)`:
```python
import functools

def my_decorator(func):
    @functools.wraps(func)  # ✅ Preserves __name__, __doc__, __annotations__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 2. The Exhausted Generator Trap

### The Bug
```python
def get_numbers():
    yield 1
    yield 2
    yield 3

gen = get_numbers()

# First loop:
print("First pass:", list(gen))  # [1, 2, 3]

# Second loop:
print("Second pass:", list(gen)) # []  <-- Empty!
```

### Why It Happens
Generators are **one-time data streams**. Once they reach the end and raise `StopIteration`, they cannot be reset or rewound.

### The Fix
If you need to iterate multiple times:
1. Call the generator factory function again (`get_numbers()`).
2. Or convert to a list `lst = list(get_numbers())` if the dataset fits comfortably in RAM.

---

## 3. Accidental Exception Suppression in `__exit__`

### The Bug
```python
class FaultyResource:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Cleaning up...")
        return True  # ❌ DANGEROUS! Suppresses ALL exceptions!

with FaultyResource():
    x = 10 / 0  # ZeroDivisionError is silently swallowed!

print("Program continues with corrupted state...")
```

### Why It Happens
In Python, if `__exit__()` returns `True`, Python **suppresses the exception** and ignores it completely.

### The Fix
Only return `True` if you explicitly intended to handle that specific exception. Return `False` (or `None`) by default to allow errors to propagate:
```python
def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
    print("Cleaning up...")
    return False  # ✅ Standard behavior
```

---

## 4. Parameterized Decorator 3-Layer Nesting

### The Rule
* A **standard decorator** has **2 layers**: `decorator(func) -> wrapper(*args)`
* A **parameterized decorator** (taking custom options like `@retry(attempts=3)`) requires **3 layers**:
  `factory(options) -> decorator(func) -> wrapper(*args)`

```python
def repeat(num_times: int):        # Layer 1: Factory (takes decorator parameters)
    def decorator(func):           # Layer 2: Decorator (takes the function)
        @functools.wraps(func)
        def wrapper(*args, **kwargs): # Layer 3: Wrapper (takes runtime arguments)
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
```
