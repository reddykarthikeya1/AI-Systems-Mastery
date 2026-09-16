# Module 22 Project Guide: Build a Real Native Accelerator

**Deliverable:** a compiled Rust extension module that is measurably 20x+ faster than pure Python and releases the GIL, with a pure-Python fallback so the package still works where no wheel exists.

You write the Rust. The tests are already written and they grade you — including a performance test that fails if your "optimisation" is not actually faster.

---

## 🎯 3-Tier Progressive Learning Path

Pick your entry point. Each tier is a complete, working deliverable.

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **1 — Novice Walkthrough** | You have never compiled anything | 3 functions: hash, dot product, module registration | ~2 hrs |
| **2 — Core Project** | Tier 1 passes | GIL release + parallelism measurement | ~2.5 hrs |
| **3 — Architect Stretch** | You want the full engineering picture | `#[pyclass]`, fallback dispatch, CI wheels, benchmark suite | ~3 hrs |

**Setup for all tiers:**

```bash
cd starter/rust_accelerator
maturin develop --release
cd ../..
pytest project_solution/test_native_accelerator.py -v
```

> Windows + OneDrive users: run this **first**, or the linker will fail with `LNK1104`:
> ```powershell
> $env:CARGO_TARGET_DIR = "$env:LOCALAPPDATA\cargo-target"
> ```

Everything you implement goes in [`starter/rust_accelerator/src/lib.rs`](starter/rust_accelerator/src/lib.rs). Each `todo!()` is one exercise, with hints.

---

## Tier 1 — Novice Walkthrough: Your First Native Extension

**Goal:** get *anything* to compile and import. That first successful `import` is the hard part; everything after is detail.

### Step 1 — Prove the toolchain works

```bash
rustc --version      # need 1.70+
cargo --version
python -c "import maturin; print('maturin ok')"
```

Missing Rust? Install from [rustup.rs](https://rustup.rs) — one command, no configuration.

### Step 2 — Understand the two manifests before editing code

`Cargo.toml` tells **Rust** what to build:

```toml
[lib]
name = "rust_accelerator"     # ← CPython will look for PyInit_rust_accelerator
crate-type = ["cdylib"]       # ← a C-compatible dynamic library, not a Rust lib
```

`pyproject.toml` tells **Python** how to package it:

```toml
[build-system]
requires = ["maturin>=1.7,<2.0"]
build-backend = "maturin"
```

Read both files now. Nearly every beginner failure is a mismatch between them.

### Step 3 — Exercise 6 first (registration)

Counter-intuitive, but do the `#[pymodule]` function before the others. An empty module that *imports* proves your whole pipeline works; a perfect function you cannot import teaches you nothing.

Register nothing at first:

```rust
#[pymodule]
fn rust_accelerator(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__doc__", "my first extension")?;
    Ok(())
}
```

Comment out the other functions, then:

```bash
maturin develop --release
python -c "import rust_accelerator; print(rust_accelerator.__doc__)"
```

**Stop here until that prints.** If it does not, go to [TROUBLESHOOTING](09_TROUBLESHOOTING_AND_EDGE_CASES.md) — do not proceed.

### Step 4 — Exercise 1: `fnv1a_64`

Now implement the hash and register it. Verify against the published test vector:

```python
>>> import rust_accelerator
>>> hex(rust_accelerator.fnv1a_64(b""))
'0xcbf29ce484222325'          # the offset basis
>>> hex(rust_accelerator.fnv1a_64(b"a"))
'0xaf63dc4c8601ec8c'
```

Wrong numbers? You almost certainly used `*` instead of `wrapping_mul`, and a debug build panicked or a release build wrapped differently than you expected.

### Step 5 — Exercise 2: `dot_product`

The lesson here is error mapping, not arithmetic:

```python
>>> rust_accelerator.dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
32.0
>>> rust_accelerator.dot_product([1.0], [1.0, 2.0])
ValueError: vectors must be equal length (got 1 and 2)
```

That must be a genuine `ValueError`, not a `PanicException`.

### ✅ Tier 1 acceptance

```bash
pytest project_solution/test_native_accelerator.py -v -k "fnv1a or dot_product or backend_selection"
```

All green, and `python -c "import rust_accelerator"` works. **You have shipped a native extension.**

---

## Tier 2 — Core Project: Release the GIL

**Goal:** make Python do something it fundamentally cannot do on its own.

### Step 1 — See the limitation first

```bash
python 07_gil_release_parallelism_demo.py
```

With no Rust built, you get only the Python half:

```
  1 thread        119 ms
  4 threads       473 ms
  Ideal scaling would be 4.0x. Measured: 1.00x
  -> The GIL serialises the work. Threads bought you nothing.
```

Sit with that for a moment. Four threads, four cores, **zero** speedup — and the wall-clock got *worse* from context-switching overhead. No pure-Python change fixes this.

### Step 2 — Exercise 3: `count_primes` with `allow_threads`

Write the trial-division loop inside:

```rust
py.allow_threads(|| {
    // your loop here — cannot touch any Python object
})
```

The compiler enforces the safety rule. If it compiles, it is sound.

### Step 3 — Measure again

```bash
cd starter/rust_accelerator && maturin develop --release && cd ../..
python 07_gil_release_parallelism_demo.py
```

Target numbers:

| | 1 thread | 4 threads | Scaling |
| :--- | ---: | ---: | ---: |
| Pure Python | ~119 ms | ~473 ms | 1.00x |
| Your Rust | ~4 ms | ~5 ms | **>1.5x** |

### Step 4 — Deliberately break it (do this — it is the lesson)

Remove `py.allow_threads` and return the bare loop. Rebuild, re-run:

```bash
pytest project_solution/test_native_accelerator.py -v -k gil
```

It should **fail**, reporting that 4 threads took ~4x as long as 1. Now put it back and watch it pass. You have just proven to yourself what that one line does.

### Step 5 — Exercise 4: `sum_of_squares`

Same pattern, simpler body. Fold over the range without allocating.

### ✅ Tier 2 acceptance

```bash
pytest project_solution/test_native_accelerator.py -v -m "perf or not perf"
```

- `test_rust_count_primes_matches_python` — correctness
- `test_rust_is_substantially_faster_on_cpu_bound_work` — >5x
- `test_gil_is_actually_released` — real parallelism

---

## Tier 3 — Architect Stretch: Ship It Like a Professional

**Goal:** the parts that separate a demo from a library people depend on.

### Challenge 3.1 — Exercise 5: `RollingStats` as a `#[pyclass]`

Implement Welford's algorithm. Then measure why batching matters:

```python
import time, rust_accelerator
data = [float(i) for i in range(1_000_000)]

s = rust_accelerator.RollingStats()
t0 = time.perf_counter()
for x in data:            # 1,000,000 FFI crossings
    s.push(x)
per_call = time.perf_counter() - t0

s2 = rust_accelerator.RollingStats()
t0 = time.perf_counter()
s2.extend(data)           # ONE crossing
batched = time.perf_counter() - t0

print(f"per-call {per_call*1000:.0f}ms | batched {batched*1000:.0f}ms | {per_call/batched:.1f}x")
```

Write down your ratio. This is the most common real-world PyO3 mistake: a fast extension called in the slowest possible way.

### Challenge 3.2 — Graceful degradation

Extend [`native_accelerator.py`](project_solution/native_accelerator.py)'s `load_backend()` so that:

- `PYTHON_ACCELERATOR=python` in the environment forces the pure-Python path
- A `warnings.warn` fires once (not per call) when the native path is unavailable
- `benchmark()` reports which backend actually ran

Add tests for all three. **Rule:** a missing wheel must never be an `ImportError` for your users.

### Challenge 3.3 — A real benchmark suite

Write `bench.py` that sweeps workload sizes and prints a table:

```
   workload   python     rust   speedup
      1,000    0.8ms    0.9ms      0.9x   ← FFI overhead dominates
     10,000    8.1ms    0.4ms     20.3x
    100,000   81.4ms    2.6ms     31.3x
  1,000,000  814.2ms   25.1ms     32.4x
```

Find your **crossover point** — the size below which calling Rust is a net loss. Every native extension has one. Knowing yours is what makes you able to advise on when *not* to use it.

### Challenge 3.4 — Cross-platform wheels in CI

Write `.github/workflows/wheels.yml` using `PyO3/maturin-action` to build `abi3` wheels for Linux, macOS (x86_64 + arm64), and Windows, then upload them as artifacts. Confirm one `abi3-py311` wheel per platform — not one per Python version. Compare your file count to the 15 builds a non-`abi3` matrix would need.

### Challenge 3.5 — Type stubs

Native modules have no introspectable signatures, so `mypy` sees `Any`. Write `rust_accelerator.pyi`:

```python
def fnv1a_64(data: bytes) -> int: ...
def dot_product(a: list[float], b: list[float]) -> float: ...
def count_primes(limit: int) -> int: ...
def sum_of_squares(n: int) -> int: ...

class RollingStats:
    def __init__(self) -> None: ...
    def push(self, x: float) -> None: ...
    def extend(self, xs: list[float]) -> None: ...
    @property
    def count(self) -> int: ...
    @property
    def mean(self) -> float: ...
    @property
    def variance(self) -> float | None: ...
```

Add a `py.typed` marker and confirm `mypy --strict` is clean. Module 23 covers the packaging side of this.

### ✅ Tier 3 acceptance

- Every test passes, including `-m perf`
- You can state your crossover point and your batching ratio from memory
- `mypy --strict` is clean against the stubs
- CI produces `abi3` wheels for 3 platforms

---

## 🧪 Grading Yourself

```bash
# Correctness only — fast
pytest project_solution/test_native_accelerator.py -m "not perf" -q

# Everything, including performance and GIL assertions
pytest project_solution/test_native_accelerator.py -v

# Just the two that prove the module's thesis
pytest project_solution/test_native_accelerator.py -v -m perf
```

| Test | Proves |
| :--- | :--- |
| `test_fnv1a_known_vector` | Your hash matches the published spec |
| `test_rust_fnv1a_matches_python_property` | Hypothesis: agreement on *arbitrary* bytes |
| `test_rust_dot_product_raises_valueerror_like_python` | Errors cross the FFI boundary correctly |
| `test_rust_is_substantially_faster_on_cpu_bound_work` | The optimisation is real (>5x) |
| `test_gil_is_actually_released` | You achieved genuine multicore parallelism |

---

## 📤 Reference Solution

[`project_solution/rust_accelerator/src/lib.rs`](project_solution/rust_accelerator/src/lib.rs) is heavily commented and explains *why* each choice was made.

**Read it after your tests pass, not before.** Then compare: where did you differ, and is your version better or worse? That comparison is worth more than the reading.

---

## 🎓 You have mastered this module when you can…

- [ ] Explain why a Python `int` costs 28 bytes, without looking it up
- [ ] Explain why non-atomic refcounts require the GIL
- [ ] Name the four escape hatches and pick the right one for a described problem
- [ ] Explain why wrapping data in `ctypes` arrays does not accelerate a Python loop — and cite the measured number
- [ ] Write a `#[pyfunction]`, map an error to a Python exception, and register a module from memory
- [ ] Explain what `py.allow_threads` does and demonstrate it with a measurement
- [ ] State your crossover point and why FFI overhead creates one
- [ ] Explain what `abi3-py311` buys and what it costs
- [ ] Argue convincingly for **not** writing a native extension in a given scenario
