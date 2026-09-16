# Debug Lab Answers: Module 01

<details>
<summary>Bug 1: Floating-Point IEEE-754 Equality</summary>

### Root Cause
In binary floating-point representation, `0.1` and `0.2` cannot be represented with infinite precision. `0.1 + 0.2` is `0.30000000000000004`, which is strictly not equal to `0.3`.

### Fix
Use `math.isclose` or Python's `decimal.Decimal` module for financial arithmetic:
```python
from decimal import Decimal
import math

# Approach A (Floats with tolerance):
math.isclose(credit + debit, target, rel_tol=1e-9)

# Approach B (Exact monetary arithmetic):
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
```
</details>

<details>
<summary>Bug 2: Identity 'is' vs Equality '==' on Integers</summary>

### Root Cause
`is` checks memory address identity (`id(a) == id(b)`), while `==` checks value equivalence. CPython pre-allocates and caches integer objects in the range `[-5, 256]`. Integers outside that range are distinct objects unless interned.

### Fix
Always use `==` when comparing values:
```python
def calculate_tier_bonus(account_id_a: int, account_id_b: int) -> bool:
    return account_id_a == account_id_b
```
</details>

<details>
<summary>Bug 3: Off-by-one in range(1, months)</summary>

### Root Cause
`range(1, months)` generates values from `1` up to `months - 1`, resulting in `months - 1` total iterations.

### Fix
Use `range(months)` or `range(1, months + 1)`:
```python
def compute_installments(total_amount: float, months: int) -> list[float]:
    monthly = round(total_amount / months, 2)
    return [monthly for _ in range(months)]
```
</details>
