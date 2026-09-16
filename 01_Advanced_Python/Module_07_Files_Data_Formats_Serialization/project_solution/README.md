# Design Rationale: Safe Multi-Format Configuration Migrator

## Architectural Overview
A cross-platform file migration engine providing atomic file writes, strict schema validation, and lossless conversions across JSON, TOML, CSV, and YAML formats.

## Key Design Decisions
1. **Atomic File Swapping via `tempfile` and `os.replace`:** Output files are written to temporary staging files on the same filesystem and swapped atomically, preventing corrupted half-written files during sudden crashes.
2. **`pathlib.Path` Object Model:** Eliminates OS-specific path concatenation bugs (`/` vs `\`) and provides path traversal validation (`is_relative_to`).
3. **Explicit UTF-8 Encoding:** All I/O operations specify `encoding='utf-8'`, preventing Windows system encoding (`cp1252`) crashes when handling non-ASCII content.

## Rejected Alternatives
1. **`pickle` for Configuration Serialization:**
   - *Reason for Rejection:* Deserializing untrusted pickle streams enables Remote Code Execution (RCE) via `__reduce__` execution exploits.
2. **Direct Overwrite (`open(file, 'w')`):**
   - *Reason for Rejection:* Direct writing truncates the existing file immediately. If the process terminates before completion, existing data is permanently destroyed.

## Invariants & Guarantees
- Destination files are never left in an incomplete or corrupted state.
- Path traversal escapes (`../`) outside the target root directory are strictly rejected.

## Verification
```bash
pytest test_config_migrator.py -v
```
