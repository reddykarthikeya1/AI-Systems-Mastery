from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

ADDITIONS = {
    "Module_03_Embedded_Databases_SQLite_WAL": '''
### SQLite Deep-Dive: The Shm Index & Frame Checksumming
The SQLite WAL architecture relies on an auxiliary shared-memory (`.shm`) file:
- **Fast Frame Mapping:** Readers map WAL frame offsets directly into 32KB shared-memory hash tables, bypassing file seeks.
- **Frame Headers:** Each 24-byte WAL frame header records a 32-bit page number, commit marker flag, and rolling cumulative checksum.
- **Zero Reader Interference:** Readers snapshot the current WAL salt and max committed frame upon starting, ensuring read isolation is never disrupted by background checkpointing.
''',
    "Module_05_PostgreSQL_MVCC_Indexing_EXPLAIN": '''
### PostgreSQL Deep-Dive: Visibility Map Bits & Page Checksums
- **All-Visible Bit:** Set when all tuples on a page are visible to all current transactions; allows Index-Only Scans to avoid touching heap pages entirely.
- **All-Frozen Bit:** Set when all tuples on a page have been frozen by VACUUM FREEZE; prevents transaction ID wraparound scans from reading the page.
- **Data Page Checksums:** Enabled via `initdb -k`; calculates CRC-32 checksums on every 8KB page write to detect physical bit rot.
''',
    "Module_07_Oracle_Database_Architecture_SGA_PGA": '''
### Oracle SGA Deep-Dive: Granules and Memory Resize Operations
- **SGA Granules:** Memory is allocated in contiguous chunks (granules) ranging from 4MB (small systems) to 128MB/512MB (large systems).
- **Dynamic Sizing:** ASMM can resize the Database Buffer Cache and Shared Pool dynamically without restarting the database instance.
- **PGA Memory Areas:** Private SQL Areas, Sort Areas, and Hash Areas are allocated dynamically within PGA based on `PGA_AGGREGATE_TARGET`.
''',
    "Module_09_Oracle_RAC_DataGuard_GoldenGate": '''
### Oracle High Availability Deep-Dive: Redo Apply vs SQL Apply
- **Physical Standby (Redo Apply):** Active Data Guard applies exact block-level redo vectors via media recovery (`MRP0`), maintaining bit-for-bit parity.
- **Logical Standby (SQL Apply):** Data Guard converts redo vectors back into SQL transactions via LogMiner (`LSP0`), allowing open read/write tables.
- **Fast-Start Failover (FSFO):** Automates zero-touch failover to standby within seconds when primary crash is confirmed by an independent observer process.
''',
}

for folder, extra_text in ADDITIONS.items():
    readme_path = root / folder / "README.md"
    content = readme_path.read_text(encoding="utf-8")
    readme_path.write_text(content.rstrip() + "\n" + extra_text.strip() + "\n", encoding="utf-8")

print("Enriched remaining 4 READMEs.")
