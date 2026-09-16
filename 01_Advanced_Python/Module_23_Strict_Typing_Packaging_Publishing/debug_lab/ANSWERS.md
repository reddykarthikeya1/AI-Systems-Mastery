# Debug Lab Answers: Module 23

<details>
<summary>Bug 1: Any disabling type checking</summary>

### Root Cause
`Any` is an escape hatch that silences static analysis. Using `Any` instead of protocols, generics, or unions transfers type errors to runtime.

### Fix
Use generics with bounds or a Protocol:
```python
from typing import Protocol

class HasIdentifier(Protocol):
    def get_id(self) -> int: ...

def transform_data(payload: HasIdentifier) -> int:
    return payload.get_id()
```
</details>
