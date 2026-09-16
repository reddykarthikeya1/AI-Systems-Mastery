# Module 01: Troubleshooting, Common Bugs & Storage Traps

Here are the most frequent pitfalls, concurrency traps, and design bugs encountered in storage theory, ACID properties, and relational normalization, along with deep explanations and production fixes.

---

## 1. The "Lost Update" Concurrency Trap

### The Bug
Two concurrent processes read account balance `$1,000`. Both deposit `$100`. The final balance in your database or file is `$1,100` instead of `$1,200`!

### Why It Happens
This is the classic **Lost Update Anomaly**:
```text
Process A reads balance: $1,000
Process B reads balance: $1,000
Process A adds $100 -> writes $1,100 to disk
Process B adds $100 -> overwrites $1,100 to disk! (Process A's update is completely lost!)
```

### The Fix
Never use disconnected read-then-write loops. Use an atomic database update statement with locking or database-level arithmetic:
```sql
-- ✅ ATOMIC: Handled directly in the database engine with row locks!
UPDATE accounts SET balance = balance + 100 WHERE id = 1;
```

---

## 2. Torn Pages & Partial Disk Writes

### The Bug
Your power flickered, and upon restarting your application, your database file fails to open or throws `CorruptDatabaseError`.

### Why It Happens
Operating systems write data to hard drives in **4KB disk sectors** (or database pages). If a database page is 8KB, writing it requires writing two 4KB sectors. If power is cut halfway, only half of the page was written to the disk. This is called a **Torn Page**.

### The Fix
Modern relational databases (PostgreSQL, SQLite, MySQL) protect against torn pages using **Doublewrite Buffers** (MySQL) or **Full-Page Writes** in the Write-Ahead Log (PostgreSQL). If a page is torn upon restart, the recovery process restores the clean version from the WAL before applying transactions.

---

## 3. The 3NF Transitive Dependency Trap

### The Bug
Designing an `orders` table that includes:
`[order_id, customer_id, customer_email, customer_zip_code, customer_city]`

### Why It Happens
This table violates **Third Normal Form (3NF)** because of a **Transitive Dependency**:
- `order_id` $\rightarrow$ determines `customer_id`.
- `customer_id` $\rightarrow$ determines `customer_city`.
- `customer_zip_code` $\rightarrow$ determines `customer_city`.

If a customer changes their city, or if a zip code is mislabeled, updating it across 50,000 historic orders leads to update anomalies and inconsistent data.

### The Fix
Decompose into two normalized tables with a Foreign Key:
1. `customers` table: `[customer_id, email, zip_code, city]`
2. `orders` table: `[order_id, customer_id, order_date, total_amount]`
