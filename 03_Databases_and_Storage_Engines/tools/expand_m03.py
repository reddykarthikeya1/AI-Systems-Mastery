from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")
m03_readme = root / "Module_03_Embedded_Databases_SQLite_WAL" / "README.md"
content = m03_readme.read_text(encoding="utf-8")

extra = '''
### Production WAL Checkpointing Strategies: PASSIVE vs RESTART vs TRUNCATE
In mission-critical embedded deployments, choosing the proper checkpointing pragma is critical:
- **`PRAGMA wal_checkpoint(PASSIVE);`**: Checkpoints as many frames as possible without blocking active readers or writers. If a reader is open on an older frame, it pauses at that frame.
- **`PRAGMA wal_checkpoint(FULL);`**: Blocks subsequent writers until all active readers complete, flushing all frames to the main database file.
- **`PRAGMA wal_checkpoint(RESTART);`**: Similar to FULL, but ensures subsequent writers begin writing at frame 1 of the WAL file.
- **`PRAGMA wal_checkpoint(TRUNCATE);`**: Flushes all frames and truncates the `-wal` file to zero bytes on disk, reclaiming operating system storage.
'''

m03_readme.write_text(content.rstrip() + "\n" + extra.strip() + "\n", encoding="utf-8")
print("Module 03 expanded.")
