# Module 22: Troubleshooting & Edge Cases

Native extensions fail in ways pure Python never does: link errors, ABI mismatches, silently wrong numbers. Every entry below is a real error message with its real cause.

**All of these were hit while building this module's own solution.** They are not hypothetical.

---

## 1. `ImportError: dynamic module does not define module export function`

```
ImportError: dynamic module does not define module export function (PyInit_accelerator)
```

**The #1 first-time PyO3 error.** CPython looks for a symbol named `PyInit_<module>`. PyO3 generates that symbol from your `#[pymodule]` **function name** — which must match `lib.name` in `Cargo.toml`.

```toml
# Cargo.toml
[lib]
name = "rust_accelerator"       # ← this
```
```rust
// src/lib.rs
#[pymodule]
fn rust_accelerator(...)        // ← must be identical
```

**Fix:** make the three names agree — `Cargo.toml` `lib.name`, the `#[pymodule]` fn name, and what you type in `import`.

---

## 2. `LNK1104: cannot open file '...\build_script_build.exe'` (Windows + OneDrive)

```
error: linking with `link.exe` failed: exit code: 1104
= note: LINK : fatal error LNK1104: cannot open file
  'C:\Users\...\OneDrive\<synced folder>\...\target\release\build\...\build_script_build.exe'
```

**Cause:** the crate lives inside a **cloud-synced folder** (OneDrive, Dropbox, iCloud). OneDrive's filesystem filter locks and virtualises files mid-write; the MSVC linker cannot create its output. Antivirus real-time scanning causes the identical symptom.

**Fix — redirect the build directory outside the synced folder:**

```powershell
# PowerShell (persist it for the session)
$env:CARGO_TARGET_DIR = "$env:LOCALAPPDATA\cargo-target"
cargo build --release
```

```bash
# Git Bash / WSL
export CARGO_TARGET_DIR="$LOCALAPPDATA/cargo-target"
```

Make it permanent in `~/.cargo/config.toml`:

```toml
[build]
target-dir = "C:/Users/<you>/AppData/Local/cargo-target"
```

**Why this matters beyond Rust:** any toolchain that writes many small files fast — `node_modules`, `.venv`, Docker build contexts — suffers the same way inside OneDrive/Dropbox/iCloud. Keep build artifacts out of synced folders as a standing rule.

---

## 3. "PyO3 didn't help — it's barely faster than Python"

**Cause, ~90% of the time: you forgot `--release`.**

```bash
maturin develop            # ✗ DEBUG build: no optimisation, overflow checks on
maturin develop --release  # ✓ opt-level=3 + LTO
```

A debug build is routinely **10–50x slower** than release and can genuinely lose to pure Python. Confirm what you actually built:

```python
>>> import rust_accelerator, time
>>> t=time.perf_counter(); rust_accelerator.count_primes(150_000); print(time.perf_counter()-t)
0.0037     # release
0.15       # debug — rebuild with --release
```

**Second cause:** FFI overhead on tiny workloads. Each boundary crossing costs ~100–200 ns. Below roughly 10,000 elements the crossing can cost more than the work. Find your crossover point (Tier 3 challenge 3.3) rather than assuming Rust always wins.

---

## 4. `attempt to multiply with overflow` (panics in debug, wrong answers in release)

```
thread '<unnamed>' panicked at src/lib.rs:12:
attempt to multiply with overflow
```

Rust checks integer overflow in debug builds and **wraps silently** in release. A hash function that relies on wrapping must say so:

```rust
hash = hash * 0x100000001b3;              // ✗ panics in debug
hash = hash.wrapping_mul(0x100000001b3);  // ✓ explicit intent
```

Also available: `checked_mul` (returns `Option`), `saturating_mul` (clamps), `overflowing_mul` (value + flag). Pick deliberately — this is Rust making you state what Python's arbitrary-precision ints let you ignore.

> **Nasty variant:** debug passes, release gives wrong numbers, and your tests
> only run in one mode. Test both, or always use the explicit method.

---

## 5. `PanicException` reaching Python

```
pyo3_runtime.PanicException: index out of bounds: the len is 3 but the index is 5
```

A Rust panic crossing the FFI boundary becomes `PanicException` — which does **not** inherit from `ValueError` or `TypeError`, so ordinary `except ValueError` will not catch it.

**Treat every `PanicException` as a bug in your extension**, not as control flow. Return `PyResult` and an explicit error instead:

```rust
// ✗ panics
fn get(v: Vec<f64>, i: usize) -> f64 { v[i] }

// ✓ raises IndexError in Python
fn get(v: Vec<f64>, i: usize) -> PyResult<f64> {
    v.get(i).copied().ok_or_else(|| PyIndexError::new_err(format!("index {i} out of range")))
}
```

A panic while the GIL is released can also abort the process outright, which is why `panic = "abort"` in a release profile needs thought.

---

## 6. Stale extension: your edits appear to do nothing

You changed `lib.rs`, rebuilt, and the old behaviour persists.

**Causes and fixes:**

| Cause | Fix |
| :--- | :--- |
| Python cached the loaded module | Restart the interpreter. You **cannot** meaningfully `importlib.reload` a native module |
| A Jupyter kernel is holding the old `.pyd` | Restart the kernel; on Windows the file is locked while loaded |
| An old copy shadows the new one | `python -c "import rust_accelerator as m; print(m.__file__)"` — is that the path you just built? |
| `maturin develop` targeted a different environment | Confirm with `python -c "import sys; print(sys.prefix)"` |

On Windows, a loaded `.pyd` cannot be overwritten. `maturin develop` will fail with a permission error while any process still has it open — including a stray notebook kernel.

---

## 7. `error: linker 'cc' not found` / `link.exe not found`

Rust needs a **system linker**, which it does not bundle.

| Platform | Fix |
| :--- | :--- |
| Windows | Install "Visual Studio Build Tools" → *Desktop development with C++* |
| Debian/Ubuntu | `sudo apt install build-essential` |
| Fedora/RHEL | `sudo dnf install gcc` |
| macOS | `xcode-select --install` |

---

## 8. Wheel builds but will not install: `not a supported wheel on this platform`

```
ERROR: rust_accelerator-1.0.0-cp312-cp312-win_amd64.whl is not a supported wheel on this platform
```

You built for a different Python version or architecture than the one installing it. The `abi3` feature is the durable fix:

```toml
pyo3 = { version = "0.23", features = ["extension-module", "abi3-py311"] }
```

The filename then reads `...-cp311-abi3-win_amd64.whl` and installs on **3.11, 3.12, 3.13, 3.14…** without rebuilding.

Check what you produced:

```bash
ls target/wheels/
# rust_accelerator-1.0.0-cp311-abi3-win_amd64.whl   ← good
# rust_accelerator-1.0.0-cp311-cp311-win_amd64.whl  ← version-locked
```

---

## 9. `test_gil_is_actually_released` fails

```
AssertionError: 4 threads took 480ms vs 120ms for one -
the GIL does not appear to be released
```

**Cause 1 — you omitted `py.allow_threads`.** The Rust body runs while holding the GIL, so threads serialise exactly like pure Python. Wrap the compute in the closure.

**Cause 2 — you are on a 1–2 core machine.** With fewer cores than threads there is no parallelism to find. Check `python -c "import os; print(os.cpu_count())"`; the test allows 3.0x precisely to tolerate 2-core CI runners, but a single-core VM cannot pass it.

**Cause 3 — the closure captured a Python object.** Then it will not compile at all; if you worked around the borrow checker by cloning data *into* Python types, you have re-acquired the GIL. The closure must be pure Rust.

---

## 10. Silently wrong results from `ctypes` (no error at all)

The most dangerous failure in this module, because nothing raises:

```python
libm.cbrt.restype = ctypes.c_int      # WRONG — cbrt returns a double
libm.cbrt(27.0)                       # returns garbage, no exception
```

Without `argtypes`/`restype`, ctypes assumes every argument and the return value are `int`. On a float function you get reinterpreted bytes — plausible-looking numbers that are simply wrong.

**Rule: always declare both**, on every function, before the first call.

```python
libm.cbrt.argtypes = [ctypes.c_double]
libm.cbrt.restype = ctypes.c_double
```

[Demo 1](06_ctypes_honest_demo.py) shows both the broken and correct declaration side by side.

---

## 11. Edge case: `&[u8]` vs `Vec<u8>` — a silent 2x memory cost

```rust
fn hash_borrowed(data: &[u8]) -> u64 { ... }   // ✓ borrows; zero copies
fn hash_owned(data: Vec<u8>) -> u64 { ... }    // ✗ COPIES the whole buffer
```

Both compile and both give correct answers. On a 100 MB payload the second allocates a second 100 MB. Prefer borrowed slices for read-only input; take ownership only when you must mutate or retain the data.

---

## 12. Edge case: `f64` accumulation order changes results

`test_rust_dot_product_matches_python` uses `pytest.approx`, not `==`, on purpose. Rust's iterator `sum()` and Python's `sum()` may accumulate in a different order, and floating-point addition is not associative:

```python
>>> 0.1 + 0.2 + 0.3 == 0.1 + (0.2 + 0.3)
False
```

**Never assert exact equality across two float implementations.** Use `pytest.approx` with an explicit tolerance. (Module 01 introduced this; here it has real consequences.)

---

## 13. Free-threaded Python (3.13t+) and your extension

On a free-threaded build there is no GIL to release. Extensions must opt in:

```rust
#[pymodule(gil_used = false)]
fn rust_accelerator(m: &Bound<'_, PyModule>) -> PyResult<()> { ... }
```

Without that declaration, CPython re-enables the GIL at import time and prints a warning — silently erasing the benefit of the free-threaded build for the whole process. `py.allow_threads` remains valid and becomes a no-op, so the code in this module is forward-compatible; only the module declaration changes.

---

## 🔍 Diagnostic Checklist

Work top to bottom when something is wrong:

```bash
rustc --version                                     # 1. toolchain present?
echo $CARGO_TARGET_DIR                              # 2. build dir outside OneDrive?
cargo build --release 2>&1 | tail -5                # 3. does Rust alone compile?
maturin develop --release                           # 4. does packaging succeed?
python -c "import rust_accelerator as m; print(m.__file__)"   # 5. right file?
python -c "import rust_accelerator as m; print(dir(m))"       # 6. symbols exported?
pytest project_solution/test_native_accelerator.py -m "not perf" -q   # 7. correct?
pytest project_solution/test_native_accelerator.py -m perf -v         # 8. fast?
```

If step 4 succeeds but step 5 shows an unexpected path, you have two installs. `pip uninstall rust-accelerator` and rebuild.
