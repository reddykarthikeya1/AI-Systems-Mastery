# Module 08 Oracle PLSQL Packages Triggers: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Oracle PL/SQL Packages, Triggers & Autonomous Transactions** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is the purpose of PRAGMA AUTONOMOUS_TRANSACTION in PL/SQL?** What is the purpose of PRAGMA AUTONOMOUS_TRANSACTION in PL/SQL?
2. **Why does an ORA-04091 'mutating table' error occur, and how do Compound Triggers solve it?** Why does an ORA-04091 'mutating table' error occur, and how do Compound Triggers solve it?
3. **How does FORALL bulk binding improve DML performance compared to standard FOR loops?** How does FORALL bulk binding improve DML performance compared to standard FOR loops?
4. **What is the difference between a PL/SQL Package Specification and Package Body?** What is the difference between a PL/SQL Package Specification and Package Body?
5. **What does BULK COLLECT INTO do in PL/SQL?** What does BULK COLLECT INTO do in PL/SQL?
6. **How does %ROWTYPE differ from %TYPE in PL/SQL variable declaration?** How does %ROWTYPE differ from %TYPE in PL/SQL variable declaration?
7. **What is the difference between RAISE_APPLICATION_ERROR and standard RAISE in PL/SQL?** What is the difference between RAISE_APPLICATION_ERROR and standard RAISE in PL/SQL?
8. **What are the four timing points of a Compound DML Trigger?** What are the four timing points of a Compound DML Trigger?
9. **Can an autonomous transaction see uncommitted data from its parent transaction?** Can an autonomous transaction see uncommitted data from its parent transaction?
10. **What is the PL/SQL Result Cache?** What is the PL/SQL Result Cache?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
It executes an independent transaction within a procedure, committing or rolling back its work without affecting the main caller transaction.

#### Answer 2:
Row triggers cannot query the table being modified. A Compound Trigger provides 4 timing phases, allowing row-level data to be collected and aggregated in the statement phase.

#### Answer 3:
It switches context between the PL/SQL runtime and the SQL execution engine once for the entire array batch rather than once per row.

#### Answer 4:
The specification declares public constants, types, and procedure signatures; the body contains the private implementation details and logic.

#### Answer 5:
It retrieves entire query result sets into in-memory collections (nested tables or varrays) in a single context switch.

#### Answer 6:
%TYPE anchors a variable to a single column's data type; %ROWTYPE anchors a record to the entire column structure of a table.

#### Answer 7:
RAISE_APPLICATION_ERROR allows assigning custom error numbers (-20000 to -20999) and human-readable messages returned to client applications.

#### Answer 8:
BEFORE STATEMENT, BEFORE EACH ROW, AFTER EACH ROW, and AFTER STATEMENT.

#### Answer 9:
No. An autonomous transaction is a completely separate session and cannot see the calling transaction's uncommitted writes.

#### Answer 10:
A memory structure that caches the return values of deterministic functions in the SGA, eliminating repeated function execution for identical arguments.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Build a high-performance bulk billing batch processor using FORALL and SAVE EXCEPTIONS.

### 🚀 Challenge 2: Architect Stretch Problem
Implement an autonomous security auditor logging every transaction attempt regardless of parent transaction outcome.

---

## Verification Criteria
- [ ] Answered all 10 diagnostic questions without checking reference notes.
- [ ] Implemented Challenge 1 and validated with automated unit tests.
- [ ] Documented trade-offs and edge case behaviors for Challenge 2.

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. ORA-04091 Mutating Table error in row-level trigger

```sql
CREATE OR REPLACE TRIGGER trg_check_salary
BEFORE INSERT OR UPDATE ON employees
FOR EACH ROW
DECLARE
    v_max_sal NUMBER;
BEGIN
    -- Querying the very table that is currently being modified!
    SELECT MAX(salary) INTO v_max_sal FROM employees WHERE dept_id = :NEW.dept_id;
    IF :NEW.salary > v_max_sal * 1.5 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Salary exceeds departmental ceiling');
    END IF;
END;
```

**Observed symptom:** Updating employee salary fails with `ORA-04091: table HR.EMPLOYEES is mutating, trigger/function may not see it`.

**(a)** What is a 'mutating table' in Oracle PL/SQL, and why does Oracle restrict row-level triggers from reading it?

**(b)** Why does a Compound Trigger eliminate the mutating table restriction?

**(c)** Which timing points (phases) are supported in an Oracle Compound Trigger?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** A table is 'mutating' when it is in the middle of a DML statement. If a row-level trigger (`FOR EACH ROW`) reads the table, it would see an inconsistent, partially updated state, violating transaction consistency rules.

**Fix:** Use a **Compound Trigger**. In the `BEFORE STATEMENT` phase, initialize state; in `AFTER EACH ROW`, record affected IDs into a package collection; in `AFTER STATEMENT`, query the table and perform bulk validation after the table has stabilized.

**Compound Trigger Phases:** `BEFORE STATEMENT`, `BEFORE EACH ROW`, `AFTER EACH ROW`, `AFTER STATEMENT`.

</details>

---

### D2. Autonomous Transaction deadlock on uncommitted parent row lock

```
PROCEDURE transfer(p_from INT, p_to INT, p_amt NUMBER) IS
    PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
    -- Parent transaction has ALREADY updated account p_from!
    UPDATE accounts SET balance = balance - p_amt WHERE id = p_from;
    COMMIT;
END;
```

**Observed symptom:** Application freezes indefinitely; after 60 seconds, Oracle terminates the session with a deadlock error.

**(a)** Why is an autonomous transaction considered a completely independent database session?

**(b)** What happens when an autonomous transaction attempts to modify a row locked by its parent transaction?

**(c)** What is the valid architectural use case for `PRAGMA AUTONOMOUS_TRANSACTION`?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** `PRAGMA AUTONOMOUS_TRANSACTION` creates a separate child transaction boundary. It cannot see uncommitted changes made by the parent transaction and cannot acquire exclusive locks held by the parent. Attempting to update `p_from` causes the child to wait on the parent, while the parent waits for the procedure to return — an immediate deadlock!

**Valid Use Case:** Autonomous transactions should **only** be used for independent audit logging or error logging that must commit even if the parent transaction rolls back: `INSERT INTO audit_log VALUES (...) COMMIT;`.

</details>

---

### D3. Bulk FORALL processing losing error indexes without SAVE EXCEPTIONS

```
BEGIN
    FORALL i IN 1..order_ids.COUNT
        UPDATE orders SET status = 'PROCESSED' WHERE id = order_ids(i);
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Batch failed: ' || SQLERRM);
END;
```

**Observed symptom:** Row 42 has an invalid constraint; the entire batch of 10,000 updates aborts, and the exception handler cannot determine which specific row failed.

**(a)** Why does standard FORALL abort execution on the very first encountered exception?

**(b)** What clause allows FORALL to process all valid rows and defer exception collection?

**(c)** How do you inspect individual error indices and error codes using `SQL%BULK_EXCEPTIONS`?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Without `SAVE EXCEPTIONS`, the first DML error immediately terminates the `FORALL` statement and rolls back uncommitted rows.

**Fix:** Add `SAVE EXCEPTIONS`:
```plsql
FORALL i IN 1..order_ids.COUNT SAVE EXCEPTIONS
    UPDATE orders SET status = 'PROCESSED' WHERE id = order_ids(i);
```
In the exception block, catch `ORA-24381` and iterate through `SQL%BULK_EXCEPTIONS` to log `SQL%BULK_EXCEPTIONS(i).ERROR_INDEX` and `SQL%BULK_EXCEPTIONS(i).ERROR_CODE`.

</details>

---

### D4. Package state invalidation ORA-04068 under concurrent sessions

```sql
-- Session A is actively running a banking package with package package variables
-- DBA recompiles the package in Session B:
ALTER PACKAGE banking_pkg COMPILE BODY;
```

**Observed symptom:** Session A's next call crashes with `ORA-04068: existing state of packages has been discarded; ORA-04061: existing state of package body has been invalidated`.

**(a)** What is package state in Oracle PL/SQL, and where is it stored?

**(b)** Why does compiling a package body invalidate the session memory (UGA/PGA) of all active sessions?

**(c)** How does `PRAGMA SERIALLY_REUSABLE` eliminate package state invalidation for stateless utility packages?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** When a package declares global package variables (variables outside procedures), Oracle allocates state memory in each user's UGA. Recompiling the package invalidates this memory structure across all connected sessions.

**Fix:** Add `PRAGMA SERIALLY_REUSABLE;` to the package specification. This frees package state at the end of each database call, preventing cross-call state persistence and eliminating ORA-04068 errors during zero-downtime hot code deployments.

</details>

---

### D5. PL/SQL context switching penalty in row-by-row cursor loops

```
FOR r IN (SELECT id, salary FROM employees) LOOP
    UPDATE employees SET bonus = r.salary * 0.1 WHERE id = r.id;
END LOOP;
```

**Observed symptom:** Processing 200,000 employees takes 45 seconds due to millions of internal context switches.

**(a)** What is a context switch between the PL/SQL runtime engine and the SQL query engine?

**(b)** How does `BULK COLLECT INTO ... LIMIT` with `FORALL` eliminate context switching overhead?

**(c)** What is the single-statement SQL replacement that eliminates PL/SQL altogether?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** A row-by-row cursor loop alternates execution between the PL/SQL procedural engine and the SQL execution engine on every single iteration (200,000 context switches).

**Fix 1 (Single SQL):** `UPDATE employees SET bonus = salary * 0.1;` (0 context switches, executed entirely inside the SQL engine in 0.2 seconds).

**Fix 2 (Batching):** Use `FETCH c BULK COLLECT INTO l_data LIMIT 1000;` followed by `FORALL i IN 1..l_data.COUNT`.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites real storage engine behaviors, configuration directives, and production failure modes.
Open your implementation files and verify the behavior — the fix is not hypothetical, it is in the code you have built.
