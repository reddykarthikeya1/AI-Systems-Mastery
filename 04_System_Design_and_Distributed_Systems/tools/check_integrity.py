#!/usr/bin/env python3
"""Guard the course's pedagogical invariants. Run in CI; fails the build on breach.

Four properties, each of which was actually broken at some point in this course's
history. Structural presence checks (does the file exist?) cannot catch any of
them, which is why this exists.

1. **A starter must FAIL the shipped tests.**
   This is the one that matters most. pytest loads conftest files along the
   *test file's* path — so a ``conftest.py`` sitting in ``starter/`` is never
   imported when you run ``pytest ../project_solution/test_x.py`` from there.
   Combined with a root conftest that puts every ``project_solution`` directory
   on ``sys.path``, the tests silently import the **solution**, every assertion
   passes, and the learner concludes an unimplemented stub is finished work.
   A course that certifies non-work is worse than one with no exercises at all.

2. **A debug lab must not name its own bug.**
   Every planted bug was once annotated ``# BUG: only 1 token per node!`` on the
   line above itself. That reduces a diagnostic exercise to reading a comment.

3. **A solution must disclose that it is an in-process model.**
   Simulation is the right pedagogy here — you cannot run a CDN in a lesson. But
   a docstring reading "Production-Grade Distributed Cache Client" above code
   that never opens a socket teaches a false mental model.

4. **A starter must actually contain stubs.**
   A ``starter/`` that holds a finished implementation is not a starter.

Usage::

    python tools/check_integrity.py
    python tools/check_integrity.py --verbose
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DISCLOSURE_RE = re.compile(
    r"simulat|in-process|in-memory|single.process|pure.Python|does not connect"
    r"|model of|from scratch|mimick|educational",
    re.I,
)
OVERCLAIM_RE = re.compile(r"production.grade", re.I)
SPOILER_RE = re.compile(r"#\s*(?:BUG|Bug|bug|FIXME|WRONG|PLANTED|INTENTIONAL|BROKEN)\b")


def modules() -> list[Path]:
    return sorted(p for p in ROOT.glob("Module_*") if p.is_dir())


def check_starters_fail(verbose: bool) -> list[str]:
    """Property 1: running the shipped tests from starter/ must NOT pass."""
    problems: list[str] = []
    for module_dir in modules():
        starter = module_dir / "starter"
        tests = sorted((module_dir / "project_solution").glob("test_*.py"))
        if not starter.is_dir():
            problems.append(f"{module_dir.name}: no starter/ directory")
            continue
        if not tests:
            problems.append(f"{module_dir.name}: no shipped tests to grade against")
            continue

        args = [str(Path("..") / "project_solution" / t.name) for t in tests]
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", *args, "-q", "-p", "no:cacheprovider"],
            cwd=starter,
            capture_output=True,
            text=True,
            timeout=300,
        )
        output = proc.stdout + proc.stderr
        failed = "NotImplementedError" in output or re.search(r"\d+ failed", output)
        if not failed:
            tail = output.strip().splitlines()[-1] if output.strip() else "(no output)"
            problems.append(
                f"{module_dir.name}: starter PASSES the shipped tests -> {tail[:70]}"
            )
        elif verbose:
            print(f"  ok   {module_dir.name} starter fails as intended")
    return problems


def check_debug_labs_unspoiled(verbose: bool) -> list[str]:
    """Property 2: no planted bug may be labelled in a comment."""
    problems: list[str] = []
    for module_dir in modules():
        lab = module_dir / "debug_lab"
        files = [f for f in lab.glob("*.py") if not f.name.startswith("test_")] if lab.is_dir() else []
        if not files:
            problems.append(f"{module_dir.name}: no debug_lab/*.py")
            continue
        for f in files:
            hits = SPOILER_RE.findall(f.read_text(encoding="utf-8"))
            if hits:
                problems.append(
                    f"{module_dir.name}/{f.name}: names its own bug ({len(hits)} marker(s))"
                )
        for required in ("SYMPTOMS.md", "ANSWERS.md"):
            if not (lab / required).exists():
                problems.append(f"{module_dir.name}: debug_lab missing {required}")
        if verbose and not problems:
            print(f"  ok   {module_dir.name} debug lab unspoiled")
    return problems


def check_disclosure(verbose: bool) -> list[str]:
    """Property 3: every solution says it is an in-process model, and none overclaims."""
    problems: list[str] = []
    for module_dir in modules():
        sols = [
            f
            for f in (module_dir / "project_solution").glob("*.py")
            if not f.name.startswith("test_") and f.name != "__init__.py"
        ]
        for f in sols:
            text = f.read_text(encoding="utf-8")
            try:
                doc = ast.get_docstring(ast.parse(text)) or ""
            except SyntaxError:
                problems.append(f"{module_dir.name}/{f.name}: does not parse")
                continue
            if not DISCLOSURE_RE.search(doc):
                problems.append(
                    f"{module_dir.name}/{f.name}: docstring does not disclose it is a model"
                )
            if OVERCLAIM_RE.search(doc):
                problems.append(
                    f"{module_dir.name}/{f.name}: claims 'production-grade' for an in-process model"
                )
            if verbose:
                print(f"  ok   {module_dir.name}/{f.name} discloses")
    return problems


def check_starters_are_stubs(verbose: bool) -> list[str]:
    """Property 4: a starter file must contain stubs, not a finished implementation."""
    problems: list[str] = []
    for module_dir in modules():
        files = [
            f
            for f in (module_dir / "starter").rglob("*.py")
            if f.name not in {"conftest.py", "__init__.py"}
        ]
        if not files:
            problems.append(f"{module_dir.name}: starter/ has no Python files")
            continue
        if not any(
            "NotImplementedError" in f.read_text(encoding="utf-8")
            or "TODO" in f.read_text(encoding="utf-8")
            for f in files
        ):
            problems.append(f"{module_dir.name}: starter/ contains no stubs or TODOs")
        elif verbose:
            print(f"  ok   {module_dir.name} starter is a real stub")
    return problems


CHECKS = (
    ("starters fail the shipped tests", check_starters_fail),
    ("debug labs do not spoil answers", check_debug_labs_unspoiled),
    ("solutions disclose they are models", check_disclosure),
    ("starters contain stubs", check_starters_are_stubs),
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    total = 0
    for label, fn in CHECKS:
        problems = fn(args.verbose)
        status = "PASS" if not problems else f"FAIL ({len(problems)})"
        print(f"[{status:>9}] {label}")
        for p in problems:
            print(f"             {p}")
        total += len(problems)

    print()
    if total:
        print(f"INTEGRITY CHECK FAILED: {total} breach(es)")
        return 1
    print(f"INTEGRITY CHECK PASSED: all 4 invariants hold across {len(modules())} modules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
