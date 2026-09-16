# Module 22: Self-Assessment Quiz & Mastery Challenges

Test your understanding of CPython Internals, C-FFI, and Rust PyO3 Extensions before moving to **Module 21**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **The PyObject Struct:** What two header fields exist in every single object allocated on the CPython heap?
2. **Dynamic Linking:** How does `ctypes.cdll.LoadLibrary()` interact with OS shared libraries (`.dll` / `.so`)?
3. **Rust vs C for Extensions:** What major memory safety and concurrency advantages does Rust have over C when writing Python extensions?
4. **PyO3 & Maturin:** What are the respective roles of the `PyO3` crate and the `Maturin` build tool?
5. **Releasing the GIL:** How does `py.allow_threads(|| { ... })` in PyO3 allow true multi-core parallel CPU execution?
6. **Segmentation Faults:** Why does an out-of-bounds array access in C crash the entire Python interpreter without a Python traceback?
7. **Refcounting Leaks:** What happens if a C extension calls `Py_INCREF` on an object and forgets to balance it with `Py_DECREF`?
8. **Zero-Copy Memory:** How does Python's `memoryview` / Buffer Protocol allow native code to access large NumPy or byte arrays without duplicating memory in RAM?
9. **FFI vs Extension Module:** What is the architectural difference between calling an external C DLL via `ctypes` vs compiling a native CPython extension module?
10. **Thread Safety:** Why is it dangerous for a detached C worker thread to access a `PyObject*` without first acquiring the GIL?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- `ob_refcnt`: 64-bit integer tracking reference count.
- `ob_type`: Pointer to the object's `PyTypeObject` struct defining its methods and behavior.

#### Answer 2:
It uses OS system calls (`LoadLibraryW` on Windows, `dlopen` on POSIX) to load compiled machine code directly into the Python process virtual memory space.

#### Answer 3:
Rust eliminates NULL pointer dereferences, buffer overflows, use-after-free bugs, and data races at compile time via its borrow checker.

#### Answer 4:
- `PyO3`: Rust crate providing ergonomic macros (`#[pyfunction]`, `#[pymodule]`) to bind Rust types to Python.
- `Maturin`: Modern build tool and wheel packager for Rust-based Python extensions.

#### Answer 5:
It drops the Python Global Interpreter Lock, allowing the operating system to schedule the Rust thread across all available physical CPU cores simultaneously.

#### Answer 6:
C code accesses raw unmanaged hardware memory. Accessing protected memory violates OS kernel memory boundaries, causing the OS kernel to kill the process instantly (`SIGSEGV`).

#### Answer 7:
The object's reference count will never reach zero, preventing Python's garbage collector from ever freeing the memory (causing permanent RAM leaks).

#### Answer 8:
It passes a raw C memory pointer and stride dimensions directly to native code, avoiding expensive byte copying and allocation.

#### Answer 9:
- `ctypes`: Dynamic runtime bridging using `libffi`.
- Extension Module: Statically compiled C/Rust code adhering to Python's C-ABI, imported directly as a standard Python module (`import my_module`).

#### Answer 10:
CPython's internal memory allocator, dictionary lookup tables, and garbage collector are not thread-safe. Concurrent access without the GIL corrupts interpreter state.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: ctypes High-Speed Array Sum

**Goal:** Create a ctypes function that accepts an array of C integers and computes their sum.

<details>
<summary><b>Solution Code</b></summary>

```python
import ctypes

def ctypes_sum_integers(numbers: list[int]) -> int:
    ArrayType = ctypes.c_int * len(numbers)
    c_array = ArrayType(*numbers)
    # Sum using native ctypes pointer iteration
    return sum(c_array)

# Verification:
res = ctypes_sum_integers([10, 20, 30, 40, 50])
print("ctypes Sum Result:", res)
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Debug build presented as an optimisation

```
$ maturin develop
$ python -c "import rust_accelerator, time; \
  t=time.perf_counter(); rust_accelerator.count_primes(150_000); \
  print(time.perf_counter()-t)"
0.148
```

**Observed symptom:** The Rust version is barely faster than pure Python (0.15 s vs 0.12 s), and sometimes slower.

**(a)** What is missing from the build command?

**(b)** How large is the difference, typically?

**(c)** Which test in this module catches it?

<details>
<summary><b>Show the diagnosis</b></summary>

`--release` is missing. A debug build has no optimisation, keeps overflow checks, and includes debug assertions.

**Correct:** `maturin develop --release`, which applies `opt-level=3` plus the `lto = true` and `codegen-units = 1` settings in `Cargo.toml`. The difference is routinely **10–50×** — which is exactly the range that turns a 32× speedup into no speedup at all.

**The test:** `test_rust_is_substantially_faster_on_cpu_bound_work` asserts `speedup > 5.0` and its failure message says *'Did you build with --release?'*. This is the entire reason performance assertions exist in a test suite: without one, a forgotten flag produces a module that looks correct and delivers nothing.

</details>

---

### D2. Wrapping data in ctypes and calling it native

```python
import ctypes

def dot(a: list[float], b: list[float]) -> float:
    n = len(a)
    ca, cb = (ctypes.c_double * n)(*a), (ctypes.c_double * n)(*b)
    total = 0.0
    for i in range(n):
        total += ca[i] * cb[i]
    return total
```

**Observed symptom:** Measurably **5.26× slower** than `sum(x*y for x, y in zip(a, b))`.

**(a)** Why is the 'native' version slower?

**(b)** What is ctypes genuinely for?

**(c)** What would actually make this loop fast?

<details>
<summary><b>Show the diagnosis</b></summary>

The **loop still runs in the interpreter**. Worse, every `ca[i]` constructs a fresh Python `float` from the C double — you have added boxing overhead on top of the interpreter overhead you still pay.

**ctypes is for calling code that already exists** in a compiled library: `libm`, a vendor `.dll`, a system API. It is a bridge, never an engine. Storage type is not execution speed.

**To make the loop fast** the loop itself must leave Python: `numpy.dot` (vectorised, one BLAS call), or a compiled extension where the iteration happens in Rust/C. `Module_22/01_ctypes_honest_demo.py` measures both the anti-pattern and the real thing, so the 5.26× figure above is reproducible on your own machine rather than asserted.

</details>

---

### D3. Overflow behaviour differs between builds

```python
#[pyfunction]
fn fnv1a_64(data: &[u8]) -> u64 {
    let mut hash: u64 = 0xcbf2_9ce4_8422_2325;
    for &byte in data {
        hash ^= byte as u64;
        hash = hash * 0x0000_0100_0000_01b3;
    }
    hash
}
```

**Observed symptom:** Panics with `attempt to multiply with overflow` in debug; returns plausible but *different* values in release than the Python reference.

**(a)** Why do the two build profiles behave differently?

**(b)** What is the fix, and what are the alternatives?

**(c)** Why is the release behaviour more dangerous than the panic?

<details>
<summary><b>Show the diagnosis</b></summary>

Rust checks integer overflow in **debug** builds (panic) and **wraps** in release builds. The code relies on wrapping without saying so, so its behaviour is profile-dependent.

**Fix:** `hash.wrapping_mul(0x100000001b3)` — an explicit statement that wrapping is intended. Alternatives: `checked_mul` returns `Option<u64>`, `saturating_mul` clamps at the maximum, `overflowing_mul` returns the value plus a flag. Choosing deliberately is the point.

**Release is more dangerous** because a panic is loud and immediate, whereas silent wrapping produces a *wrong answer* that looks fine. If your tests only run one profile you will never see it. Module 22's `test_rust_fnv1a_matches_python_property` uses Hypothesis to compare against the Python oracle over arbitrary byte strings, which catches any divergence regardless of profile.

</details>

---

### D4. GIL held by the extension

```python
#[pyfunction]
fn count_primes(limit: u64) -> u64 {
    (2..limit).filter(|&n| is_prime(n)).count() as u64
}
```

**Observed symptom:** The Rust function is 32× faster single-threaded, but four threads take four times as long as one — no parallelism at all.

**(a)** What is missing, and why does it matter?

**(b)** What constraint does the fix impose on your code?

**(c)** Which test catches this?

<details>
<summary><b>Show the diagnosis</b></summary>

There is no `py.allow_threads`. The function holds the GIL for its whole duration, so Python threads calling it serialise exactly as pure-Python code would.

**Fix:**

```rust
fn count_primes(py: Python<'_>, limit: u64) -> u64 {
    py.allow_threads(|| { /* compute */ })
}
```

**Constraint:** the closure may not touch **any** Python object. The borrow checker enforces this at compile time, so if it compiles it is sound — you cannot accidentally violate it. Extract everything you need into Rust types *before* entering the closure.

**The test:** `test_gil_is_actually_released` runs the function on one thread and on four, and asserts the four-thread wall clock is under 3× the single-thread time. Measured result in this module: Python scales at 1.00×, Rust at 3.21×. That capability — using every core — is the main reason to write the extension at all, and it hangs on one line.

</details>

---

### D5. Per-call FFI overhead

```python
stats = rust_accelerator.RollingStats()
for x in million_values:
    stats.push(x)
```

**Observed symptom:** Slower than the pure-Python equivalent, despite Rust being 30× faster on the same arithmetic.

**(a)** Where does the time go?

**(b)** What is the fix?

**(c)** How would you find the size below which calling Rust is a net loss?

<details>
<summary><b>Show the diagnosis</b></summary>

Each `push` is a **boundary crossing**: argument conversion, GIL interaction, and the call itself, roughly 100–200 ns. A million crossings is 0.1–0.2 s of pure overhead, dwarfing the nanoseconds of actual work per element.

**Fix: batch.** `stats.extend(million_values)` crosses the boundary **once** and loops inside Rust. Same computation, one crossing instead of a million. This is the most common real-world PyO3 mistake — a fast extension called in the slowest possible way.

**Find the crossover** by sweeping workload sizes and plotting the speedup: at 1,000 elements Rust may be 0.9× (a loss), at 10,000 20×, at 1,000,000 32×. Every native extension has such a point, and knowing yours is what lets you advise when *not* to use it. Module 22's Tier 3 challenge 3.3 builds exactly this table.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
