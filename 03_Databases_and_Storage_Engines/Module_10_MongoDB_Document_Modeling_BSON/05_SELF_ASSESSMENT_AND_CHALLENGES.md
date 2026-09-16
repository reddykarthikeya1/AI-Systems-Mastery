# Module 10 MongoDB Document Modeling BSON: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **MongoDB Document Modeling & BSON Wire Protocol** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is the 16MB document size limit in MongoDB, and what architectural pattern addresses it?** What is the 16MB document size limit in MongoDB, and what architectural pattern addresses it?
2. **Explain the structural components of a 12-byte BSON ObjectId.?** Explain the structural components of a 12-byte BSON ObjectId.
3. **When should you Embed vs Reference related data in MongoDB?** When should you Embed vs Reference related data in MongoDB?
4. **What is a TTL (Time-To-Live) index in MongoDB?** What is a TTL (Time-To-Live) index in MongoDB?
5. **How does schema validation work in MongoDB?** How does schema validation work in MongoDB?
6. **What is the difference between $set, $inc, and $push update operators?** What is the difference between $set, $inc, and $push update operators?
7. **Why is an atomic findAndModify/findOneAndUpdate preferred over find-then-update?** Why is an atomic findAndModify/findOneAndUpdate preferred over find-then-update?
8. **What does the stage 'COLLSCAN' indicate in MongoDB query explain output?** What does the stage 'COLLSCAN' indicate in MongoDB query explain output?
9. **How does BSON differ from standard JSON?** How does BSON differ from standard JSON?
10. **What is the Extended Reference pattern in document modeling?** What is the Extended Reference pattern in document modeling?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
MongoDB caps single BSON documents at 16MB. The Time-Series Bucket Pattern or 1:N referencing solves unbounded array growth.

#### Answer 2:
4 bytes unix epoch timestamp, 5 bytes random value unique to machine/process, and 3 bytes incrementing counter.

#### Answer 3:
Embed for 1:1 or bounded 1:N relationships accessed together atomically; Reference for unbounded 1:N or M:N relationships updated independently.

#### Answer 4:
A single-field index on a date field that automatically deletes documents after a specified number of seconds via a background reaper thread.

#### Answer 5:
Collections can enforce validation rules using JSON Schema (`$jsonSchema`) with strict or moderate enforcement levels.

#### Answer 6:
`$set` updates/adds a field; `$inc` atomically increments a numeric field; `$push` appends an item to an array.

#### Answer 7:
It eliminates race conditions by reading and updating the document in a single atomic database operation.

#### Answer 8:
A collection scan (every document read into RAM) indicating a missing or unused index.

#### Answer 9:
BSON is a binary serialization format supporting rich data types (Date, ObjectId, BinData, Int64, Decimal128) and faster field traversal.

#### Answer 10:
Embedding only the most frequently read fields of a referenced document (e.g. customer name) while keeping the full entity in a referenced collection.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Benchmark single-document read throughput for 1:50 embedded items vs 50 separate referenced queries.

### 🚀 Challenge 2: Architect Stretch Problem
Create a strict JSON Schema validated collection rejecting invalid schema insertions.

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

### D1. Document exceeding MongoDB 16MB BSON size limit

```python
# IoT sensor schema storing unbounded array of readings inside device doc:
db.sensors.update_one(
    {"_id": "sensor_99"},
    {"$push": {"readings": {"timestamp": datetime.now(), "temp": 24.5}}}
)
```

**Observed symptom:** After 6 months of operation, application crashes with `pymongo.errors.WriteError: BSONObj size: 16793610 (0x100400A) is invalid. Size must be between 0 and 16793600(16MB)`.

**(a)** What is MongoDB's hard maximum BSON document size limit, and why was it chosen?

**(b)** What schema design anti-pattern causes unbounded array growth in document databases?

**(c)** How does the Time-Series Bucketing Pattern (e.g. one document per sensor per hour) resolve this limit?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** MongoDB enforces a hard **16 MB BSON document size limit** to prevent memory bloat in the WiredTiger cache and avoid network socket saturation. Storing unbounded arrays inside a single document guarantees eventual failure.

**Fix:** Use the **Bucketing Pattern**: create one document per hour/day with a fixed pre-allocated array of up to 60 readings (e.g., `_id: "sensor_99:2026-03-08:14"`), or store each reading as an individual document in a dedicated time-series collection.

</details>

---

### D2. ObjectId generation timestamp drift under unsynchronized clocks

```python
# Server A clock is running 15 minutes ahead due to NTP failure
doc_id_a = ObjectId() # Generated on Server A
doc_id_b = ObjectId() # Generated on Server B (accurate clock)
# Sorting documents by _id:
docs = list(db.orders.find().sort("_id", 1))
```

**Observed symptom:** Orders created on Server A appear in the future; real-time order processing queues process orders completely out of chronological sequence.

**(a)** What are the four components encoded within a standard 12-byte MongoDB `ObjectId`?

**(b)** Why does ObjectId timestamp generation depend on local server operating system clocks?

**(c)** What separate monotonically increasing sequence or distributed timestamp authority should be used when strict global ordering is required?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** The first 4 bytes of a 12-byte `ObjectId` represent a Unix epoch timestamp (in seconds) read from the local machine clock. If machine clocks drift, ObjectIds generated on different servers lose monotonic global ordering.

**ObjectId Structure:** 4-byte timestamp + 5-byte random value (machine/process identifier) + 3-byte incrementing counter.

**Fix:** Ensure NTP/Chrony synchronizes all app servers to within milliseconds. For strict business sequencing, generate cluster-wide monotonic IDs using a counter collection or Snowflake ID generator.

</details>

---

### D3. BSON integer type coercion causing silent numeric precision loss

```python
# Python driver writing integer into MongoDB:
large_balance = 5_000_000_000 # 5 Billion (requires 64-bit int)
db.accounts.insert_one({"user": "corp", "balance": large_balance})

# Downstream Node.js / Python service reads balance with 32-bit driver:
doc = db.accounts.find_one({"user": "corp"})
```

**Observed symptom:** Balance is read as `705032704` (overflow wrapped) or throws `BSONTypeError: value out of bounds`.

**(a)** What is the difference between BSON type `` (double), `` (int32), and `` (int64)?

**(b)** How does Python's dynamic arbitrary-precision integer model interact with strict BSON wire types?

**(c)** What BSON type must be used when storing monetary values requiring exact decimal precision?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** BSON distinguishes between 32-bit signed integers (`int32`, max 2.14B) and 64-bit signed integers (`int64`, max 9.22E18). If an integer exceeds $2^{31}-1$, it must be explicitly encoded as `int64`. In languages without native 64-bit integers (e.g. JavaScript Number), precision is lost.

**Monetary Precision:** Always use **BSON Decimal128** (`NumberDecimal` / `bson.decimal128.Decimal128`) for financial balances to prevent floating-point and integer truncation errors.

</details>

---

### D4. Compound index prefix mismatch causing COLLSCAN

```sql
-- Collection has compound index on (status, created_at, customer_id)
db.orders.create_index([("status", 1), ("created_at", -1), ("customer_id", 1)])

-- Query issued by user dashboard:
db.orders.find({"customer_id": "cust_42", "created_at": {"$gte": start_date}}).explain("executionStats")
```

**Observed symptom:** `executionStages.stage` reports `COLLSCAN`; query examines 2,000,000 documents instead of using the index.

**(a)** What is the Golden Rule of compound index prefixing in B-Tree / MongoDB indexes?

**(b)** Why does omitting `status` prevent the query planner from using the index?

**(c)** What index definition satisfies the Equality, Sort, Range (ESR) rule for this query?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** B-Tree compound indexes can only be utilized if query filters include the **index prefix**. Since the query omits the leading column `status`, the database cannot traverse the compound B-Tree and falls back to a full collection scan (`COLLSCAN`).

**ESR Rule Fix:** Create an index matching Equality, Sort, Range: `db.orders.create_index([('customer_id', 1), ('created_at', -1)])`.

</details>

---

### D5. Unindexed array field search causing multi-key explosion

```python
# Query filtering on embedded array tags without multikey index:
db.articles.find({"tags": "distributed-systems"})
```

**Observed symptom:** Under 5,000 concurrent queries, WiredTiger cache fills with un-indexed document scans; memory usage hits 95%.

**(a)** What is a Multikey Index in MongoDB, and how does it index array fields?

**(b)** What restriction prevents creating compound multikey indexes where two fields are both arrays?

**(c)** Which test in the test suite verifies BSON serialization and collection indexing?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Querying an array element without an index forces a full collection scan where every document's array is unpacked and scanned in memory.

**Fix:** Create a multikey index: `db.articles.create_index({'tags': 1})`. MongoDB automatically creates an index entry for every individual element in the array.

**Multikey Restriction:** A compound multikey index cannot have more than one field that is an array (to prevent exponential Cartesian product entry explosion in index B-Trees).

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
