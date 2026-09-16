# Debug Lab: Module 07 — Serialization Traps

## How to Run
```bash
python debug_lab/broken_config_migrator.py
```

## Observed Symptoms
1. **UnicodeDecodeError / Character Mangling**:
   Writing and reading UTF-8 characters without `encoding="utf-8"` fails or corrupts characters on Windows environments.
2. **Integer dictionary keys silently converted to strings**:
   `101 in deserialized` evaluates to `False`, because JSON maps keys to `"101"`.
3. **TypeError on timezone-naive vs timezone-aware datetime comparison**:
   ```
   TypeError: can't compare offset-naive and offset-aware datetimes
   ```
