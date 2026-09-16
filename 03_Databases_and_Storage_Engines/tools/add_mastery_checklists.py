#!/usr/bin/env python3
"""Append a per-module "You have mastered this when..." checklist to each PROJECT_GUIDE.

Why this is a script and not 24 hand edits: the *structure* is uniform (a
checklist of observable capabilities) while the *content* is entirely
module-specific. The capabilities below are written per module by hand; the
script only handles placement and idempotency.

A mastery item must name something the learner can **do or explain**, never a
topic they have "covered". "Understands MVCC" is unobservable. "Can predict
which of two concurrent transactions will see a row, and say why" is testable.

Usage::

    python tools/add_mastery_checklists.py            # apply
    python tools/add_mastery_checklists.py --check    # report coverage only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEADING = "## 5. You Have Mastered This Module When You Can…"

# module-number -> (list of observable capabilities)
MASTERY: dict[str, list[str]] = {
    "01": [
        "Explain what `fsync` actually guarantees, and what it does not",
        "Describe the exact failure window in which a crash loses a committed write",
        "Explain why a write-ahead log makes recovery possible, from first principles",
        "Name the four ACID properties and give a concrete failure for each when it is absent",
        "Predict what a reader sees mid-write in a non-atomic file update",
        "Explain why appending is safer than overwriting in place",
        "Recover a deliberately truncated WAL and say which records survive",
        "Argue when a plain file is genuinely sufficient instead of a database",
    ],
    "02": [
        "Write a window function with the right frame clause without consulting docs",
        "Explain the difference between `ROW_NUMBER`, `RANK` and `DENSE_RANK` on tied values",
        "Rewrite a correlated subquery as a join and say which the planner prefers",
        "Explain when a CTE is materialised and when it is inlined",
        "Predict the row count of any join type before executing it",
        "Use `GROUPING SETS` instead of a UNION of three aggregate queries",
        "Spot why `WHERE` cannot filter on a window function and use `QUALIFY`/subquery instead",
        "Read a query you did not write and state its output shape",
    ],
    "03": [
        "Explain what WAL mode changes about reader/writer concurrency in SQLite",
        "Say what `PRAGMA synchronous` trades away at each level",
        "Explain why an open write transaction blocks a WAL checkpoint",
        "Predict which concurrent operation will raise `database is locked`",
        "Register a Python function as a SQL function and know its performance cost",
        "Read `EXPLAIN QUERY PLAN` and say whether an index was used",
        "Argue when SQLite is the correct production choice, and when it is not",
    ],
    "04": [
        "Choose between `JSONB`, a column, and a separate table for a given field",
        "Explain why `JSONB` needs a GIN index and what `@>` does without one",
        "Predict whether a value will be TOASTed, and verify with `pg_column_size`",
        "Write an `EXCLUDE` constraint that prevents overlapping ranges",
        "Explain the storage difference between `json` and `jsonb`",
        "Say when an array column is right and when it is a normalisation failure",
        "Read `EXPLAIN` output and confirm your index is actually being used",
    ],
    "05": [
        "Explain MVCC without using the word 'snapshot' as a synonym for itself",
        "Say what `xmin` and `xmax` mean on a concrete row version",
        "Explain why a long-running read transaction blocks `VACUUM`",
        "Diagnose table bloat from `pg_stat_user_tables` and act on it",
        "Predict which of two concurrent transactions sees a given row, and why",
        "Distinguish `VACUUM`, `VACUUM FULL` and `autovacuum` by their locking behaviour",
        "Read `EXPLAIN (ANALYZE, BUFFERS)` and identify the dominant cost",
        "Explain why an index-only scan is possible only when the visibility map is current",
    ],
    "06": [
        "Explain the InnoDB clustered index and why the primary key choice matters so much",
        "Trace a secondary-index lookup through its bookmark to the clustered index",
        "Read the deadlock section of `SHOW ENGINE INNODB STATUS`",
        "Explain how row-based binlog replication differs from statement-based",
        "Build a CDC consumer and explain its at-least-once semantics",
        "Say why a UUID primary key hurts InnoDB more than an auto-increment one",
        "Explain what the redo log and the doublewrite buffer each protect against",
    ],
    "07": [
        "Draw the Oracle SGA and name what lives in each pool",
        "Explain the difference between the buffer cache and the shared pool",
        "Say what PGA memory is used for and why it is per-session",
        "Query `V$` views to answer a real capacity question",
        "Explain what a checkpoint does and why it bounds recovery time",
        "Distinguish an instance from a database in Oracle terminology",
    ],
    "08": [
        "Write a PL/SQL package with a spec and body, and say why they are separate",
        "Explain why `BULK COLLECT` + `FORALL` beats a row-by-row loop, with numbers",
        "Say when a trigger is the right tool and when it is a maintenance trap",
        "Handle an exception in PL/SQL without swallowing the original error",
        "Explain what a cursor is and when to use an explicit one",
        "Describe how LOBs are stored and why they need different handling",
    ],
    "09": [
        "Explain what RAC shares and what it does not",
        "Distinguish physical from logical standby in Data Guard",
        "Explain the trade-off between maximum protection and maximum performance mode",
        "Describe how a client reconnects after a node failure",
        "Say what GoldenGate does that Data Guard cannot",
        "Explain split-brain and how the cluster prevents it",
    ],
    "10": [
        "Decide embed-vs-reference for a given access pattern and defend it",
        "State the BSON document size limit and what to do when you approach it",
        "Explain why an unbounded array field is a modelling error",
        "Create a TTL index and explain when the reaper actually runs",
        "Read `explain()` and tell `COLLSCAN` from `IXSCAN`",
        "Explain how a compound index's field order constrains which queries it serves",
    ],
    "11": [
        "Write an aggregation pipeline and explain each stage's memory behaviour",
        "Say when `allowDiskUse` is required and what it costs",
        "Explain what a change stream guarantees and what it does not",
        "Choose a shard key and explain how a bad one creates a hot partition",
        "Explain read preference and the staleness it can introduce",
        "Describe what happens to writes during a replica-set election",
    ],
    "12": [
        "Explain why Redis is single-threaded and why that is a feature",
        "Describe the SDS layout and why Redis does not use C strings",
        "Explain how a skip list gives O(log n) rank queries",
        "State the difference between RDB and AOF persistence and their failure modes",
        "Explain why `KEYS` is banned in production and what to use instead",
        "Build a correct distributed lock and name the failure mode of a naive one",
        "Explain each `maxmemory-policy` and pick one for a given workload",
        "Show, with measurement, why pipelining beats N round-trips",
    ],
    "13": [
        "Explain what Sentinel does and what it cannot protect against",
        "Say why Lua scripts are atomic in Redis and when that matters",
        "Explain hash slots and how a cluster resharding moves them",
        "Describe what `WAIT` guarantees about replication",
        "Explain why Redis replication is asynchronous by default and the data-loss window",
        "Use Streams consumer groups with `XAUTOCLAIM` for crash recovery",
    ],
    "14": [
        "Explain why Cassandra has no primary node and what that buys",
        "Design a partition key from a query, not from an entity",
        "Explain tunable consistency and compute R+W>N for a given setup",
        "Say what a tombstone is and why too many destroy read performance",
        "Explain hinted handoff and read repair",
        "Predict which queries a given table can and cannot serve",
    ],
    "15": [
        "Explain the LSM write path from memtable to SSTable",
        "Describe why LSM trees favour writes and B+ trees favour reads",
        "Explain what compaction does and the space/write amplification trade-off",
        "Design a DynamoDB single-table schema for two access patterns",
        "Explain why `Scan` is almost always the wrong choice",
        "Compute the read/write capacity a described workload needs",
        "Explain how a bloom filter avoids unnecessary SSTable reads",
    ],
    "16": [
        "Write a Cypher traversal and explain what it does to the index",
        "Explain index-free adjacency and why it makes traversals cheap",
        "Express a recursive query in Cypher and in SQL, and compare",
        "Read `PROFILE` output and reduce the db-hits count",
        "Model a domain as nodes and relationships, choosing where properties live",
        "Argue when a graph database is the wrong choice",
    ],
    "17": [
        "Explain why columnar storage compresses better than row storage",
        "Predict which queries benefit from columnar and which do not",
        "Explain what a MergeTree does in the background",
        "Query a Parquet file without loading it and say why that is possible",
        "Choose a compression codec and justify it from measured ratios",
        "Explain why OLAP and OLTP want opposite physical layouts",
    ],
    "18": [
        "Explain an inverted index and how a term lookup resolves to documents",
        "Describe what an analyzer does to text at index time versus query time",
        "Explain BM25 scoring and read an `explain` output",
        "Say why the default `text` mapping breaks aggregations, and fix it",
        "Explain what a refresh interval trades away",
        "Design a mapping for a given search requirement",
    ],
    "19": [
        "Explain what an embedding is and why cosine distance is the usual metric",
        "Compare HNSW and IVFFlat on build time, memory, and recall",
        "Explain what recall means for an approximate index and how to measure it",
        "Decide between `pgvector` and a dedicated vector database, with reasons",
        "Combine a metadata filter with a vector search and explain the cost",
        "Explain why a cryptographic hash cannot serve as an embedding",
    ],
    "20": [
        "Draw a B+ tree node and explain why the fan-out determines the depth",
        "Compute the height of a B+ tree for a given row count and page size",
        "Explain why leaf nodes are linked and what that enables",
        "Describe a page split and its cost",
        "Explain why B+ trees suit reads and LSM trees suit writes",
        "Say why the database page size and the disk block size interact",
    ],
    "21": [
        "Read `EXPLAIN (ANALYZE)` and find where estimates diverge from actuals",
        "Explain how the planner uses statistics and what `ANALYZE` refreshes",
        "Say why a function wrapping an indexed column prevents index use, and fix it",
        "Predict when the planner will pick a nested loop over a hash join",
        "Explain what an index-only scan requires",
        "Diagnose a query that was fast at 10k rows and slow at 10M",
        "Decide against adding an index and justify it by write cost",
    ],
    "22": [
        "Name the four ANSI isolation levels and the anomaly each permits",
        "Demonstrate a dirty read, a non-repeatable read, and a phantom",
        "Explain write skew and why only `SERIALIZABLE` prevents it",
        "Handle a serialisation failure correctly in application code",
        "Explain why two transactions locking rows in opposite order deadlock",
        "Describe how Raft elects a leader and commits an entry",
        "Explain why consensus needs a majority and what happens at exactly half",
    ],
    "23": [
        "Perform a backup and verify the restore, not just the backup",
        "Explain point-in-time recovery and what WAL archiving requires",
        "Run a zero-downtime schema change using expand/contract",
        "Compute an RTO and RPO for a described backup strategy",
        "Promote a replica and explain what happens to in-flight writes",
        "Explain why a backup that restores but loses a sequence value is a failed backup",
        "Design a migration that is safe to run twice",
    ],
    "24": [
        "Choose the right engine for each part of a polyglot system, with reasons",
        "Explain the dual-write problem and implement the outbox pattern",
        "Say why distributed transactions across engines are usually the wrong answer",
        "Design a saga with compensating actions for a multi-store operation",
        "Explain how you keep a cache and a system of record consistent",
        "Diagnose which store is responsible for an observed inconsistency",
        "Defend a decision to use *one* database instead of five",
    ],
}


def guide_for(module_dir: Path) -> Path:
    return module_dir / "PROJECT_GUIDE.md"


def build_block(number: str) -> str:
    items = MASTERY.get(number)
    if not items:
        return ""
    lines = [
        "",
        "---",
        "",
        HEADING,
        "",
        "Mastery is a capability, not a topic you have read about. Tick an item only",
        "if you could do it right now, on a whiteboard, without notes.",
        "",
    ]
    lines += [f"- [ ] {item}" for item in items]
    lines += [
        "",
        "If more than two are unticked, the material is not finished with you yet -",
        "go back to the module's demos and the Track B live implementation.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report coverage, change nothing")
    args = parser.parse_args()

    modules = sorted(p for p in ROOT.glob("Module_*") if p.is_dir())
    have = added = missing = 0

    for module_dir in modules:
        number = module_dir.name.split("_")[1]
        guide = guide_for(module_dir)
        if not guide.exists():
            print(f"  {module_dir.name}: no PROJECT_GUIDE.md")
            missing += 1
            continue

        text = guide.read_text(encoding="utf-8")
        if HEADING in text or "mastered this module when" in text.lower():
            have += 1
            continue

        block = build_block(number)
        if not block:
            print(f"  {module_dir.name}: no mastery items defined for module {number}")
            missing += 1
            continue

        if not args.check:
            guide.write_text(text.rstrip() + "\n" + block, encoding="utf-8")
        added += 1

    verb = "would add" if args.check else "added"
    print(f"already present: {have} | {verb}: {added} | missing definition: {missing}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
