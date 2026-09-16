# Module 04: Troubleshooting, Common OOP Bugs & Edge Cases

This reference guide details common traps when designing object-oriented architectures in Python.

---

## 1. The Mutable Class Attribute State Leak

### The Bug
```python
class ShoppingCart:
    items = []  # ❌ Class variable shared by all carts!

    def add(self, item):
        self.items.append(item)

cart1 = ShoppingCart()
cart1.add("Laptop")

cart2 = ShoppingCart()
print(cart2.items)  # ['Laptop']  <-- Cart 2 sees Cart 1's items!
```

### Why It Happens
Class-level attributes are created **once** when the class definition is first parsed. All instance lookups (`self.items`) fall back to that single shared list in RAM.

### The Fix
Initialize mutable containers inside `__init__()`:
```python
class ShoppingCart:
    def __init__(self):
        self.items = []  # ✅ Unique instance variable for each cart
```

---

## 2. The Unhashable Object Bug (`__eq__` without `__hash__`)

### The Bug
```python
class Customer:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __eq__(self, other):
        return isinstance(other, Customer) and self.user_id == other.user_id

c = Customer("C-101")
lookup = {c: "Active"}  # ❌ Crash!
```
**Crash:** `TypeError: unhashable type: 'Customer'`

### Why It Happens
In Python, if a class overrides `__eq__` but does **not** define `__hash__`, Python automatically sets `__hash__ = None` to prevent corrupted hash table lookups.

### The Fix
Implement `__hash__` using the same immutable attributes used in `__eq__`:
```python
class Customer:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def __eq__(self, other):
        return isinstance(other, Customer) and self.user_id == other.user_id

    def __hash__(self):
        return hash(self.user_id)
```

---

## 3. `TypeError: Can't instantiate abstract class`

### The Bug
```python
from abc import ABC, abstractmethod

class BaseWorker(ABC):
    @abstractmethod
    def work(self): pass

    @abstractmethod
    def report(self): pass

class JuniorWorker(BaseWorker):
    def work(self):
        print("Working...")
    # Forgot to implement report()!

worker = JuniorWorker()  # ❌ Crash!
```
**Crash:** `TypeError: Can't instantiate abstract class JuniorWorker with abstract method report`

### Why It Happens
Python's ABC engine inspects the subclass during instantiation and strictly blocks any class that has not implemented **every single `@abstractmethod`**.

### The Fix
Ensure all abstract methods from parent classes are fully implemented.

---

## 4. Forgetting to Call `super().__init__()`

### The Bug
```python
class BaseAccount:
    def __init__(self, account_number: str):
        self.account_number = account_number
        self.is_active = True

class PremiumAccount(BaseAccount):
    def __init__(self, account_number: str, bonus_tier: int):
        # Forgot super().__init__(account_number)!
        self.bonus_tier = bonus_tier

prem = PremiumAccount("ACC-99", 2)
print(prem.is_active)  # ❌ AttributeError: 'PremiumAccount' object has no attribute 'is_active'
```

### The Fix
Always call `super().__init__(...)` when overriding a child constructor:
```python
class PremiumAccount(BaseAccount):
    def __init__(self, account_number: str, bonus_tier: int):
        super().__init__(account_number)
        self.bonus_tier = bonus_tier
```
