# Debug Lab: Module 22 — Native Extensions & Rust Traps

## How to Run
```bash
python debug_lab/broken_extension.py
```

## Observed Symptoms
1. **GIL Starvation of concurrent threads**:
   Native CPU loops without `py.allow_threads` hold Python's Global Interpreter Lock, freezing GUI, heartbeat, and network threads.
2. **Debug build performance regression**:
   Running without `--release` in cargo/maturin produces native code that runs up to 10× slower than optimized Rust.
