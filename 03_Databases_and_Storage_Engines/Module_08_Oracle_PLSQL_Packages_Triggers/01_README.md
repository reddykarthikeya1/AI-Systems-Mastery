# Module 08: Oracle PL/SQL, Packages, Triggers & Autonomous Transactions

> **Brand new to this topic?** Start with [`00_W3_BEGINNER_PLAYGROUND.md`](00_W3_BEGINNER_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 08**. In this module, you will dive deep into **PL/SQL (Procedural Language/SQL)** — Oracle's procedural programming extension that powers multi-billion dollar financial ledgers, automated clearing houses, and high-security defense pipelines.

---

## 🏎️ 1. The Dual-Engine Context Switch & Bulk Processing

One of the most dangerous performance traps in Oracle is the **Engine Context Switch**:
- Oracle has two distinct runtime engines: the **SQL Engine** (handles relational queries) and the **PL/SQL Engine** (handles procedural logic, loops, conditionals).
- When developers write naive row-by-row procedural cursor loops:
  ```sql
  FOR rec IN (SELECT id, amount FROM invoices) LOOP
      UPDATE accounts SET balance = balance + rec.amount WHERE id = rec.id;
  END LOOP;
  ```
  Oracle must switch control between the PL/SQL engine and the SQL engine **twice per row**. For 1,000,000 rows, that is **2,000,000 context switches**!

```
[PL/SQL Engine] ──(1. Send SQL DML)──► [SQL Engine] ──(2. Return status)──► [PL/SQL Engine]
       ▲                                                                           │
       └──────────────────────── Repeat 1,000,000 Times! ──────────────────────────┘
```

### The Solution: `BULK COLLECT` and `FORALL`
By vectorizing data transfer, Oracle bundles thousands of rows into an in-memory collection and passes them in a single batch transition:
```sql
SELECT id, amount BULK COLLECT INTO l_ids, l_amounts FROM invoices;
FORALL i IN 1..l_ids.COUNT SAVE EXCEPTIONS
    UPDATE accounts SET balance = balance + l_amounts(i) WHERE id = l_ids(i);
```
**Result**: Context switches drop from 2,000,000 down to **2**!

---

## 📦 2. Oracle Packages & Autonomous Transactions

### Package Specification vs. Body
Oracle enforces modularity through two distinct artifacts:
1. **Package Specification (`PACKAGE SPEC`)**: The public interface declaring functions, procedures, types, and exceptions.
2. **Package Body (`PACKAGE BODY`)**: The private implementation. Allows modifying business logic without invalidating dependent callers.

### Autonomous Transactions (`PRAGMA AUTONOMOUS_TRANSACTION`)
Normally, when a parent transaction issues a `ROLLBACK`, every statement executed within that session is undone.
However, in security, compliance, and auditing:
- If a fraudulent transfer fails, you **must commit an audit log entry** recording the attempt, even while rolling back the financial transaction!
- **Autonomous Transactions**: Suspend the main transaction, execute an isolated sub-transaction with its own independent `COMMIT` or `ROLLBACK`, and then resume the parent transaction.

```
[Main Transaction (Tx 101)]
       ├── Debit Account A ($10,000)
       ├── Attempt Credit Account B (Fails - Invalid Route)
       ├── Call Log_Security_Failure()
       │        └── [Autonomous Transaction (Tx 102)]
       │                 ├── INSERT INTO audit_logs VALUES (...)
       │                 └── COMMIT! (Permanently saved to disk)
       └── ROLLBACK! (Account A balance is restored, but Audit Log remains!)
```

---

## ⚠️ 3. Triggers & The Infamous Mutating Table Error (`ORA-04091`)

A **Row-Level Trigger** (`AFTER UPDATE FOR EACH ROW`) fires for every modified row.
If that trigger attempts to query or update the table that fired it:
```sql
CREATE OR REPLACE TRIGGER trg_check_budget
AFTER INSERT ON department_expenses FOR EACH ROW
BEGIN
    -- ORA-04091: table DEPARTMENT_EXPENSES is mutating, trigger may not see it!
    SELECT SUM(amount) INTO l_total FROM department_expenses WHERE dept_id = :NEW.dept_id;
END;
```
### Why Oracle Throws `ORA-04091`
The table is in a state of flux (mid-statement transition). Some rows are updated, some are not. If Oracle allowed reading the table, it could not guarantee a mathematically consistent view of the data.

### The Modern Cure: Compound Triggers (`COMPOUND DML`)
Introduced to eliminate mutating table workarounds, a Compound Trigger combines all 4 execution timing points into a single stateful structure:
1. `BEFORE STATEMENT`: Initialize package-scoped collection.
2. `BEFORE EACH ROW`: Validate row values.
3. `AFTER EACH ROW`: Buffer row IDs into in-memory collection without querying table.
4. `AFTER STATEMENT`: Table mutation is finished! Safely query the table and perform aggregations using the buffered IDs.

---

## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/oracle_plsql_engine.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | oracle_plsql_engine.py (Autonomous audit logger & banking package) | oracle_plsql_live.py (python-oracledb, PL/SQL package execution) |
| **Verification** | `project_solution/test_oracle_plsql_engine.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. ORA-04091 Mutating Table: Row-level triggers attempting to query the table currently being modified.
2. Context Switching Overhead: Iterating row-by-row in PL/SQL loops rather than using FORALL bulk array binding.
3. Lost Audit Records: Omitting PRAGMA AUTONOMOUS_TRANSACTION causes security logs to roll back when parent transactions fail.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT put complex business logic in database triggers where execution flow becomes invisible and difficult to trace; encapsulate logic in PL/SQL Packages.

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_08_Oracle_PLSQL_Packages_Triggers -v

# Operational Diagnostics & Health Verification
sqlplus system/oracle@localhost:1521/FREEPDB1 <<EOF
SELECT object_name, status FROM user_objects WHERE object_type = 'PACKAGE BODY';
EXIT;
EOF
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_oracle_plsql.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](04_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](05_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.

