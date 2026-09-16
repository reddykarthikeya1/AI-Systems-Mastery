# Interactive Foundations Playground: Descriptors, Metaprogramming & Slots

> *"A descriptor is an attribute with a brain of its own."*

Welcome to the **Module 21 Metaprogramming Descriptors Memory** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Descriptors give you complete control over what happens when an attribute is accessed or set using `__get__` and `__set__`. Using `__slots__` strips the default `__dict__` from class instances, saving massive RAM.

---

## 2. Micro-Code Example (3-5 Lines)

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, 0)

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError(f"{self.name} must be positive!")
        instance.__dict__[self.name] = value

class Product:
    price = PositiveNumber()  # Controlled by descriptor!
```

### Line-by-Line Breakdown:
- `__set_name__`: Automatically learns the variable name (`'price'`) when the class is defined.
- `__get__`: Called whenever someone reads `obj.price`.
- `__set__`: Called whenever someone assigns `obj.price = 50`.
- `__slots__ = ('name', 'price')`: Eliminates instance dictionary bloat for million-object collections.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
What methods make a class a descriptor?

<details><summary><b>Show Answer</b></summary>

Implementing `__get__`, `__set__`, or `__delete__`.
</details>

---

### Drill 2: Quick Check
Why does `__slots__` reduce memory usage?

<details><summary><b>Show Answer</b></summary>

It prevents Python from creating a dynamic `__dict__` hash table for every single instance.
</details>

---
