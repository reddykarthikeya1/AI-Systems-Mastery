//! # Module 22 STARTER — write the native accelerator yourself.
//!
//! Every `todo!()` below is one exercise. The test suite in
//! `../../project_solution/test_native_accelerator.py` already grades you:
//! it compares your Rust output against the pure-Python oracle and asserts
//! that your build is genuinely faster.
//!
//! ## How to work
//!
//! ```bash
//! cd starter/rust_accelerator
//! maturin develop --release          # compile + install into this env
//! cd ../..
//! pytest project_solution/test_native_accelerator.py -v
//! ```
//!
//! Windows + OneDrive: set `CARGO_TARGET_DIR` outside the synced folder first
//! (see TROUBLESHOOTING_AND_EDGE_CASES.md).
//!
//! Work the exercises in order — each one builds on the last.
//! Do NOT read `project_solution/rust_accelerator/src/lib.rs` until your tests
//! pass. Reading the answer costs you the entire lesson.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

// ===========================================================================
// EXERCISE 1 — Zero-copy buffer access                          [Tier 1]
// ===========================================================================
// Implement the FNV-1a 64-bit hash.
//
//   hash = 0xcbf29ce484222325                 (the offset basis)
//   for each byte:
//       hash = hash XOR byte
//       hash = hash * 0x100000001b3           (the FNV prime)
//
// HINTS
//  - The parameter is already `&[u8]`: it BORROWS the Python bytes buffer.
//    Nothing is copied. Iterate with `for &byte in data { ... }`.
//  - Rust panics on integer overflow in debug builds. Multiplication here is
//    *meant* to wrap, so you must say so explicitly: `wrapping_mul`.
//  - `byte` is a u8; you need it as u64. Use `byte as u64`.
//
// TEST: test_rust_fnv1a_matches_python  (and the Hypothesis property version)
#[pyfunction]
fn fnv1a_64(data: &[u8]) -> u64 {
    let _ = data;
    todo!("Exercise 1: implement FNV-1a. Remember wrapping_mul.")
}

// ===========================================================================
// EXERCISE 2 — Mapping a Rust error to a Python exception       [Tier 1]
// ===========================================================================
// Return the dot product of `a` and `b`.
// If the lengths differ, return a Python ValueError whose message contains the
// words "equal length" (the test matches on that phrase).
//
// HINTS
//  - `Err(PyValueError::new_err(format!("...")))` produces a real Python
//    ValueError that `pytest.raises(ValueError)` will catch.
//  - For the happy path: `a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()`.
//    That iterator chain fuses into one tight loop after optimisation.
//  - Wrap the success value in `Ok(...)`.
//
// TEST: test_rust_dot_product_matches_python,
//       test_rust_dot_product_raises_valueerror_like_python
#[pyfunction]
fn dot_product(a: Vec<f64>, b: Vec<f64>) -> PyResult<f64> {
    let _ = (&a, &b);
    todo!("Exercise 2: dot product + ValueError on length mismatch.")
}

// ===========================================================================
// EXERCISE 3 — Releasing the GIL  ★ the whole point of the module ★  [Tier 2]
// ===========================================================================
// Count the primes below `limit` using trial division.
//
// The counting logic is straightforward. The IMPORTANT part is that all of it
// must run inside `py.allow_threads(|| { ... })`, which drops the GIL so other
// Python threads can execute on other cores while this runs.
//
// HINTS
//  - Shape:  py.allow_threads(|| { /* your loop, returning u64 */ })
//  - The closure may not touch any Python object. The compiler enforces this;
//    if it compiles, you are safe.
//  - Trial division: n<4 is prime (2,3); even numbers >2 are not; otherwise
//    test odd divisors d while d*d <= n.
//  - `(2..limit).filter(|&n| ...).count() as u64` is a clean way to express it.
//
// If you skip allow_threads, `test_gil_is_actually_released` will FAIL — four
// threads will take ~4x as long as one instead of running concurrently.
//
// TEST: test_rust_count_primes_matches_python, test_gil_is_actually_released
#[pyfunction]
fn count_primes(py: Python<'_>, limit: u64) -> u64 {
    let _ = (py, limit);
    todo!("Exercise 3: trial division INSIDE py.allow_threads.")
}

// ===========================================================================
// EXERCISE 4 — Raw arithmetic throughput                        [Tier 2]
// ===========================================================================
// Return the sum of i*i for i in 0..n, wrapped to 64 bits.
// Release the GIL here too. Avoid allocating a Vec — fold over the range.
//
// HINT: (0..n).map(|i| i.wrapping_mul(i)).fold(0u64, u64::wrapping_add)
//
// TEST: (compare against PyAccelerator.sum_of_squares in your own check)
#[pyfunction]
fn sum_of_squares(py: Python<'_>, n: u64) -> u64 {
    let _ = (py, n);
    todo!("Exercise 4: wrapping sum of squares, GIL released.")
}

// ===========================================================================
// EXERCISE 5 — A Rust struct as a Python class                  [Tier 3]
// ===========================================================================
// Implement Welford's online algorithm for streaming mean and variance.
//
//   push(x):
//       count += 1
//       delta  = x - mean
//       mean  += delta / count
//       m2    += delta * (x - mean)      // note: the UPDATED mean
//
//   variance = m2 / (count - 1)          // None when count < 2
//
// HINTS
//  - `#[new]` marks the constructor.
//  - `#[getter]` turns a method into a Python property.
//  - `variance` returns `Option<f64>`; Rust `None` becomes Python `None`.
//  - `extend` should loop internally and call `push`. This is what makes ONE
//    FFI crossing do a million updates instead of a million crossings.
//  - Casting: `self.count as f64`.
//
// TEST: test_rust_rolling_stats_matches_python
#[pyclass]
struct RollingStats {
    count: u64,
    mean: f64,
    m2: f64,
}

#[pymethods]
impl RollingStats {
    #[new]
    fn new() -> Self {
        todo!("Exercise 5a: initialise count=0, mean=0.0, m2=0.0")
    }

    fn push(&mut self, x: f64) {
        let _ = x;
        todo!("Exercise 5b: Welford update")
    }

    fn extend(&mut self, xs: Vec<f64>) {
        let _ = xs;
        todo!("Exercise 5c: loop over xs calling push — one FFI crossing")
    }

    #[getter]
    fn count(&self) -> u64 {
        todo!("Exercise 5d")
    }

    #[getter]
    fn mean(&self) -> f64 {
        todo!("Exercise 5e")
    }

    #[getter]
    fn variance(&self) -> Option<f64> {
        todo!("Exercise 5f: None below 2 samples, else m2/(count-1)")
    }

    fn __repr__(&self) -> String {
        format!("RollingStats(count={}, mean={:.6})", self.count, self.mean)
    }
}

// ===========================================================================
// EXERCISE 6 — Module registration                              [Tier 1]
// ===========================================================================
// Register everything above so Python can see it.
//
// ⚠️ THE #1 FIRST-TIME ERROR: this function's name must be EXACTLY the same as
// `lib.name` in Cargo.toml (`rust_accelerator`). CPython imports the symbol
// `PyInit_rust_accelerator`. A mismatch gives you:
//     ImportError: dynamic module does not define module export function
//
// HINTS
//  - m.add_function(wrap_pyfunction!(some_fn, m)?)?;
//  - m.add_class::<RollingStats>()?;
//  - End with Ok(())
#[pymodule]
fn rust_accelerator(m: &Bound<'_, PyModule>) -> PyResult<()> {
    let _ = m;
    todo!("Exercise 6: register the 4 functions and 1 class.")
}
