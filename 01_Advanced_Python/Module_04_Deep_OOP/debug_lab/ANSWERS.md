# Debug Lab Answers: Module 04

<details>
<summary>Bug 1: Mutable class-level attribute</summary>

### Root Cause
Defining `transaction_log: list[str] = []` directly inside the class body creates a single class attribute shared across every instance.

### Fix
Initialize instance-specific attributes inside `__init__`:
```python
def __init__(self, owner: str, balance: float):
    self.owner = owner
    self.balance = balance
    self.transaction_log: list[str] = []
```
</details>

<details>
<summary>Bug 2: Implementing __eq__ without __hash__</summary>

### Root Cause
In Python 3, defining `__eq__` automatically sets `__hash__ = None` to prevent mutable equality violations. If instances must be usable in dict keys or sets, `__hash__` must be explicitly implemented.

### Fix
Implement `__hash__` using the immutable identifying fields:
```python
def __hash__(self) -> int:
    return hash(self.account_num)
```
</details>

<details>
<summary>Bug 3: Explicit parent call instead of cooperative super()</summary>

### Root Cause
Directly calling `BaseService.log(self, ...)` short-circuits Python's C3 linearization (MRO), skipping sibling mixins in multiple inheritance hierarchies.

### Fix
Always use `super().log(...)`:
```python
class AuditMixin(BaseService):
    def log(self, msg: str):
        super().log(f"[Audit] {msg}")
```
</details>
