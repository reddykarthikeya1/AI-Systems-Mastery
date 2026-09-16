# Module 01: Self-Assessment Quiz & Mastery Challenges

Test your understanding of storage theory, ACID properties, relational algebra, and normalization before moving to **Module 02**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Storage Bottleneck:** Why does searching for a row in a raw CSV file take $O(N)$ time while an indexed database lookup takes $O(\log N)$ time?
2. **ACID - Atomicity:** What does "Atomicity" guarantee when a multi-step transaction encounters a disk error halfway through?
3. **ACID - Durability:** What physical mechanism allows databases to guarantee Durability even if the power is abruptly cut immediately after a `COMMIT`?
4. **Relational Theory:** What is the formal difference between a **Tuple**, an **Attribute**, and a **Relation** in Codd's Relational Model?
5. **Relational Algebra:** Which relational operator corresponds to SQL `SELECT * WHERE price > 100`, and which corresponds to `SELECT name, email`?
6. **1NF Violation:** Why does a column `hobbies` storing `"reading, gaming, hiking"` violate First Normal Form (1NF)?
7. **2NF Violation:** When does a table that is in 1NF violate Second Normal Form (2NF)?
8. **3NF Violation:** What is a "transitive dependency", and how does it lead to update anomalies?
9. **Concurrency:** What is a "Lost Update", and why does it occur when two transactions execute concurrent read-modify-write cycles?
10. **Torn Pages:** What is a "Torn Page", and how do modern relational database engines protect against it during sudden crashes?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
A raw CSV has no pre-sorted index structure; the operating system must sequentially read every single line from beginning to end ($O(N)$ linear scan). An indexed database organizes search keys into balanced tree structures (like B+ Trees) where each node traversal eliminates half the remaining search space, enabling $O(\log N)$ lookups.

#### Answer 2:
Atomicity guarantees "all-or-nothing". If an error occurs midway, all preceding modifications made by that transaction are completely undone (rolled back) to leave the database in its exact pre-transaction state.

#### Answer 3:
The database flushes transaction intentions and data changes to a sequential **Write-Ahead Log (WAL)** on non-volatile storage *before* returning a success acknowledgment. Upon power restoration, the engine reads the WAL to replay any committed transactions that had not yet reached the primary tables.

#### Answer 4:
- **Relation:** The table itself (a mathematical set of unique tuples).
- **Tuple:** A single row / record in the relation.
- **Attribute:** A named column representing a specific domain/data type.

#### Answer 5:
- `SELECT * WHERE price > 100` corresponds to the **Selection ($\sigma$)** operator.
- `SELECT name, email` corresponds to the **Projection ($\pi$)** operator.

#### Answer 6:
1NF mandates that all column values must be **atomic** (indivisible). Storing a comma-separated list of multiple values in a single cell violates 1NF. It should be decomposed into a separate related table (e.g. `user_hobbies` with 1 hobby per row).

#### Answer 7:
A 1NF table violates 2NF when it has a **composite primary key** (a key made of 2+ columns) and a non-key column depends on only *part* of that primary key (a partial key dependency).

#### Answer 8:
A transitive dependency occurs when non-key column A determines non-key column B (e.g., `zip_code` $\rightarrow$ `city`). If the same zip code is repeated across 10,000 rows, updating the city in 9,999 rows leaves 1 inconsistent row—an update anomaly.

#### Answer 9:
A Lost Update occurs when two transactions read the same initial value, compute an update in memory, and then write back to disk. The second write completely overwrites and obliterates the changes made by the first write.

#### Answer 10:
A Torn Page occurs when a power outage interrupts a multi-sector disk write (e.g. only 4KB of an 8KB page was physically flushed to magnetic/flash media). Engines protect against this by keeping full page copies in write-ahead logs or using doublewrite buffers.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Normalizing a Messy Hospital Spreadsheet

**Goal:** Write a Python function that takes a list of denormalized dictionaries representing hospital visits and decomposes them into **3 normalized relations** (Patients, Doctors, Visits) in 3NF:

```python
raw_records = [
    {"patient_id": 1, "patient_name": "Alice", "doctor_id": 101, "doctor_name": "Dr. House", "doctor_specialty": "Diagnostics", "visit_date": "2026-01-10"},
    {"patient_id": 1, "patient_name": "Alice", "doctor_id": 102, "doctor_name": "Dr. Watson", "doctor_specialty": "General", "visit_date": "2026-01-15"},
    {"patient_id": 2, "patient_name": "Bob", "doctor_id": 101, "doctor_name": "Dr. House", "doctor_specialty": "Diagnostics", "visit_date": "2026-02-01"},
]
```

<details>
<summary><b>Solution Code</b></summary>

```python
def normalize_hospital_records(records: list[dict]) -> tuple[dict, dict, list]:
    patients = {}
    doctors = {}
    visits = []

    for r in records:
        # Extract unique patients
        patients[r["patient_id"]] = {"id": r["patient_id"], "name": r["patient_name"]}
        
        # Extract unique doctors (eliminating transitive specialty duplicates)
        doctors[r["doctor_id"]] = {
            "id": r["doctor_id"],
            "name": r["doctor_name"],
            "specialty": r["doctor_specialty"]
        }
        
        # Normalized visits table linking foreign keys
        visits.append({
            "patient_id": r["patient_id"],
            "doctor_id": r["doctor_id"],
            "visit_date": r["visit_date"]
        })

    return patients, doctors, visits
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Transitive dependency causing partial update anomaly

```sql
-- Updating user office location in denormalized employee table
UPDATE employees 
SET office_city = 'San Francisco' 
WHERE emp_id = 101;
-- 50 other employees work in the same office building (office_id = 'BLDG-B')
```

**Observed symptom:** Queries grouping by office_city report fragmented stats: BLDG-B is split between 'SF' and 'San Francisco'.

**(a)** Which normal form does this schema violate, and what is the functional dependency chain?

**(b)** How do you decompose the relation to achieve 3NF?

**(c)** What database constraint prevents orphaned office records after decomposition?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Violates **Third Normal Form (3NF)** due to a transitive dependency: `emp_id -> office_id -> office_city`. Non-key attribute `office_city` depends on non-key attribute `office_id` rather than the primary key `emp_id`.

**Fix:** Decompose into two tables: `employees(emp_id, name, office_id)` with foreign key `office_id REFERENCES offices(office_id)`, and `offices(office_id, office_city)`.

**Constraint:** A `FOREIGN KEY (office_id) REFERENCES offices(office_id) ON UPDATE CASCADE ON DELETE RESTRICT` guarantees referential integrity.

</details>

---

### D2. Lost Update under concurrent Read-Modify-Write

```python
# Thread A and Thread B concurrently executing balance increment:
cur.execute("SELECT balance FROM accounts WHERE id = %s", (acc_id,))
bal = cur.fetchone()[0]
new_bal = bal + deposit_amount
cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_bal, acc_id))
```

**Observed symptom:** Two concurrent deposits of $100 both read $500 initial balance; final balance is $600 instead of $700.

**(a)** Why did Thread B overwrite Thread A's deposit without throwing a concurrency error?

**(b)** What is the single-statement SQL atomic fix?

**(c)** If multi-statement logic is required, which locking clause must be appended to the SELECT?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Lost Update anomaly under Read Committed isolation. Both transactions read snapshot state $500, calculate $600 locally, and the second `UPDATE` blindsides the first write without conflict detection.

**Fix:** Use atomic in-place mutation: `UPDATE accounts SET balance = balance + %s WHERE id = %s`.

**Locking alternative:** Use pessimistic row-level locking: `SELECT balance FROM accounts WHERE id = %s FOR UPDATE`, forcing Thread B to block until Thread A commits.

</details>

---

### D3. Torn Page vulnerability during unbuffered power loss

```python
# Storage engine writes 8KB database pages using standard OS write()
with open("data.db", "r+b") as f:
    f.seek(page_offset)
    f.write(modified_page_bytes)  # 8192 bytes
    f.flush()  # Power loss happens halfway through disk controller flush!
```

**Observed symptom:** On restart, the page contains corrupted header checksums; 4096 bytes are new data and 4096 bytes are old sector data.

**(a)** Why does `write()` of 8KB fail to guarantee atomicity at the physical drive level?

**(b)** How does MySQL InnoDB protect against this specific failure using the doublewrite buffer?

**(c)** How does PostgreSQL protect against torn pages in its WAL stream?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Hard drive sector write atomicity is physically limited to 512 bytes or 4KB (Advanced Format). Writing an 8KB or 16KB database page requires multiple hardware sector writes; power loss during intermediate sectors yields a **Torn Page**.

**InnoDB Fix:** InnoDB writes pages first to a contiguous sequential **Doublewrite Buffer** on disk before writing to data files. If a crash occurs during data file write, the page is restored intact from the doublewrite buffer.

**PostgreSQL Fix:** PostgreSQL writes **Full Page Images (FPI)** to WAL on the first modification to a page following a checkpoint (`full_page_writes = on`).

</details>

---

### D4. 1NF Violation: Storing comma-separated tags in relational column

```sql
SELECT * FROM products WHERE tags LIKE '%electronics%';
```

**Observed symptom:** Query requires a full table scan; indexes on `tags` are bypassed; partial string matches false-positive on 'microelectronics' and 'consumer-electronics-repair'.

**(a)** What rule of First Normal Form (1NF) is violated by the `tags` column?

**(b)** What are the severe performance and query limitations of matching CSV strings via LIKE?

**(c)** What are the two standard relational architectures for resolving this schema defect?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Violates 1NF, which dictates that every column must contain **atomic (indivisible) values**. Comma-separated strings encode multi-valued repeating groups.

**Limitations:** Wildcard prefix `%term%` prevents B-Tree index range scans, forcing $O(N)$ table scans, and cannot enforce uniqueness or referential integrity on tag tokens.

**Relational Fixes:** Either (1) create a normalized junction table `product_tags(product_id, tag_id)` with foreign keys and compound primary key, or (2) use native PostgreSQL array types with GIN indexing: `tags text[], WHERE tags @> ARRAY['electronics']`.

</details>

---

### D5. Dirty read anomaly under READ UNCOMMITTED isolation

```sql
-- Session 1 (Fraudulent transaction):
BEGIN;
UPDATE accounts SET balance = balance - 10000 WHERE id = 1;
-- Network glitch / validation fails -> ROLLBACK;

-- Session 2 (Concurrent credit check running concurrently before rollback):
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT balance FROM accounts WHERE id = 1; -- Sees balance deducted!
```

**Observed symptom:** Session 2 grants a loan based on the uncommitted balance reduction; Session 1 rolls back, leaving invalid loan approvals.

**(a)** What is a Dirty Read, and why is it permitted in READ UNCOMMITTED?

**(b)** What is the minimum ANSI SQL transaction isolation level that eliminates Dirty Reads?

**(c)** How does MVCC in modern PostgreSQL/MySQL prevent dirty reads without locking readers?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** In READ UNCOMMITTED, readers inspect dirty memory buffers in the buffer pool without checking transaction commit status (`xmax` or commit bits), reading transient uncommitted mutations.

**Fix:** Elevate isolation level to at least **READ COMMITTED**.

**MVCC Mechanics:** In PostgreSQL and InnoDB, readers construct a snapshot based on active transaction IDs (`Snapshot.active_xids`). Any tuple version created by an uncommitted transaction (`xmin` in active list) is invisible to readers, directing them to the previous committed tuple version without taking read locks.

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
