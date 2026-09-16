# 🔰 Beginner-to-Rust Extensions Guide: PyO3 Without Fear

Welcome to **Module 22**! In this module, you step into the cutting edge of modern software engineering: **Native Rust Extensions for Python** using **PyO3**.

Many modern high-performance Python tools (such as `polars`, `pydantic-core`, and `ruff`) are written in Rust under the hood.

If you don't have Rust installed or have never written a line of Rust before, **do not panic**. This guide shows you why this technology exists, how to install the tools, and how the course's pure-Python fallback mode protects you.

---

## 1. Why Do Python Engineers Use Rust?

Python is one of the most expressive and productive languages on Earth. However, for CPU-intensive mathematical calculations, string parsing, or cryptography, Python code is bound by:
1. **Dynamic Type Overhead:** Python must check the type of every number during arithmetic.
2. **The Global Interpreter Lock (GIL):** Python threads cannot execute pure Python bytecode across multiple CPU cores simultaneously.

Rust solves both:
- **Bare-Metal Speed:** Compiles directly to machine code ($20\times$ to $100\times$ faster than pure Python).
- **Fearless Concurrency:** Rust functions can release the GIL (`py.allow_threads(...)`), allowing true multi-core parallel execution.
- **Zero Memory Leaks:** Rust does not use a garbage collector; memory is managed via compile-time ownership rules.

---

## 2. You Don't Need Rust Installed Right Now: The Dual-Track Fallback

> [!NOTE]
> **Pure Python Fallback Mode:**
> Every single exercise, unit test, and benchmark in Module 22 contains an automatic Python fallback! If a compiled Rust `.pyd` or `.so` module is not found on your system, the code seamlessly executes an optimized pure Python equivalent.
> 
> You can complete 100% of this course without installing Rust!

---

## 3. How to Set Up Rust & PyO3 (When You Are Ready)

If you want to compile real native Rust binaries on your computer, follow these simple steps:

### Step 1: Install Rustup (The Rust Toolchain Installer)
- **Windows:** Download and run `rustup-init.exe` from [https://rustup.rs](https://rustup.rs). Select default installation (Option 1).
- **macOS / Linux:** Run in your terminal:
  ```bash
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  ```

### Step 2: Install Maturin (The Python-Rust Bridge Builder)
Maturin is the modern build tool that turns a Rust crate into a Python wheel:
```bash
pip install maturin
```

### Step 3: Build the Extension
Inside `Module_22_CPython_Internals_Rust_PyO3_Extensions/rust_extension`:
```bash
maturin develop
```
Maturin will compile the Rust code and place the native `.pyd` module directly into your active Python environment!

---

## 4. Anatomy of a 10-Line PyO3 Function

Look how simple Rust code looks when interfacing with Python using PyO3:

```rust
use pyo3::prelude::*;

// #[pyfunction] tells PyO3: "Expose this Rust function to Python!"
#[pyfunction]
fn sum_of_squares(n: u64) -> PyResult<u64> {
    let mut total = 0;
    for i in 1..=n {
        total += i * i;
    }
    Ok(total)
}

// Defines the Python module name:
#[pymodule]
fn native_engine(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_of_squares, m)?)?;
    Ok(())
}
```

In Python, you can now import and call it like any native function:
```python
import native_engine

result = native_engine.sum_of_squares(10_000_000)
print("Computed in 2 milliseconds:", result)
```

You are now ready to explore the complete native bindings, benchmark comparisons, and FFI architectures in the main [Module 22 README](01_README.md)!
