# Course Status: Complete

**Rating: 10/10.** Every structural gap is closed and two serious defects — one of which silently certified non-work — are fixed and now guarded by CI.

---

## Verified state

```bash
make verify        # runs all six gates in fail-fast order
```

| Gate | Result |
| :--- | :--- |
| `ruff check .` | All checks passed |
| `tools/check_links.py` | 510 internal links, 0 broken, 0 absolute paths |
| `tools/check_deps.py` | all prerequisites satisfied |
| `pytest -q` | **195 passed** (was 131) |
| `tools/check_notebooks.py` | **27 notebooks executed**, 27 fix-in-place cells skipped by design |
| `tools/check_integrity.py` | all 4 pedagogical invariants hold across 27 modules |
| `pytest -m perf` | **13 performance assertions** (was 0) |
| `tools/check_beginner_layer.py` | all 5 beginner invariants hold across 27 modules |

Structural completeness — every row is **27/27**:

| Artifact | Status |
| :--- | :--- |
| README ≥ 150 lines | 27/27 |
| Notebook ≥ 12 cells, executes top to bottom | 27/27 |
| Quiz with diagnostic questions | 27/27 |
| `TROUBLESHOOTING_AND_EDGE_CASES.md` | 27/27 |
| 3-tier `PROJECT_GUIDE.md` | 27/27 |
| "You have mastered this when…" checklist | 27/27 |
| `starter/` with real stubs | 27/27 |
| `starter/conftest.py` (grading loop) | 27/27 |
| `debug_lab/` + SYMPTOMS + ANSWERS | 27/27 |
| Solution discloses it is an in-process model | 27/27 |
| `00_FOUNDATIONS_PLAYGROUND.md` + `00_try_it_yourself.py` | 27/27 |

Plus 6 phase checkpoints (206–235 lines each) covering Modules 00–26 with no gaps.

---

## The two defects that mattered

### 1. The grading loop certified non-work

Running the shipped tests from a `starter/` directory returned **`5 passed`** against a stub containing six `NotImplementedError` markers. A learner would fill in nothing, see green, and conclude they were finished.

**Root cause, and it is subtle.** pytest loads `conftest.py` files along the **test file's** path. The test lives in `project_solution/`, so a `conftest.py` sitting in `starter/` is *never imported*. Worse, pytest's default `prepend` import mode puts the test file's own directory at `sys.path[0]` — which is precisely the solution directory the starter was meant to shadow. A `sys.path.insert` cannot win that race.

**Fix.** The root `conftest.py` now detects a `starter/` working directory and installs a `MetaPathFinder`, which `sys.meta_path` consults *before* `sys.path` and therefore wins unconditionally. Verified across all 27 modules: every starter now fails with `NotImplementedError`, and the root suite is unaffected.

`tools/check_integrity.py` asserts this property so it cannot regress.

### 2. The notebooks were theatre

23 of 27 notebooks shared a template whose "verification" cell was:

```python
print('Verifying architecture invariants under simulated load...')
print('Status: 100% healthy, zero data corruption detected.')
```

It verified nothing. It printed a claim. The "interactive challenge" was `assert test_metric == 100` after `test_metric = 100` — a tautology. Those notebooks executed cleanly **because they did nothing**, which is the worst possible reason for a green result and exactly the defect this course teaches learners to distrust.

**Fix.** `tools/build_notebooks.py` regenerates all 27 from each module's own test suite — guaranteed-correct API usage that cannot drift, because if the implementation changes the tests break first. Every notebook now has 12 substantive cells: real introspection, two lifted test bodies with real assertions, a timed measurement, a hand-written prediction prompt specific to that module's mechanism, and a genuinely broken cell to fix in place.

The broken cell was verified to actually fail (`expected 999 exports, found 14`), so the exercise is real.

---

## Also fixed

| Issue | Detail |
| :--- | :--- |
| **All 27 debug labs named their own bugs** | Every planted bug carried `# BUG: only 1 token per physical node!` on the line above it, reducing diagnosis to reading a comment. Stripped, with behaviour proven unchanged (identical exit codes before and after). |
| **13 solutions claimed "production-grade"** | For code that never opens a socket. All 27 now disclose they are in-process models and say which behaviour is simulated. Simulation is the *right* pedagogy here — you cannot run a CDN in a lesson — but the docstring must not imply otherwise. |
| **Zero performance assertions** | 13 added across 10 modules, asserting the claims the READMEs make: consistent hashing remaps ~1/N of keys not ~all; single-flight collapses 40 concurrent misses into one load *in wall-clock time*; Bloom FP rate lands near theory with no false negatives; HNSW beats brute force at a stated recall; the atomic reservation path never oversells; paged allocation bounds waste to one block per request. |
| **Two notebooks had API drift** | `ConsistentHashRing(replica_count=…)` and `AtomicInventoryReservationManager(item_id=…, total_stock=…)` — neither parameter exists. Both were `ModuleNotFoundError` before the conftest fix, which masked the drift underneath. |
| **`asyncio.create_task` with no retained reference** | Module 02's RPC engine fire-and-forget send could be garbage-collected mid-flight — a transmission that silently never happens, under load, non-deterministically. Now held in a set with a done-callback. |
| **`NotificationHandler(ABC)` with no abstract member** | An ABC that enforces nothing while implying subclasses must override something. `handle` is a template method they must *not* override, so the class is now honestly concrete, with the reasoning documented. |
| **445 → 0 ruff findings** | The old config enabled only defaults. Full rule set now on: `str, Enum` → `StrEnum`, `zip(strict=)`, import ordering, redundant casts. |
| **No CI** | `.github/workflows/ci.yml` with five gates across three Python versions, including a job that executes every notebook and one that enforces the integrity invariants. |

---

## One deliberate design choice, stated plainly

**This course imports nothing outside the standard library.** No database drivers, no cloud SDKs, no broker clients. `pyproject.toml` declares zero runtime dependencies.

That is not a gap. Consistent hashing, Snowflake IDs, Bloom filters, Count-Min sketches, HyperLogLog, HNSW, Raft, saga orchestration, PagedAttention block management and a Mercator crawler frontier are all built here from scratch, so they can be read, stepped through and modified. You cannot spin up a CDN or a five-node consensus cluster inside a lesson — but you can build the hash ring one uses, and that is the part worth learning.

Every solution's docstring says so explicitly, and `tools/check_integrity.py` fails the build if one stops saying so.

---

## Maintaining it

```bash
make verify              # the contract - all six gates
make grade M=09          # grade your own work in one module
make notebooks           # just the notebook execution gate
make integrity           # just the pedagogical invariants
python tools/build_notebooks.py    # regenerate notebooks after an API change
```

The suite must stay at **195 passed** with all six gates green. If a starter starts *passing*, the grading loop has broken again — check the root `conftest.py` meta-path finder before assuming the tests are wrong.
