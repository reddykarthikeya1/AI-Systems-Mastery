//! # Module 22 — A Real Native Rust Accelerator (PyO3)
//!
//! This crate compiles to a genuine CPython extension module. Every function
//! below exists to teach one specific PyO3 concept:
//!
//! | Function            | Teaches                                              |
//! |---------------------|------------------------------------------------------|
//! | `fnv1a_64`          | Zero-copy `&[u8]` borrowing — no data is duplicated  |
//! | `dot_product`       | Rust `Result` -> Python exception mapping            |
//! | `count_primes`      | `py.allow_threads()` — releasing the GIL for real    |
//! | `sum_of_squares`    | Iterator fusion; what `opt-level=3` + LTO buys you   |
//! | `RollingStats`      | `#[pyclass]` — a Rust struct as a Python class       |
//!
//! Build it with:  `maturin develop --release`   (from this directory)

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

// ---------------------------------------------------------------------------
// 1. ZERO-COPY BUFFER ACCESS
// ---------------------------------------------------------------------------
// `&[u8]` borrows the bytes object's buffer directly. Nothing is copied, and
// nothing is boxed into a Python int per element — which is precisely the
// mistake the pure-ctypes version in `native_accelerator.py` cannot avoid.
/// FNV-1a 64-bit hash over a raw byte buffer.
#[pyfunction]
fn fnv1a_64(data: &[u8]) -> u64 {
    let mut hash: u64 = 0xcbf2_9ce4_8422_2325; // FNV offset basis
    for &byte in data {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(0x0000_0100_0000_01b3); // FNV prime
    }
    hash
}

// ---------------------------------------------------------------------------
// 2. ERROR MAPPING: Rust Result -> Python exception
// ---------------------------------------------------------------------------
// Returning `PyResult<T>` lets a Rust `Err` surface in Python as a normal
// raised exception. `?` and `Err(...)` replace `raise`.
/// Dot product of two equal-length float vectors.
#[pyfunction]
fn dot_product(a: Vec<f64>, b: Vec<f64>) -> PyResult<f64> {
    if a.len() != b.len() {
        return Err(PyValueError::new_err(format!(
            "vectors must be equal length (got {} and {})",
            a.len(),
            b.len()
        )));
    }
    // zip + map + sum fuses into a single tight loop after optimisation.
    Ok(a.iter().zip(b.iter()).map(|(x, y)| x * y).sum())
}

// ---------------------------------------------------------------------------
// 3. RELEASING THE GIL — the single most important reason to write Rust
// ---------------------------------------------------------------------------
// While inside `allow_threads`, this thread holds NO GIL. Other Python threads
// run concurrently on other cores. Pure-Python CPU work can never do this;
// Module 09's threading lesson explains why.
//
// The closure may not touch any Python object — the compiler enforces that.
/// Count primes below `limit` by trial division (deliberately CPU-bound).
#[pyfunction]
fn count_primes(py: Python<'_>, limit: u64) -> u64 {
    py.allow_threads(|| {
        (2..limit)
            .filter(|&n| {
                if n < 4 {
                    return true;
                }
                if n % 2 == 0 {
                    return false;
                }
                let mut d = 3u64;
                while d * d <= n {
                    if n % d == 0 {
                        return false;
                    }
                    d += 2;
                }
                true
            })
            .count() as u64
    })
}

// ---------------------------------------------------------------------------
// 4. RAW ARITHMETIC THROUGHPUT
// ---------------------------------------------------------------------------
/// Sum of i*i for i in 0..n, computed without allocating.
#[pyfunction]
fn sum_of_squares(py: Python<'_>, n: u64) -> u64 {
    py.allow_threads(|| (0..n).map(|i| i.wrapping_mul(i)).fold(0u64, u64::wrapping_add))
}

// ---------------------------------------------------------------------------
// 5. A RUST STRUCT EXPOSED AS A PYTHON CLASS
// ---------------------------------------------------------------------------
// Welford's online algorithm — numerically stable streaming mean/variance.
// `#[pyclass]` gives it a Python type; `#[getter]` gives it properties.
/// Streaming mean/variance accumulator backed by a Rust struct.
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
        RollingStats { count: 0, mean: 0.0, m2: 0.0 }
    }

    /// Feed one sample into the accumulator.
    fn push(&mut self, x: f64) {
        self.count += 1;
        let delta = x - self.mean;
        self.mean += delta / self.count as f64;
        self.m2 += delta * (x - self.mean);
    }

    /// Feed a whole batch — one FFI crossing instead of N.
    fn extend(&mut self, xs: Vec<f64>) {
        for x in xs {
            self.push(x);
        }
    }

    #[getter]
    fn count(&self) -> u64 {
        self.count
    }

    #[getter]
    fn mean(&self) -> f64 {
        self.mean
    }

    /// Sample variance (Bessel-corrected). None until 2 samples exist.
    #[getter]
    fn variance(&self) -> Option<f64> {
        if self.count < 2 {
            None
        } else {
            Some(self.m2 / (self.count - 1) as f64)
        }
    }

    fn __repr__(&self) -> String {
        format!("RollingStats(count={}, mean={:.6})", self.count, self.mean)
    }
}

// ---------------------------------------------------------------------------
// MODULE REGISTRATION
// ---------------------------------------------------------------------------
// The `#[pymodule]` name MUST match `lib.name` in Cargo.toml, or CPython will
// not find the init symbol. This is the #1 PyO3 beginner error.
#[pymodule]
fn rust_accelerator(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__doc__", "Native Rust accelerator for Module 22.")?;
    m.add_function(wrap_pyfunction!(fnv1a_64, m)?)?;
    m.add_function(wrap_pyfunction!(dot_product, m)?)?;
    m.add_function(wrap_pyfunction!(count_primes, m)?)?;
    m.add_function(wrap_pyfunction!(sum_of_squares, m)?)?;
    m.add_class::<RollingStats>()?;
    Ok(())
}
