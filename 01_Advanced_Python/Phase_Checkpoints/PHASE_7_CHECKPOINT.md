# Phase 7 Checkpoint Exam: Modern Data Engineering & AI Systems

> **Phase Scope:** Modules 24–26 (Polars/DuckDB Data Engineering, RAG & Vector Embeddings, Capstone Platform)  
> **Allocated Time:** 120 Minutes  
> **Format:** Large-scale analytics, semantic AI, and unified architecture exam.

---

## 🎯 The Exam Mission: Unified Market Intelligence & AI RAG Platform

Build an enterprise-scale market analytics and semantic retrieval engine. Ingest high-volume market datasets into Polars LazyFrames, run analytical window queries using DuckDB in-process SQL, build a semantic search index with vector embeddings, and package the complete system behind a resilient FastAPI gateway.

---

## 📋 Functional Requirements

### 1. Polars & DuckDB Columnar Pipeline (`analytics.py`)
- Lazy evaluation plan with filter and projection pushdown.
- DuckDB analytical SQL window query computing sector price rankings and moving averages.
- Zero copy Apache Arrow integration between Polars and DuckDB.

### 2. Semantic Search & Vector Retrieval (`rag.py`)
- Sliding window text chunking with sentence-boundary awareness and configurable overlap.
- Semantic vector embeddings (TF-IDF + TruncatedSVD or SentenceTransformers).
- Cosine similarity search retrieving top-k relevant financial disclosures.

### 3. Unified Gateway & Distributed Platform (`gateway.py`)
- FastAPI gateway with JWT authentication and correlation telemetry.
- Asynchronous task processing with Dead Letter Queue (DLQ) fallback.
- End-to-end integration test suite verifying end-to-end user workflows.

---

## 📊 Grading Rubric (100 Points Total)

| Requirement | Criteria | Points |
| :--- | :--- | :--- |
| **Columnar Data Engineering** | Lazy execution optimization, window functions, high-throughput aggregation | 30 pts |
| **Semantic AI & Retrieval** | Sentence-aware chunking, cosine distance accuracy, zero boundary loss | 30 pts |
| **Gateway & Task Architecture** | Clean auth, error isolation, Dead Letter Queue retry semantics | 25 pts |
| **Integration & Test Rigor** | Full integration test coverage under `@pytest.mark.capstone` | 15 pts |

**Passing Threshold:** 90/100 points required for Master of Python Systems Architecture Certification.

---

## 🚦 Pre-Flight Gate

**Do not start this exam until all of the following pass.** Attempting a
checkpoint on a foundation that does not build wastes the exam — you will spend
your time debugging setup instead of demonstrating skill.

```bash
# From the course root. All must be green.
pytest Module_24_Data_Engineering_Polars_Playwright \
      Module_25_AI_Engineering_LLM_Integration \
      Module_26_Final_Capstone_Project \
      -q

python tools/check_links.py --quiet
ruff check .
```

If any of that is red, fix it first. The exam assumes a working environment.

---

## 📏 Exam Rules

| Rule | Detail |
| :--- | :--- |
| **Time box** | Set a timer. When it ends, stop and submit what you have. |
| **No solution exists** | There is deliberately no reference implementation for this exam. The rubric is the specification. |
| **Modules are open-book** | Re-read any README, demo or troubleshooting guide. That is not cheating; it is what the job looks like. |
| **`project_solution/` is closed-book** | Do not read the module solutions during the exam. Copying them measures nothing. |
| **Write your own tests** | Untested code scores zero on the correctness criteria, however elegant it looks. |
| **Working beats complete** | A subset that runs and is tested outscores a full implementation that does not import. |

---

## 🔬 Self-Verification Harness

Produce this evidence before you score yourself. An unmeasured claim earns no
points.

```bash
# 1. It imports and runs at all
python -m your_solution            # must not traceback

# 2. Your tests pass
pytest your_tests.py -v            # paste the summary line

# 3. It is clean
ruff check .
mypy --strict your_solution.py     # advisory, but note the count

# 4. Coverage of your own code
pytest --cov=your_solution --cov-report=term-missing
```

Record the four outputs. The rubric below is scored against **evidence**, not
against intent.

---

## ⏱️ If You Run Out of Time

Score what exists and be honest about the gap. Partial credit is real:

1. **Submit the working subset.** Delete or clearly comment out anything that
   does not run — a broken import costs you every point in the file.
2. **Write down what is missing**, in one line per requirement. Naming your own
   gap accurately is itself a senior skill and earns the analysis criteria.
3. **Keep your tests.** Tests for the parts you finished are worth more than
   untested code for the parts you did not.

---

## 🔁 If You Score Below the Threshold

This is diagnostic information, not a verdict. Do exactly this:

1. Identify which **rubric row** you lost the most points on.
2. Go back to: **Module 25's retrieval-quality material and the capstone specification**.
3. Work that module's `debug_lab/` — it drills the failure modes this exam
   punishes.
4. Re-take the exam with a different data set or a changed requirement so you
   are re-solving rather than remembering.

Re-taking a checkpoint is normal. Advancing past one you failed is not — every
later phase assumes this one.

---

## 🎓 What This Checkpoint Actually Measures

Modules 24–26 taught you a set of tools. This exam tests **whether you can assemble subsystems into something that works and state honestly what it does not do**.

That is deliberately different from the module quizzes, which test whether you
understood each piece. Here nobody tells you which tool to reach for. Choosing
correctly, under a time limit, with no solution to check against, is the whole
point — and it is the closest this course gets to the actual job.
