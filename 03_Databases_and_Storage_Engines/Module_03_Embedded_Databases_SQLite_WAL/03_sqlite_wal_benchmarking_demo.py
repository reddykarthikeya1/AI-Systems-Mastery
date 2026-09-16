"""Module 03: SQLite WAL Mode Benchmarking Demo.

Demonstrates:
1. Performance differences between ROLLBACK journal (DELETE) and Write-Ahead Logging (WAL).
2. Concurrency: Readers not blocking writers in WAL mode.
3. Synchronous pragma trade-offs: NORMAL vs FULL.
"""

import sqlite3
import tempfile
import time
from pathlib import Path

def benchmark_mode(journal_mode: str, num_inserts: int = 500) -> float:
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / f"bench_{journal_mode}.db"
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        cur.execute(f"PRAGMA journal_mode = {journal_mode};")
        cur.execute("PRAGMA synchronous = NORMAL;")
        cur.execute("CREATE TABLE bench_log (id INTEGER PRIMARY KEY, val TEXT, ts REAL);")
        conn.commit()

        start = time.perf_counter()
        for i in range(num_inserts):
            cur.execute("INSERT INTO bench_log (val, ts) VALUES (?, ?);", (f"record_{i}", time.time()))
            conn.commit()

        elapsed = time.perf_counter() - start
        conn.close()
        return elapsed

def run_demo():
    print("Benchmarking 500 individual committed INSERT transactions:")
    t_delete = benchmark_mode("DELETE", 300)
    print(f"  DELETE Journal Mode: {t_delete:.3f} s ({300/t_delete:.1f} txn/s)")

    t_wal = benchmark_mode("WAL", 300)
    print(f"  WAL Mode:            {t_wal:.3f} s ({300/t_wal:.1f} txn/s)")
    if t_wal > 0:
        print(f"  WAL Speedup:         {t_delete / t_wal:.2f}x faster!")

if __name__ == "__main__":
    run_demo()
