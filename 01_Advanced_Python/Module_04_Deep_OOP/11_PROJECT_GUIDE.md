# Module_04_Deep_OOP: Project Implementation Guide

**Deliverable:** an enterprise-grade object-oriented banking system with abstract base classes, descriptors, currency conversion, and cooperative MRO.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_banking_system.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Monetary Descriptor
Implement `PositiveAmount` descriptor ensuring balances and transactions cannot be negative.

### Step 2 — Abstract Account Hierarchy
Define `Account(ABC)` with abstract methods `deposit` and `withdraw`, implemented by `SavingsAccount` and `CheckingAccount`.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_banking_system.py -k "basic or initial or health or create" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Multi-Currency Arithmetic
Implement `Currency` value object supporting explicit exchange rates and preventing raw float addition across currencies.

### Step 4 — Bank Transfer Coordination
Implement `Bank.transfer` executing atomic double-entry debit and credit operations.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/banking_system.py`, remove the `__hash__` implementation from `Currency` while leaving `__eq__`.
Run:
```bash
pytest ../project_solution/test_banking_system.py -k test_currency_equality_and_hashing -v
```
Watch the test fail with `TypeError: unhashable type: 'Currency'`, then restore `__hash__`.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_banking_system.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Interest Accrual Worker:** Add an automated compound interest accrual cycle for savings accounts.
2. **Overdraft Protection:** Create a cooperative mixin transferring funds from linked savings when checking drops below zero.
3. **Audit Trail Mixin:** Implement cooperative MRO mixin recording every transaction to a secure log.
4. **Dynamic Exchange Rate Provider:** Fetch live currency exchange rates via an abstract provider interface.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_savings_account_deposit_and_interest` | Proves savings accounts apply correct interest multipliers |
| `test_checking_account_overdraft_limit` | Proves checking accounts enforce overdraft boundaries |
| `test_currency_conversion_and_arithmetic` | Proves currency value objects prevent invalid cross-currency math |
| `test_bank_atomic_transfer` | Proves bank transfers debit and credit accounts atomically |
| `test_negative_deposit_raises_value_error` | Proves descriptor constraints reject negative deposit attempts |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain Python's C3 Linearization algorithm for method resolution order (MRO)
- [ ] Use super() correctly in cooperative multiple inheritance hierarchies
- [ ] Implement descriptors using __get__, __set__, and __set_name__
- [ ] Enforce abstract contracts using abc.ABC and @abstractmethod
- [ ] Implement value objects with immutable __eq__ and __hash__ contracts
- [ ] Avoid mutable class attribute traps that share state across instances
- [ ] Design robust double-entry financial domain models in pure Python
