# 🐛 Global Database Debugging Playbook: Decoding Errors into Plain English

> *"A database never crashes without telling you why. It speaks through error codes, lock wait graphs, and execution plans."*

When your database queries crash, time out, or hang indefinitely, **do not panic**. Database error messages are extraordinarily informative once you understand their vocabulary.

This playbook decodes the **Top 10 Most Common Database Errors** across PostgreSQL, Oracle, MySQL, MongoDB, Redis, and Cassandra into plain human English, complete with side-by-side buggy code vs clean production fixes.

---

## 🔍 The Top 10 Database Errors Decoded

### 1. Connection Pool Exhaustion (`OperationalError: connection slots exhausted`)
* **What it means in human terms:** Every connection to a database consumes server RAM (~10MB per connection in Postgres). Your application opened too many concurrent connections without closing them or without using a connection pool, so the database rejected new connections.
* **The Buggy Anti-Pattern:**
  ```python
  # ❌ BROKEN: Opening a new raw connection for every single incoming web request
  def handle_request():
      conn = psycopg.connect("dbname=app")  # Leaks connections under high traffic!
      ...
  ```
* **The Production Fix:** Use an asynchronous connection pool with a fixed size:
  ```python
  # ✅ FIXED: Share a pre-warmed connection pool across all requests
  pool = psycopg_pool.AsyncConnectionPool(conninfo="dbname=app", min_size=5, max_size=20)
  async with pool.connection() as conn:
      ...
  ```

---

### 2. Lock Wait Timeout (`LockWaitTimeoutException` / `canceling statement due to statement timeout`)
* **What it means in human terms:** Transaction A locked a row with `UPDATE` or `SELECT FOR UPDATE` and went to sleep or started a slow network call. Transaction B wanted to update the same row, waited in line, and eventually timed out.
* **The Golden Rule:** **Never perform external network HTTP calls or long file I/O inside an active database transaction!** Keep transactions open for microseconds, not seconds.

---

### 3. Deadlock (`DeadlockDetected: deadlock detected`)
* **What it means in human terms:**
  - Transaction 1 locks Row A and requests Row B.
  - Transaction 2 locks Row B and requests Row A.
  - Both transactions freeze waiting for the other. The database detects this circular dependency and intentionally kills one of them.
* **The Production Fix (Consistent Locking Order):**
  Always acquire locks in the **exact same sorted order** across your entire codebase:
  ```python
  # ✅ FIXED: Always lock rows in ascending order of IDs!
  account_ids = sorted([sender_id, receiver_id])
  cursor.execute("SELECT * FROM accounts WHERE id IN (%s, %s) ORDER BY id FOR UPDATE", account_ids)
  ```

---

### 4. Serialization Failure (`could not serialize access due to concurrent update`)
* **What it means in human terms:** You are running under `SERIALIZABLE` or `REPEATABLE READ` isolation. Another transaction updated the data you were reading before you could finish your transaction.
* **The Production Fix (Automatic Retry Loop):**
  Serialization failures are normal in strict isolation! You must wrap serializable transactions in an exponential backoff retry loop:
  ```python
  # ✅ FIXED: Retry loop for serialization errors
  for attempt in range(max_retries):
      try:
          with conn.transaction():
              run_business_logic(conn)
          break
      except psycopg.errors.SerializationFailure:
          time.sleep(0.05 * (2 ** attempt))
  ```

---

### 5. The Fatal N+1 Query Trap
* **What it means in human terms:** You fetch 100 users with 1 query, then loop over each user to fetch their orders in 100 individual queries. Total queries: $1 + 100 = 101$. Your application grinds to a halt.
* **The Fix:** Use a single SQL `JOIN` or modern ORM eager loading:
  ```python
  # ❌ BROKEN: N+1 queries
  users = session.execute(select(User)).scalars()
  for u in users:
      print(u.orders)  # Triggers 100 separate queries!

  # ✅ FIXED: 1 single query with eager loading
  users = session.execute(select(User).options(selectinload(User.orders))).scalars()
  ```

---

### 6. Full Table Scan on Million-Row Tables (The Accidental Invalidation Trap)
* **What it means in human terms:** You created a B-Tree index on `email`, but your query takes 5 seconds because you wrapped the column in a function:
  ```sql
  -- ❌ BROKEN: Function wrapping invalidates the standard B-Tree index!
  SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';
  ```
* **The Production Fix:**
  Either search the exact value or create a **Functional Index**:
  ```sql
  -- ✅ FIXED: Create an expression index
  CREATE INDEX idx_users_lower_email ON users (LOWER(email));
  ```

---

### 7. MongoDB: Document Size Exceeded (`BSONObjectTooLarge: > 16777216 bytes`)
* **What it means in human terms:** MongoDB strictly limits a single document to **16MB**. You used an unbounded array inside a document (e.g. embedding 500,000 sensor logs inside a single user document).
* **The Production Fix:** Use the **Bucket Pattern** or normalize into separate documents:
  Instead of 1 document with 500,000 logs, split into documents containing 500 logs each (bucketed by hour/day).

---

### 8. Redis: Out of Memory (`OOM command not allowed when used memory > 'maxmemory'`)
* **What it means in human terms:** Redis ran out of RAM, and its `maxmemory-policy` is set to `noeviction` (which refuses writes).
* **The Production Fix:**
  Configure a sensible eviction policy in `redis.conf`:
  ```text
  maxmemory 4gb
  maxmemory-policy allkeys-lru  # Automatically evicts Least Recently Used keys!
  ```

---

### 9. Cassandra: `UnavailableException` / `ReadTimeoutException`
* **What it means in human terms:** You requested a query with `ConsistencyLevel.QUORUM`, but enough nodes in the replica set are offline or unresponsive that a mathematical quorum ($N/2 + 1$) cannot be achieved.
* **The Production Fix:** Check node status with `nodetool status`, check for high garbage collection pauses on nodes, or adjust consistency to `LOCAL_QUORUM` for multi-datacenter setups.

---

### 10. Oracle: `ORA-01555: snapshot too old`
* **What it means in human terms:** You ran a query that took 30 minutes to complete. Meanwhile, other transactions modified the blocks you needed, and the old version of the data in the **UNDO tablespace** was overwritten before your slow query could read it.
* **The Production Fix:** Tune the query so it finishes in seconds instead of minutes, increase the `UNDO_RETENTION` parameter, and increase the size of the `UNDO` tablespace.
