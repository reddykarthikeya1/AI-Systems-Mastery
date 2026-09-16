# Module 21: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Metaprogramming, Descriptors, and Dynamic Class Creation before moving to **Module 20**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Class Factories:** What does the 3-argument `type(name, bases, namespace_dict)` call do at runtime?
2. **Metaclasses:** What is a Metaclass, and what is the relationship between `type` and `object`?
3. **Subclass Hooks:** How does `__init_subclass__` allow customizing subclass creation without writing a full metaclass?
4. **The Descriptor Protocol:** What are the 4 dunder methods that make up the full Python descriptor protocol?
5. **Data vs Non-Data Descriptors:** What is the technical difference between a Data Descriptor and a Non-Data Descriptor?
6. **Lookup Precedence:** Why does a Data Descriptor override an instance's `__dict__`, while a Non-Data Descriptor does not?
7. **The Shared State Trap:** What happens if a descriptor stores an assigned value on `self` instead of the target `instance`?
8. **Automated Naming:** What role did `__set_name__(self, owner, name)` introduce in Python 3.6 to simplify descriptor code?
9. **Built-in Descriptors:** How do Python's standard `@property`, `@classmethod`, and regular functions utilize the descriptor protocol?
10. **ORM Internals:** How do ORMs like SQLAlchemy and Django use descriptors to intercept column assignment and generate SQL?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
It dynamically constructs and returns a new Python class object at runtime.

#### Answer 2:
A metaclass is a "class of a class"—a callable that defines how class objects themselves are instantiated and customized during compilation.

#### Answer 3:
`__init_subclass__` is called on the parent class whenever a new child class inherits from it, allowing validation and auto-registration with simple, clean syntax.

#### Answer 4:
1. `__get__(self, instance, owner)`
2. `__set__(self, instance, value)`
3. `__delete__(self, instance)`
4. `__set_name__(self, owner, name)`

#### Answer 5:
- **Data Descriptor:** Defines `__set__` and/or `__delete__`.
- **Non-Data Descriptor:** Only defines `__get__` (e.g. methods and `@property` getters without setters).

#### Answer 6:
Python's attribute resolution checks: Data Descriptors $\rightarrow$ Instance `__dict__` $\rightarrow$ Non-Data Descriptors $\rightarrow$ Class `__dict__` $\rightarrow$ `__getattr__`.

#### Answer 7:
Every instance of the parent class will share and overwrite the exact same single variable, creating a critical state contamination bug.

#### Answer 8:
When the class is constructed, Python automatically passes the attribute name (e.g. `"age"`) to `__set_name__`, removing manual string name passing.

#### Answer 9:
Standard functions implement `__get__` to bind the instance `self` and return a method object; `@property` implements `__get__` and `__set__` to wrap getter/setter functions.

#### Answer 10:
ORM column descriptors intercept `model.age = 25`, mark the field as "dirty" in session state, validate the SQL type constraint, and prepare UPDATE statements.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Bounded Float Descriptor

**Goal:** Create a `BoundedFloat` descriptor that verifies floating point values between `min_val` and `max_val`.

<details>
<summary><b>Solution Code</b></summary>

```python
class BoundedFloat:
    def __init__(self, min_val: float, max_val: float) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.storage = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None: return self
        return getattr(instance, self.storage, self.min_val)

    def __set__(self, instance, value):
        val = float(value)
        if not (self.min_val <= val <= self.max_val):
            raise ValueError(f"Value {val} outside bounds [{self.min_val}, {self.max_val}]")
        setattr(instance, self.storage, val)

# Verification:
class Sensor:
    temp = BoundedFloat(-50.0, 150.0)

s = Sensor()
s.temp = 23.5
print("Sensor Temp Validated:", s.temp)
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Descriptor storing state on itself

```python
class Positive:
    def __set_name__(self, owner, name: str) -> None:
        self.name = name

    def __get__(self, obj, objtype=None) -> int:
        return self.value

    def __set__(self, obj, value: int) -> None:
        if value <= 0:
            raise ValueError("must be positive")
        self.value = value            # stored on the DESCRIPTOR

class Product:
    quantity = Positive()

a, b = Product(), Product()
a.quantity = 5
b.quantity = 9
print(a.quantity)
```

**Observed symptom:** Prints `9`. Setting `b` overwrote `a`.

**(a)** Why is the value shared between instances?

**(b)** Where should it be stored, and what are two ways to do it?

**(c)** What does `__set_name__` give you that makes one of those ways clean?

<details>
<summary><b>Show the diagnosis</b></summary>

The descriptor is a **class attribute** — one object shared by every instance of `Product`. `self.value` is state on that single shared descriptor, so all instances read and write the same slot.

**Store it per instance.** (1) In the instance dict under a private name: `obj.__dict__[self.name] = value`. (2) In a `WeakKeyDictionary` keyed by instance, which also works for classes using `__slots__`.

**`__set_name__`** is what makes option 1 clean: Python calls it at class creation with the attribute's name, so the descriptor learns it is called `"quantity"` without you having to repeat the name in the constructor. Before 3.6 you had to write `quantity = Positive('quantity')` — the redundancy that `__set_name__` removed.

</details>

---

### D2. Metaclass conflict

```python
from abc import ABC, ABCMeta

class Registry(type):
    pass

class Base(ABC, metaclass=Registry):
    pass
```

**Observed symptom:** `TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases`.

**(a)** What are the two conflicting metaclasses?

**(b)** What is the fix?

**(c)** What is the simpler alternative that avoids metaclasses entirely?

<details>
<summary><b>Show the diagnosis</b></summary>

`ABC` already has the metaclass `ABCMeta`. Declaring `metaclass=Registry` (whose metaclass is plain `type`) asks Python to use a metaclass that is *not* a subclass of `ABCMeta`, which would break abstract-method enforcement.

**Fix:** make your metaclass inherit from the other — `class Registry(ABCMeta): ...` — then `class Base(ABC, metaclass=Registry)` works because `Registry` satisfies both requirements.

**Simpler alternative:** `__init_subclass__`. It is a plain classmethod called whenever a subclass is created, it composes freely with any metaclass, and it covers the overwhelming majority of registry and validation use cases:

```python
class Base:
    registry: dict[str, type] = {}
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        Base.registry[cls.__name__] = cls
```

Reach for a metaclass only when you must control class *creation* itself.

</details>

---

### D3. `__getattr__` recursion

```python
class Proxy:
    def __init__(self, target: object) -> None:
        self.target = target

    def __getattr__(self, name: str):
        return getattr(self.target, name)

p = Proxy([1, 2, 3])
```

**Observed symptom:** `RecursionError` during `__init__`, before the object is even usable.

**(a)** Trace the recursion — what is looked up, and when?

**(b)** What is the fix?

**(c)** How does `__getattribute__` differ, and why is it more dangerous?

<details>
<summary><b>Show the diagnosis</b></summary>

`self.target = target` in `__init__` is a *store*, which is fine. The recursion comes from the *load*: `__getattr__` reads `self.target`, but if `target` is not yet in the instance dict, that lookup fails and calls `__getattr__` again — which reads `self.target` — forever.

**Fix:** bypass the instance dict lookup — `object.__getattribute__(self, 'target')` — or set the attribute via `object.__setattr__` before anything else, or guard:

```python
def __getattr__(self, name):
    if name == 'target':
        raise AttributeError(name)
    return getattr(self.target, name)
```

**`__getattribute__`** is called for **every** attribute access, not just failed ones. Overriding it means even `self.__dict__` goes through your code, so the recursion risk is far higher and the performance cost is paid on every access. `__getattr__` (the fallback) is almost always what you want.

</details>

---

### D4. Decorator loses the signature

```python
import functools

def logged(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper

@logged
def create_user(email: str, admin: bool = False) -> dict:
    return {"email": email}
```

**Observed symptom:** FastAPI raises `Invalid args for response field`, and `inspect.signature` reports `(*args, **kwargs)`.

**(a)** What does `functools.wraps` copy, and what does it not?

**(b)** How do you preserve the real signature?

**(c)** Why does this break FastAPI specifically?

<details>
<summary><b>Show the diagnosis</b></summary>

`functools.wraps` copies `__name__`, `__doc__`, `__module__`, `__qualname__`, `__dict__` and `__wrapped__`. It does **not** change the wrapper's actual parameters, so `inspect.signature` follows `__wrapped__` in some cases but the runtime signature remains `(*args, **kwargs)`.

**Preserve it** with `inspect.signature(fn)` assigned to `wrapper.__signature__`, or use the `decorator` library, or — cleanest for typing — `ParamSpec`:

```python
P = ParamSpec('P'); R = TypeVar('R')
def logged(fn: Callable[P, R]) -> Callable[P, R]: ...
```

which keeps the static types exact.

**FastAPI breaks** because it *introspects* the signature to build the request model, validation and OpenAPI schema. `(*args, **kwargs)` tells it nothing, so it cannot determine what the endpoint accepts. Any framework driven by introspection — FastAPI, Typer, Click, pytest fixtures — has this sensitivity.

</details>

---

### D5. `__slots__` and a class attribute clash

```python
class Config:
    __slots__ = ("debug",)
    debug = False
```

**Observed symptom:** `ValueError: 'debug' in __slots__ conflicts with class variable`.

**(a)** Why can a name not be both?

**(b)** How do you provide a default for a slotted attribute?

**(c)** What else silently stops working when you add `__slots__`?

<details>
<summary><b>Show the diagnosis</b></summary>

`__slots__` creates a **descriptor** on the class for each name, which is where the per-instance storage lives. A class variable of the same name would occupy that exact attribute slot, so the descriptor could never be reached. Python rejects the ambiguity at class-creation time.

**Provide the default in `__init__`** — `def __init__(self, debug: bool = False): self.debug = debug` — or use `@dataclass(slots=True)`, which generates both correctly.

**Also stops working:** weak references (unless you add `'__weakref__'` to `__slots__`), `pickle` in some protocols without `__getstate__`, `functools.cached_property` (it needs a `__dict__`), monkeypatching attributes onto instances, and multiple inheritance from two classes that both define non-empty `__slots__`. `__slots__` is a real memory optimisation with real costs — measure before adopting it.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
