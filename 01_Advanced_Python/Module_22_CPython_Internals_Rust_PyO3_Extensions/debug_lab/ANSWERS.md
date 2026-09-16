# Debug Lab Answers: Module 22

<details>
<summary>Bug 1: Native CPU loop retaining the Python GIL</summary>

### Root Cause
PyO3 functions execute while holding the GIL unless explicitly released using `py.allow_threads(|| { ... })`.

### Fix
Release the GIL around pure CPU-bound Rust logic:
```rust
#[pyfunction]
fn compute_heavy(py: Python<'_>, n: usize) -> u64 {
    py.allow_threads(|| {
        let mut total = 0u64;
        for i in 0..n {
            total = total.wrapping_add(i as u64 * 3);
        }
        total
    })
}
```
</details>
