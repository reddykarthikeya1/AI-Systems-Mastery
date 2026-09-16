# Debug Lab Incident Report: Overselling Limited Stock Under High Concurrency Race Condition

- **Severity:** P0 Critical Financial & Legal Liability
- **Affected Subsystem:** Module_20_Flash_Sale_Inventory_Reservation_Amazon
- **Reported Impact:** An item with 10 units in stock was purchased by 47 customers during a flash sale, forcing manual cancellations and refunds.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in flash_sale_engine.
Traceback (most recent call last):
  ...
RuntimeError: Overselling Limited Stock Under High Concurrency Race Condition
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_20_Flash_Sale_Inventory_Reservation_Amazon/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_flash_sale_engine.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_flash_sale_engine.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
