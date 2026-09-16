# Debug Lab: Module 00 — Tooling & Environment Traps

## How to Run
```bash
python debug_lab/broken_cli.py 5
```

## Observed Symptoms
1. **FileNotFoundError**:
   Running the script from anywhere other than the exact folder containing `config.toml` crashes immediately:
   ```
   FileNotFoundError: [Errno 2] No such file or directory: 'config.toml'
   ```
2. **ImportError / Path Flakiness**:
   `sys.path.append("./src")` fails to resolve `modern_app` when invoked from outside the root directory or when packaged.
3. **Unvalidated CLI Input**:
   Running `python debug_lab/broken_cli.py high` crashes with an unhandled traceback:
   ```
   ValueError: invalid literal for int() with base 10: 'high'
   ```
   Running with `-999` succeeds silently despite negative priorities violating application domain rules.
