# Module 21: Troubleshooting, Metaprogramming & Descriptor Traps

This reference guide details dangerous bugs and architectural traps in Python metaprogramming.

---

## 1. The Descriptor Shared State Bug (Catastrophic Instance Leak)

### The Bug
```python
class BadDescriptor:
    def __set__(self, instance, value):
        self.value = value # ❌ Storing on descriptor itself!

    def __get__(self, instance, owner):
        return self.value

class User:
    age = BadDescriptor()

u1 = User(); u1.age = 20
u2 = User(); u2.age = 35
print(u1.age) # 🚨 PRINTS 35! Overwritten by u2!
```

### Why It Happens
There is only **one single instance** of `BadDescriptor` shared across all `User` instances. Modifying `self.value` overwrites the global descriptor attribute.

### The Fix
Always store state on the passed `instance` object (or in `instance.__dict__`):
```python
class GoodDescriptor:
    def __set_name__(self, owner, name):
        self.storage = f"_{name}"

    def __set__(self, instance, value):
        setattr(instance, self.storage, value) # ✅ Stored on instance!

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage, None)
```
