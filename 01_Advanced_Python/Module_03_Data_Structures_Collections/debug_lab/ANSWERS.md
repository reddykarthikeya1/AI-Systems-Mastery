# Debug Lab Answers: Module 03

<details>
<summary>Bug 1: Dictionary mutation during iteration</summary>

### Root Cause
Python's dictionary iterators guard against concurrent modifications. Deleting a key while iterating over `orders_dict.items()` invalidates the internal hashtable iteration pointer.

### Fix
Iterate over a static snapshot of keys or use a dictionary comprehension:
```python
def cancel_expired_orders(orders_dict: dict[str, int], expiry_threshold: int):
    expired = [k for k, age in orders_dict.items() if age > expiry_threshold]
    for k in expired:
        del orders_dict[k]
```
</details>

<details>
<summary>Bug 2: Shallow copy of nested data structures</summary>

### Root Cause
`copy.copy()` duplicates the top-level container, but the nested `list` and `dict` objects inside it remain pointers to the identical memory blocks.

### Fix
Use `copy.deepcopy()` to create an isolated clone of nested objects:
```python
from copy import deepcopy

def duplicate_order_portfolio(portfolio: dict[str, list[dict]]) -> dict[str, list[dict]]:
    return deepcopy(portfolio)
```
</details>

<details>
<summary>Bug 3: Attempting to hash mutable dictionary</summary>

### Root Cause
Sets require elements to implement `__hash__` and be immutable. Python dicts are mutable and do not have a `__hash__` method.

### Fix
Store an immutable hashable representation, such as a tuple of sorted items or frozen dataclass:
```python
def register_trader_tokens(traders: list[dict]) -> set:
    return {tuple(sorted(trader.items())) for trader in traders}
```
</details>
