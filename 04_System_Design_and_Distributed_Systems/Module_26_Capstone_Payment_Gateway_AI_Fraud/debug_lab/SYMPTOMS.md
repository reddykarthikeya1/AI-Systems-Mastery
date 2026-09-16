# Debug Lab Incident Report: Accounting Discrepancy from Unbalanced Double-Entry Ledger Posting

- **Severity:** P0 Financial Regulatory Non-Compliance
- **Affected Subsystem:** Module_26_Capstone_Payment_Gateway_AI_Fraud
- **Reported Impact:** Audit reconciliation failed with a $1,250 discrepancy because a fee calculation rounding error allowed debits to exceed credits by $0.02 across 50,000 transactions.

---

## 🚨 Observable Symptoms & Logs
Under production traffic or simulated concurrent execution, the service experiences unexpected failures:
```text
CRITICAL: Defect encountered in payment_gateway_platform.
Traceback (most recent call last):
  ...
RuntimeError: Accounting Discrepancy from Unbalanced Double-Entry Ledger Posting
```

---

## 🔬 How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd "System Design/Module_26_Capstone_Payment_Gateway_AI_Fraud/debug_lab"
   ```
2. Run the defective simulation script:
   ```bash
   python broken_payment_gateway_platform.py
   ```
3. Observe the invariant violation or crash.

---

## 🎯 Your Objective
1. Inspect `broken_payment_gateway_platform.py` to pinpoint the subtle architectural flaw.
2. Read the root cause analysis and hardened fix in `ANSWERS.md` after formulating your hypothesis.
