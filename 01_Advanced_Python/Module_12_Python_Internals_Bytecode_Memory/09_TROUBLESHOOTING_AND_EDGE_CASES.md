# Module 12: Troubleshooting, Python Internals & Memory Traps

This reference guide details subtle bugs in CPython memory management, `__slots__` inheritance, and AST manipulations.

---

## 1. The `__slots__` Inheritance Trap

### The Bug
```python
class BaseUser:
    __slots__ = ("user_id", "email")

class AdminUser(BaseUser):
    # Forgot to define __slots__ in the child subclass!
    pass

admin = AdminUser()
admin.custom_tag = "VIP" # ✅ Works! But AdminUser now has a full __dict__ in RAM!
print(hasattr(admin, "__dict__")) # True  <-- Memory savings lost!
```

### The Fix
Subclasses **must explicitly define `__slots__`** (even if empty `__slots__ = ()`) to prevent Python from creating an instance `__dict__`:
```python
class AdminUser(BaseUser):
    __slots__ = ("role",) # Only allocates role + inherits BaseUser slots
```

---

## 2. Cyclic References & `weakref`

### The Bug
```python
class Parent:
    def __init__(self):
        self.child = None

class Child:
    def __init__(self, parent):
        self.parent = parent # Strong reference creates circular cycle!
```

### Why It Matters
While the cyclic GC will eventually clean this up, reference counts never reach `0` on exit, delaying deallocation.

### The Fix
Use `weakref.ref` or `weakref.proxy` for back-references to break cycles immediately:
```python
import weakref

class Child:
    def __init__(self, parent):
        self.parent = weakref.ref(parent) # Weak reference (refcount does NOT increase)
```

---

## 3. `sys.getrefcount()` +1 Offset

### The Gotcha
```python
x = object()
print(sys.getrefcount(x)) # Output: 2  <-- Why 2 when only 'x' points to it?
```

### Why It Happens
Passing `x` as an argument into `sys.getrefcount(x)` creates a temporary reference inside the function stack frame.

### The Rule
The actual reference count is always `sys.getrefcount(x) - 1`.
