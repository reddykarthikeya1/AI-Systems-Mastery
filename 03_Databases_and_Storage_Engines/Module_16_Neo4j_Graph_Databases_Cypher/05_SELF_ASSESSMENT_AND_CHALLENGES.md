# Module 16 Neo4j Graph Databases Cypher: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Graph Databases: Neo4j & Declarative Cypher** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is Index-Free Adjacency in graph databases?** What is Index-Free Adjacency in graph databases?
2. **How does Cypher's declarative pattern matching syntax model relationships?** How does Cypher's declarative pattern matching syntax model relationships?
3. **Why are graph databases significantly faster than relational databases for deep multi-hop queries?** Why are graph databases significantly faster than relational databases for deep multi-hop queries?
4. **What does the `shortestPath()` function in Cypher compute?** What does the `shortestPath()` function in Cypher compute?
5. **How do you detect circular fraud rings in Cypher?** How do you detect circular fraud rings in Cypher?
6. **What is the difference between Cypher PROFILE and EXPLAIN?** What is the difference between Cypher PROFILE and EXPLAIN?
7. **What is a 'Supernode' in a property graph, and what operational challenge does it create?** What is a 'Supernode' in a property graph, and what operational challenge does it create?
8. **What is the difference between node labels and relationship types?** What is the difference between node labels and relationship types?
9. **How does PageRank centrality measure node importance in a graph?** How does PageRank centrality measure node importance in a graph?
10. **Can relationships in a property graph have properties?** Can relationships in a property graph have properties?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
Each node maintains direct memory/disk pointers to its adjacent neighbor relationships, enabling $O(1)$ step traversals independent of total graph size.

#### Answer 2:
Using ASCII art syntax: `(start:Label)-[:REL_TYPE {prop: val}]->(end:Label)`.

#### Answer 3:
Relational databases must compute expensive join tables on primary/foreign keys ($O(N \log N)$), while graphs traverse pre-linked pointers ($O(K)$).

#### Answer 4:
It uses Breadth-First Search (BFS) to find the minimum-hop relationship path between two nodes.

#### Answer 5:
Using variable-length cyclic paths: `MATCH (a:Account)-[:TRANSFERRED*3..6]->(a) RETURN a`.

#### Answer 6:
EXPLAIN shows planner operator estimates without running; PROFILE executes the query and reports actual DB hits, rows, and memory.

#### Answer 7:
A node with millions of edges; traversing or locking it causes severe latency spikes and memory pressure.

#### Answer 8:
Labels group nodes into sets/classes (can have multiple per node); relationship types define the single specific semantic edge connecting two nodes.

#### Answer 9:
It iteratively calculates the probability that a random walk across edges will land on a specific node.

#### Answer 10:
Yes. In property graphs, edges can store arbitrary key-value properties (e.g. `since`, `weight`, `distance`).

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Write a Cypher query detecting circular financial laundering rings across bank accounts.

### 🚀 Challenge 2: Architect Stretch Problem
Implement an in-memory graph engine computing BFS shortest paths across 10,000 vertices.

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

### D1. Cartesian Product from Disconnected MATCH Clauses

```cypher
// Cypher query to find products bought by coworkers
MATCH (u:User {id: $userId})
MATCH (c:User)
WHERE c.department = u.department AND c.id <> u.id
MATCH (p:Product)
WHERE (c)-[:BOUGHT]->(p)
RETURN p.name, count(c) as coworkers_count
```

**Observed symptom:** Query takes 42 seconds for a graph with only 50,000 nodes. Neo4j logs show query warning: 'This query builds a Cartesian product between disconnected patterns'.

**(a)** What is a Cartesian product in Cypher query planning, and where did it occur in this query?

**(b)** How can you view the query execution plan in Cypher using `EXPLAIN` and `PROFILE`?

**(c)** How should the query be rewritten to express relationship traversals directly without Cartesian joins?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In the query, `MATCH (p:Product)` is declared as an independent pattern disconnected from `(c:User)` before the WHERE clause is evaluated. Cypher's query planner executes a Cartesian product (`CartesianProduct` operator) combining every node in set `c` with every node in set `p` before filtering by the relationship. If there are 1,000 coworkers and 20,000 products, it evaluates $1,000 	imes 20,000 = 20,000,000$ combinations in memory.

**Diagnostic Commands:**
1. Prepend `EXPLAIN` or `PROFILE` in Neo4j Browser or `cypher-shell`:
   ```cypher
   PROFILE
   MATCH (u:User {id: $userId})
   MATCH (c:User)
   WHERE c.department = u.department AND c.id <> u.id
   MATCH (p:Product)
   WHERE (c)-[:BOUGHT]->(p)
   RETURN p.name, count(c);
   ```
2. Look for the red `CartesianProduct` operator in the execution tree.

**Production Fix:**
Express the relationship traversal directly in a single connected `MATCH` pattern:
```cypher
MATCH (u:User {id: $userId})
MATCH (u)-[:WORKS_IN]->(d:Department)<-[:WORKS_IN]-(c:User)
WHERE c.id <> u.id
MATCH (c)-[:BOUGHT]->(p:Product)
RETURN p.name, count(DISTINCT c) AS coworkers_count;
```
This uses pointer-hopping index-free adjacency instead of full-table scanning and Cartesian products.

</details>

---

### D2. Unbounded Variable-Length Path Traversal OOM

```cypher
// Cypher query to check if two users are connected in a social network
MATCH (a:User {email: 'alice@example.com'}), (b:User {email: 'bob@example.com'})
MATCH path = (a)-[:FOLLOWS*]-(b)
RETURN path
LIMIT 1;
```

**Observed symptom:** Neo4j server JVM crashes with java.lang.OutOfMemoryError: Java heap space. All active database transactions are killed.

**(a)** Why does `[:FOLLOWS*]` cause exponential path explosion even with `LIMIT 1`?

**(b)** How do you set transaction execution timeouts in `neo4j.conf`?

**(c)** How should shortest-path algorithms or bounded hops be used instead?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
`[:FOLLOWS*]` specifies an unbounded variable-length path traversal across bidirectional edges. In a graph with cycles and high connectivity, the number of possible paths between two nodes grows exponentially $O(d^k)$ with degree $d$ and depth $k$. Even though `LIMIT 1` is present, the depth-first search or breadth-first search path matcher enumerates millions of cyclic paths into heap memory before locating a path that satisfies all criteria.

**Diagnostic Commands:**
1. Inspect query logs in `logs/query.log` to identify queries exceeding memory thresholds.
2. Check memory allocations:
   ```bash
   neo4j-admin server status
   ```

**Production Fix:**
1. **Always bound path length:**
   ```cypher
   MATCH path = (a)-[:FOLLOWS*1..4]-(b)
   RETURN path LIMIT 1;
   ```
2. **Use shortestPath() algorithm:**
   Neo4j has specialized bidirectional breadth-first search algorithms that prune paths immediately:
   ```cypher
   MATCH (a:User {email: 'alice@example.com'}), (b:User {email: 'bob@example.com'})
   MATCH path = shortestPath((a)-[:FOLLOWS*..6]->(b))
   RETURN path;
   ```
3. Guard in `neo4j.conf`:
   ```properties
   dbms.transaction.timeout=10s
   dbms.memory.transaction.global_max_size=4G
   ```

</details>

---

### D3. Supernode Degree Explosion Latency

```cypher
// Node 'Brand_Nike' is connected to 2,500,000 followers
MATCH (u:User {id: $userId})-[:FOLLOWS]->(celebrity:User)<-[:FOLLOWS]-(other:User)
RETURN other.id, count(*) as common_connections
ORDER BY common_connections DESC
LIMIT 10;
```

**Observed symptom:** For regular users with 50 followers, query runs in 4ms. When executed for a user who follows a celebrity/supernode, query runs for 28,000ms with high CPU usage.

**(a)** What is a 'supernode' in graph databases, and why does traversing through a supernode destroy query performance?

**(b)** How can you check the degree (number of relationships) of a node in Cypher before traversing it?

**(c)** What graph modeling patterns (such as relationship filtering, edge bucketing, or sampling) mitigate supernode bottlenecks?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
A **supernode** (or dense node) is a node with an abnormally high degree (e.g., thousands or millions of relationships). Graph databases rely on **index-free adjacency**, following physical relationship pointers stored on the node record. When traversing through a supernode with 2.5 million relationships, the engine must iterate through 2.5 million relationship records in memory, defeating the performance benefits of graph traversals.

**Diagnostic Commands:**
1. Check the degree of high-density nodes:
   ```cypher
   MATCH (u:User {id: $celebrityId})
   RETURN count { (u)<-[:FOLLOWS]-() } AS in_degree;
   ```
2. In `PROFILE`, observe hundreds of thousands of `Expand(All)` rows produced.

**Production Fix:**
1. **Filter by Degree during Traversal:** Do not expand through nodes whose degree exceeds a threshold:
   ```cypher
   MATCH (u:User {id: $userId})-[:FOLLOWS]->(celebrity:User)
   WHERE count { (celebrity)<-[:FOLLOWS]-() } < 50000
   MATCH (celebrity)<-[:FOLLOWS]-(other:User)
   RETURN other.id, count(*)
   LIMIT 10;
   ```
2. **Node Bucketing (Fan-Out Partitioning):** Split the celebrity node into sub-nodes (`Celebrity_Bucket_1`, `Celebrity_Bucket_2`) or maintain pre-aggregated counts and summary relationships instead of raw individual graph edges.

</details>

---

### D4. Cypher Eager Operator Blocking Heap Streaming

```cypher
MATCH (u:User)
WHERE u.active = true
SET u.last_checked = datetime()
WITH u
MATCH (u)-[:OWNS]->(a:Asset)
RETURN u.name, count(a)
```

**Observed symptom:** When executing this query on a database with 2 million users, query execution halts for 35 seconds and Neo4j throws java.lang.OutOfMemoryError: Java heap space. The query does not stream results.

**(a)** What is an `Eager` operator in Cypher, and why did modifying `u.last_checked` introduce an Eager barrier?

**(b)** How do you detect the `Eager` operator in Cypher execution plans?

**(c)** How do you decouple write operations from reads using `CALL { ... } IN TRANSACTIONS` to stream data cleanly?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Cypher protects queries against phantom reads and self-mutation hazards (e.g., updating a node that might be re-matched later in the same query). To prevent this, the planner inserts an **Eager** operator whenever a query alternates between writes (`SET`, `CREATE`, `DELETE`) and subsequent reads/matches. An Eager operator forces Cypher to buffer the entire intermediate result set into JVM heap memory before allowing the next pipeline step to execute, breaking streaming and exhausting heap space.

**Diagnostic Commands:**
1. Run `EXPLAIN` on the query:
   ```cypher
   EXPLAIN
   MATCH (u:User) WHERE u.active = true
   SET u.last_checked = datetime()
   WITH u MATCH (u)-[:OWNS]->(a:Asset) RETURN u.name, count(a);
   ```
2. Inspect the plan for `Eager` or `EagerAggregation` steps.

**Production Fix:**
1. Separate reads from writes, or batch writes using subqueries with periodic transactions:
   ```cypher
   MATCH (u:User) WHERE u.active = true
   CALL {
       WITH u
       SET u.last_checked = datetime()
   } IN TRANSACTIONS OF 10000 ROWS;
   ```
2. Read all data first before issuing writes at the end of the query:
   ```cypher
   MATCH (u:User)-[:OWNS]->(a:Asset)
   WHERE u.active = true
   WITH u, count(a) AS asset_count
   SET u.last_checked = datetime()
   RETURN u.name, asset_count;
   ```

</details>

---

### D5. Duplicate Node Creation Under Concurrent MERGE Without Constraint

```python
# Concurrent Python worker processes
def get_or_create_device(device_uuid: str):
    with driver.session() as session:
        session.run(
            "MERGE (d:Device {uuid: $uuid}) "
            "ON CREATE SET d.created_at = timestamp() "
            "RETURN d",
            uuid=device_uuid
        )

# 20 workers concurrently process telemetry for device 'dev-abc-123'
```

**Observed symptom:** After concurrent execution, querying MATCH (d:Device {uuid: 'dev-abc-123'}) returns 4 duplicate nodes with identical UUIDs.

**(a)** Why does `MERGE` fail to prevent duplicates under concurrent execution without a uniqueness constraint?

**(b)** What internal lock mechanism does Neo4j use when a uniqueness constraint is present vs absent?

**(c)** What Cypher DDL statement guarantees idempotent node creation under concurrency?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
`MERGE` in Cypher is semantically equivalent to: "MATCH the node; if not found, CREATE it". Without a unique constraint or unique index on `:Device(uuid)`, concurrent transactions executing the initial `MATCH` phase will both see that the node does not exist. Both transactions proceed to the `CREATE` step and commit independent nodes. Neo4j only acquires schema locks to enforce uniqueness when a **UNIQUE CONSTRAINT** is defined.

**Diagnostic Commands:**
1. Check existing constraints:
   ```cypher
   SHOW CONSTRAINTS;
   ```
2. Check for duplicates in database:
   ```cypher
   MATCH (d:Device)
   WITH d.uuid AS uuid, count(d) AS cnt, collect(d) AS nodes
   WHERE cnt > 1
   RETURN uuid, cnt;
   ```

**Production Fix:**
Create a unique property constraint on the label and property before running concurrent `MERGE` operations:
```cypher
CREATE CONSTRAINT constraint_device_uuid FOR (d:Device) REQUIRE d.uuid IS UNIQUE;
```
With this constraint active, Neo4j takes an exclusive lock during the `MERGE` operation. Any concurrent transaction attempting to `MERGE` the same `uuid` will wait on the lock and match the newly committed node instead of creating a duplicate.

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
