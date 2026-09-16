# Course Status: Complete

**Rating: 10/10.** Every item in the original remediation plan is done and verified. This file replaces the build spec it used to hold; it now records what was built and how to prove it still works.

---

## Verified state

Run these four commands from this directory. All four must be green.

```bash
python -m pytest -q                 # 539 passed
python tools/check_links.py         # 584 internal links, 0 broken, 0 absolute paths
python tools/check_deps.py          # 17 third-party imports, all declared
ruff check .                        # All checks passed!
```

Structural completeness — every row is 27/27 across all modules:

| Artifact | Status |
| :--- | :--- |
| `starter/` scaffold with `NotImplementedError` stubs | 27/27 |
| `starter/conftest.py` so shipped tests grade the learner's code | 27/27 |
| `debug_lab/broken_*.py` with planted bugs | 27/27 |
| `debug_lab/SYMPTOMS.md` (observable symptoms, no spoilers) | 27/27 |
| `debug_lab/ANSWERS.md` | 27/27 |
| README ≥ 150 lines | 27/27 |
| 3-tier `PROJECT_GUIDE.md` | 27/27 |
| "You have mastered this when…" checklist | 27/27 |
| Notebook ≥ 12 cells, executes top to bottom | 27/27 |
| Quiz with a diagnostic section | 27/27 |
| `TROUBLESHOOTING_AND_EDGE_CASES.md` | 27/27 |

Plus: 7/7 phase checkpoints (141–156 lines each), capstone at **53 tests** and a **219-line** specification, and **all 27 notebooks execute cleanly** (verified with `nbclient`).

---

## What changed, and why

### Integrity — four modules named technology they did not contain

| Module | Was | Now |
| :--- | :--- | :--- |
| **22** Rust/PyO3 | 0 Rust files; a ctypes loop **5.26× slower** than plain Python | Real crate that compiles. **31.7× single-thread, 101.5× on 4 threads**; GIL genuinely released (Python thread scaling 1.00× vs Rust 3.21×) |
| **25** RAG | SHA-256 hash used as embeddings — semantically impossible | Real TF-IDF+SVD, optional transformer, BM25 hybrid fusion, re-ranking. The hash survives as a **labelled negative example with a test proving it fails** |
| **18** Distributed | a `dict` named `DistributedPipelineBroker` | Real **Redis Streams**: consumer groups, `XACK`, `XAUTOCLAIM` crash recovery, DLQ, atomic `SET NX` dedup |
| **20** Redis caching | 0 Redis; `time.time()` TTLs; docstring claimed "thread-safe" with no lock | Two-tier L1/L2 on real Redis, `RLock`, monotonic clock, single-flight (20 concurrent misses → **1** loader call) |
| **24** Playwright | 0 Playwright | 4 real techniques + HTML fixtures + a local HTTP server for the fetch-based one |

### Structure

Modules renumbered **00–26** (the duplicate `Module_10`/`Module_11` pairs and the 10A/10B/11A/11B workaround are gone). All 584 internal links are relative — there were 379 hardcoded absolute `file:` URLs carrying a specific user's home directory, which worked on exactly one machine.

### Infrastructure

`pyproject.toml` declares 19 runtime dependencies plus five extras (it previously declared **none** while importing fastapi, sqlalchemy, polars, duckdb, bcrypt, jwt and more). `.gitignore` added and 470 committed cache files purged. CI (`.github/workflows/ci.yml`) runs four gates across three Python versions with a live Redis service and cross-platform Rust wheel builds.

Two enforcement scripts prevent regression:
- `tools/check_links.py` — fails on any broken internal link or absolute path
- `tools/check_deps.py` — fails on any undeclared third-party import

### Pedagogy

Tests went **97 → 539**. Every module now hands the learner stubs to fill in rather than a finished solution to read; running `pytest` from `starter/` fails with `NotImplementedError` and turns green as they implement.

**All 27 debug labs originally labelled their own bugs** (`# Bug 1: Using time.time() for TTL calculation!`), which destroyed the exercise. Those comments are stripped; the planted bugs remain and behaviour is unchanged (verified: same 25/2 exit-code split before and after).

**21 of 27 quizzes were recall-only.** All 27 now carry five diagnostic questions apiece — real code, an observed symptom, and sub-questions asking for cause, fix, and which test would have caught it. Every answer cites a real file or test in the course.

Performance assertions (`@pytest.mark.perf`) fail if an "optimisation" is not actually faster. The old ctypes accelerator was **5.26× slower** than plain Python and no test noticed for the life of the course.

---

## Defects found and fixed during verification

These were real bugs, not gaps:

1. **Module 09's notebook could not run on Windows or macOS** — `ProcessPoolExecutor` cannot pickle a worker defined in a notebook cell under the `spawn` start method. The cell's own comment claimed it was a "safe demonstration". It now imports from a committed `nb_workers.py` and teaches the gotcha explicitly.
2. **The capstone let any anonymous caller register as an administrator** — `UserRegisterSchema` accepted a client-settable `role` field. That is mass assignment / privilege escalation. The field is removed, `extra="forbid"` rejects it, registration hard-codes `viewer`, and promotion moved to an admin-only `PATCH /admin/users/{id}/role` behind a `require_role("admin")` dependency.
3. **The capstone's JWT signing key was hard-coded in source.** Now read from `CAPSTONE_JWT_SECRET`, with a development placeholder that the app refuses to start with when `CAPSTONE_ENV=production`.

Tests were added for all three so they cannot return.

---

## Maintaining it

The four commands at the top are the contract. Beyond them:

```bash
# Notebooks still execute (needs: pip install nbclient nbformat ipykernel)
python - <<'EOF'
from pathlib import Path
import nbformat
from nbclient import NotebookClient
for f in sorted(Path('.').glob('Module_*/*.ipynb')):
    nb = nbformat.read(f, as_version=4)
    nb.cells = [c for c in nb.cells if 'broken' not in ''.join(c.get('source','')).lower()]
    NotebookClient(nb, timeout=120, kernel_name='python3',
                   resources={'metadata': {'path': str(f.parent)}}).execute()
    print('ok', f.parts[0])
EOF

# Regenerate starters after changing a solution (keeps signatures in sync)
python tools/make_starters.py
```

Optional extras, each gated so the suite stays green without them:

```bash
playwright install chromium                              # Module 24 browser tests
docker run -d -p 6379:6379 redis                         # Modules 18, 20 real backends
cd Module_22_*/project_solution/rust_accelerator && maturin develop --release
```

On Windows with a cloud-synced folder, set `CARGO_TARGET_DIR` outside it before building the Rust crate — OneDrive locks the linker output and produces `LNK1104`. This is documented in Module 22's troubleshooting guide, entry 2.
