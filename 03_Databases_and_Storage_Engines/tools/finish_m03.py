from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")
m03_readme = root / "Module_03_Embedded_Databases_SQLite_WAL" / "README.md"
content = m03_readme.read_text(encoding="utf-8")

extra = '''
### Architectural Summary
- Concurrency Model: 1 exclusive writer, N concurrent readers without blocking.
- Checkpoint Modes: PASSIVE, FULL, RESTART, TRUNCATE.
- Recovery Mechanism: On-disk WAL frame replay with rolling cumulative checksums.
'''

m03_readme.write_text(content.rstrip() + "\n" + extra.strip() + "\n", encoding="utf-8")
print("Module 03 expanded.")
