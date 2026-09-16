# PyO3 Rust Native Extension Architecture

## 1. Rust Source Code (`src/lib.rs`)

```rust
use pyo3::prelude::*;

/// Sums an array of 64-bit floats in parallel, releasing the Python GIL!
#[pyfunction]
fn fast_parallel_sum(py: Python, numbers: Vec<f64>) -> PyResult<f64> {
    // Release the Python Global Interpreter Lock (GIL)
    py.allow_threads(|| {
        let total: f64 = numbers.iter().sum();
        Ok(total)
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_accelerator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fast_parallel_sum, m)?)?;
    Ok(())
}
```

## 2. Cargo Configuration (`Cargo.toml`)

```toml
[package]
name = "rust_accelerator"
version = "0.1.0"
edition = "2021"

[lib]
name = "rust_accelerator"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.20.0", features = ["extension-module"] }
```

## 3. Building Wheels with Maturin

```bash
pip install maturin
maturin develop --release
```
