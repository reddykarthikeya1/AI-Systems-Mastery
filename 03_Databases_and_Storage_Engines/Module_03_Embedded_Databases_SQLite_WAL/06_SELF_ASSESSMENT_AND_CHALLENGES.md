# Module 03 Embedded Databases SQLite WAL: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Embedded Databases: SQLite & WAL Architecture** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **How does SQLite Write-Ahead Logging (WAL) differ from the default ROLLBACK journal mode?** How does SQLite Write-Ahead Logging (WAL) differ from the default ROLLBACK journal mode?
2. **Can readers block writers in SQLite WAL mode?** Can readers block writers in SQLite WAL mode?
3. **What does PRAGMA synchronous = NORMAL guarantee in WAL mode?** What does PRAGMA synchronous = NORMAL guarantee in WAL mode?
4. **What causes a -wal file to grow indefinitely?** What causes a -wal file to grow indefinitely?
5. **What is a WAL checkpoint?** What is a WAL checkpoint?
6. **Why must custom scalar functions in SQLite be registered per database connection?** Why must custom scalar functions in SQLite be registered per database connection?
7. **What does PRAGMA busy_timeout = 5000 do?** What does PRAGMA busy_timeout = 5000 do?
8. **How does SQLite enforce single-writer concurrency across multiple operating system processes?** How does SQLite enforce single-writer concurrency across multiple operating system processes?
9. **What is the .shm file accompanying a SQLite WAL database?** What is the .shm file accompanying a SQLite WAL database?
10. **When should you NOT use SQLite in production?** When should you NOT use SQLite in production?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
In WAL mode, changes are appended to a separate -wal file, allowing concurrent readers to read from the main database while a writer appends frames.

#### Answer 2:
No. Readers never block writers, and writers never block readers.

#### Answer 3:
It guarantees durability across application crashes, and calls fsync during checkpoints, providing an optimal balance of safety and speed.

#### Answer 4:
An active long-running read transaction holds an open read snapshot, preventing the checkpoint from truncating older frames.

#### Answer 5:
The process of copying committed frame pages from the -wal file back into the primary .db file and resetting log pointers.

#### Answer 6:
SQLite stores function pointers in the in-memory connection object (C struct), not on disk in the database file.

#### Answer 7:
It instructs SQLite to sleep and retry for up to 5,000 ms before returning SQLITE_BUSY when encountering a locked database.

#### Answer 8:
Using operating system file-level byte-range locks on the database and WAL index file (.shm).

#### Answer 9:
A shared-memory index file mapping WAL frame numbers to database page numbers for fast $O(1)$ reader lookups.

#### Answer 10:
For high-volume multi-node distributed systems, network file systems (NFS), or write workloads exceeding hundreds of concurrent writers.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Benchmark single-threaded write throughput across DELETE vs TRUNCATE vs WAL journal modes.

### 🚀 Challenge 2: Architect Stretch Problem
Implement a custom SQLite C/Python aggregate function that computes rolling variance in a single pass.

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

### D1. SQLite WAL file growing into gigabytes without truncating

```python
import sqlite3, time
conn_write = sqlite3.connect("app.db")
conn_write.execute("PRAGMA journal_mode=WAL;")

# Connection 2 starts an unclosed read transaction
conn_read = sqlite3.connect("app.db")
cur = conn_read.cursor()
cur.execute("SELECT * FROM large_table WHERE id = 1")
# Reader never calls commit(), rollback(), or close()!

# Writer continues appending 1,000,000 transactions
for i in range(100_000):
    conn_write.execute("INSERT INTO audit VALUES (?)", (i,))
    conn_write.commit()
```

**Observed symptom:** `app.db-wal` grows to 4.2 GB; `PRAGMA wal_checkpoint(TRUNCATE)` returns `(0, 524288, 1)` and fails to shrink the file.

**(a)** Why does an open reader cursor prevent SQLite from checkpointing and truncating the WAL file?

**(b)** What does the return tuple `(busy, log_frames, checkpointed_frames)` signify in `wal_checkpoint`?

**(c)** What defensive architectural pattern guarantees SQLite read cursors do not leak snapshots?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** SQLite WAL mode operates via lock-free snapshots. When a reader begins a transaction, it records its read mark (the newest WAL frame at that instant). Checkpointing can only copy and truncate frames up to the oldest active read mark. The unclosed reader pins the checkpoint boundary, forcing all subsequent writes to grow the WAL file indefinitely.

**Return tuple:** `(0, 524288, 1)` indicates: `busy=0` (checkpoint completed), `log_frames=524288` total WAL frames exist, but only `checkpointed_frames=1` could be safely flushed past the stalled reader.

**Defensive Fix:** Always wrap read queries in Python context managers (`with sqlite3.connect(...) as conn:` or `try...finally: cur.close()`) to ensure read transactions are released immediately.

</details>

---

### D2. Database locked error under concurrent multi-process writes

```python
# Two worker processes write to the same SQLite database simultaneously
db = sqlite3.connect("tasks.db")
db.execute("INSERT INTO job_queue (task) VALUES ('process_image')")
```

**Observed symptom:** Worker 2 crashes with `sqlite3.OperationalError: database is locked` after 0.001 seconds.

**(a)** What is SQLite's default lock acquisition timeout when encountering write contention?

**(b)** What PRAGMA command configures SQLite to sleep and retry before returning SQLITE_BUSY?

**(c)** How does WAL mode improve concurrency for readers while preserving the single-writer invariant?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** SQLite's default `busy_timeout` is 0 milliseconds. When Worker 2 attempts an exclusive write lock while Worker 1 holds it, SQLite raises `SQLITE_BUSY` (`database is locked`) immediately.

**Fix:** Set busy timeout on connection creation: `PRAGMA busy_timeout = 5000;` or `sqlite3.connect('tasks.db', timeout=5.0)`. SQLite will perform progressive backoff sleeps up to 5 seconds before erroring.

**WAL Concurrency:** In WAL mode, writers append to the `-wal` log without blocking readers reading from the main `.db` file, though writes remain single-threaded.

</details>

---

### D3. Foreign Key constraints silently ignored in SQLite

```
conn = sqlite3.connect("shop.db")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY);")
conn.execute("CREATE TABLE orders (order_id INT, user_id INT REFERENCES users(id));")
conn.execute("INSERT INTO orders VALUES (101, 99999);") -- User 99999 does not exist!
conn.commit()
```

**Observed symptom:** The invalid order is committed successfully without raising an IntegrityError.

**(a)** Why does SQLite default to ignoring foreign key references?

**(b)** Which command must be executed on every newly established SQLite database connection?

**(c)** Which Python sqlite3 connection hook ensures this PRAGMA runs automatically for connection pools?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** For historical backward compatibility with SQLite 2.x and early 3.x, SQLite has **foreign key enforcement disabled by default**.

**Fix:** Must execute `PRAGMA foreign_keys = ON;` immediately after opening each connection.

**Pool Hook:** In SQLAlchemy or raw connection pools, attach a connect listener: `cursor.execute('PRAGMA foreign_keys=ON')`.

</details>

---

### D4. Silent database corruption over Network File System (NFS/SMB)

```python
# SQLite database placed on AWS EFS or Windows SMB shared network folder
conn = sqlite3.connect(r"\network_share\storage\prod.db")
```

**Observed symptom:** After two weeks of multi-client writes, `PRAGMA integrity_check` reports `*** in database main *** Page 104 is never used, Tree 208 page 208 has bad flags`.

**(a)** Why do POSIX advisory locks fail to function reliably over network file shares (NFS/SMB)?

**(b)** What happens to the SQLite Shared Memory file (`-shm`) over network drives in WAL mode?

**(c)** What is SQLite's official guidance regarding multi-writer setups on network storage?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Network File Systems (NFS/SMB) frequently provide buggy, delayed, or broken byte-range file locking implementations. Two clients simultaneously believe they hold exclusive locks, resulting in simultaneous uncoordinated disk writes and catastrophic B-Tree corruption.

**WAL -shm failure:** In WAL mode, SQLite uses mmap on `-shm` to coordinate readers and writers; mmap over network shares is notoriously incoherent across different client kernels.

**Official Guidance:** SQLite is an embedded database designed for local disk storage. For network-attached multi-client storage, use client-server databases like PostgreSQL or MySQL.

</details>

---

### D5. Missing commit() call leaving database in active transaction

```python
def record_audit(event: str):
    conn = sqlite3.connect("audit.db")
    conn.execute("INSERT INTO events (msg) VALUES (?)", (event,))
    conn.close() # Script exits cleanly
```

**Observed symptom:** Script finishes with exit code 0, but `SELECT COUNT(*) FROM events` returns 0; no rows were written.

**(a)** Why does Python's `sqlite3` driver fail to persist rows when `close()` is called without `commit()`?

**(b)** What is the transaction management behavior difference between Python's default isolation level and `autocommit=True`?

**(c)** What context manager pattern guarantees atomic commit on success and rollback on exception?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Python's `sqlite3` module operates in implicit transaction mode (`isolation_level=''` by default). When a DML statement (`INSERT`) is executed, it opens a transaction, but `close()` rolls back uncommitted transactions by default.

**Fix:** Use connection as a context manager: `with conn: conn.execute(...)`, which issues `conn.commit()` on clean exit and `conn.rollback()` on exception.

**Autocommit:** In Python 3.12+, `sqlite3.connect('audit.db', autocommit=True)` disables implicit transactions, matching standard SQLite CLI behavior.

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
