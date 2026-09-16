#!/usr/bin/env python3
"""Add exam scaffolding to each phase checkpoint.

The existing checkpoints already carry a real mission statement, functional
requirements and a 100-point rubric - the substance is there. What they lack is
everything around the substance that makes a timed exam actually work:

  * a **pre-flight gate** - which module tests must already pass before you are
    allowed to start, so nobody attempts the exam on a broken foundation
  * **explicit rules** - the time box, and the fact that no solution exists
  * a **self-verification harness** - the exact commands that produce evidence
  * **partial-credit guidance** - what to do when time runs out
  * a **remediation path** - what failing tells you to go back and re-read

Content per phase is hand-written below; the script handles placement.

Usage::

    python tools/enrich_checkpoints.py            # apply
    python tools/enrich_checkpoints.py --check    # report only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "## 🚦 Pre-Flight Gate"

# phase -> (module dirs in scope, remediation focus, what the phase really tests)
PHASES: dict[str, tuple[list[str], str, str]] = {
    "1": (
        [
            "Module_00_Environment_Tooling_Workflow",
            "Module_01_Python_Fundamentals",
            "Module_02_Functions_Scopes_Closures",
            "Module_03_Data_Structures_Collections",
        ],
        "Modules 01–03 READMEs, then their `debug_lab/` directories",
        "whether you can build a small program from nothing and reason about "
        "what Python does with your data",
    ),
    "2": (
        [
            "Module_04_Deep_OOP",
            "Module_05_Decorators_Generators_Context_Managers",
            "Module_06_Error_Handling_Logging",
            "Module_07_Files_Data_Formats_Serialization",
            "Module_08_Testing_Quality_Assurance",
        ],
        "Module 04's MRO material and Module 08's testing patterns",
        "whether you can design types that hold their invariants and prove it "
        "with tests you wrote yourself",
    ),
    "3": (
        [
            "Module_09_Concurrency_Threading_Multiprocessing",
            "Module_10_Concurrency_Asyncio",
            "Module_11_Networking_Sockets_HTTP",
            "Module_12_Python_Internals_Bytecode_Memory",
        ],
        "Module 09's GIL material and Module 10's event-loop diagnostics",
        "whether you can pick the right concurrency primitive for a workload "
        "and keep the event loop clean",
    ),
    "4": (
        [
            "Module_13_FastAPI_ASGI_Architecture",
            "Module_14_Pydantic_V2_Validation_Routing",
            "Module_15_SQLAlchemy_Alembic_Database",
            "Module_16_Authentication_Authorization_Security",
            "Module_17_Advanced_FastAPI_WebSockets_DI",
            "Module_18_Distributed_Systems_Task_Queues_Streaming",
        ],
        "Module 16's authorisation material and Module 15's session lifecycle",
        "whether you can build an API that is correct, validated and safe to "
        "expose to the internet",
    ),
    "5": (
        [
            "Module_19_Containerization_CICD_Deployment",
            "Module_20_Performance_Optimization_Profiling_Caching",
        ],
        "Module 20's profiling workflow — measure before optimising",
        "whether you can find a real bottleneck and prove you fixed it",
    ),
    "6": (
        [
            "Module_21_Metaprogramming_Descriptors_Memory",
            "Module_22_CPython_Internals_Rust_PyO3_Extensions",
            "Module_23_Strict_Typing_Packaging_Publishing",
        ],
        "Module 22's escape-hatch decision table — and when NOT to go native",
        "whether you can reach into the language's machinery without making "
        "the result unmaintainable",
    ),
    "7": (
        [
            "Module_24_Data_Engineering_Polars_Playwright",
            "Module_25_AI_Engineering_LLM_Integration",
            "Module_26_Final_Capstone_Project",
        ],
        "Module 25's retrieval-quality material and the capstone specification",
        "whether you can assemble subsystems into something that works and "
        "state honestly what it does not do",
    ),
}


def build(phase: str) -> str:
    modules, remediation, tests_what = PHASES[phase]
    pytest_targets = " \\\n      ".join(modules)
    first = modules[0].split("_")[1]
    last = modules[-1].split("_")[1]

    return f"""
---

{MARKER}

**Do not start this exam until all of the following pass.** Attempting a
checkpoint on a foundation that does not build wastes the exam — you will spend
your time debugging setup instead of demonstrating skill.

```bash
# From the course root. All must be green.
pytest {pytest_targets} \\
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
2. Go back to: **{remediation}**.
3. Work that module's `debug_lab/` — it drills the failure modes this exam
   punishes.
4. Re-take the exam with a different data set or a changed requirement so you
   are re-solving rather than remembering.

Re-taking a checkpoint is normal. Advancing past one you failed is not — every
later phase assumes this one.

---

## 🎓 What This Checkpoint Actually Measures

Modules {first}–{last} taught you a set of tools. This exam tests **{tests_what}**.

That is deliberately different from the module quizzes, which test whether you
understood each piece. Here nobody tells you which tool to reach for. Choosing
correctly, under a time limit, with no solution to check against, is the whole
point — and it is the closest this course gets to the actual job.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    directory = ROOT / "Phase_Checkpoints"
    have = added = 0

    for phase in sorted(PHASES):
        path = directory / f"PHASE_{phase}_CHECKPOINT.md"
        if not path.exists():
            print(f"  missing: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        if MARKER in text:
            have += 1
            continue
        if not args.check:
            path.write_text(text.rstrip() + "\n" + build(phase), encoding="utf-8")
        added += 1

    verb = "would enrich" if args.check else "enriched"
    print(f"already enriched: {have} | {verb}: {added}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
