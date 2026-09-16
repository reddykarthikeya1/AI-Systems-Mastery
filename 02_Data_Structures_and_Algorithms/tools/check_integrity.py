#!/usr/bin/env python3
"""Assert the pedagogical invariants that file-presence checks cannot see.

A structural checklist can confirm that `starter/` exists. It cannot confirm
that the starter *fails*, and that is the property that matters: a grading loop
which passes on an unimplemented stub tells the learner their work is correct
when it has not been done. That is the single worst failure a course can have,
and this course shipped with it until it was found and fixed.

Six invariants, each one a defect this course actually had or could regress to:

1. **Module starters must fail the shipped tests.** At least one test per module
   must fail on an untouched `starter/`.
2. **Problem-bank stubs must fail their tests.** Same property, for all 15
   problem banks.
3. **Reference solutions must pass.** The bank is worthless if its own answers
   are wrong.
4. **Debug labs must exit 0.** A lab that crashes teaches "read the traceback",
   not "diagnose a plausible wrong answer". Every planted defect must be silent.
5. **SYMPTOMS.md must not give away the fix.** A lab that spoils its own answer
   skips the reasoning it exists to build.
6. **Every module carries the full artifact set.**

Usage::

    python tools/check_integrity.py
    python tools/check_integrity.py --module 07
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Phrases that would hand the learner the answer before they have reasoned.
SPOILER_PATTERNS = [
    r"\bthe (?:bug|defect|fix|cause) is\b",
    r"\bshould (?:be|have been) `?(?:max|min|sorted|all|any|while|<=|>=)\b",
    r"\breplace .{0,30} with\b",
    r"\bchange .{0,20} to `?(?:max|min|all|any)\b",
    r"\bforgot to\b",
    r"\bmissing (?:a )?(?:call to|delete|rebalance|sort)\b",
]


def modules(only: str | None) -> list[Path]:
    found = sorted(p for p in ROOT.glob("Module_*") if p.is_dir())
    if only:
        want = only.zfill(2)
        found = [p for p in found if p.name.split("_")[1] == want]
    return found


def run(args: list[str], cwd: Path, timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(
        args, cwd=cwd, capture_output=True, text=True,
        timeout=timeout, encoding="utf-8", errors="replace",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="only this module number, e.g. 07")
    args = parser.parse_args()

    mods = modules(args.module)
    if not mods:
        print("no modules matched")
        return 1

    failures: list[str] = []

    # -- 1. module starters must FAIL ---------------------------------------
    print("[1] module starters must fail the shipped tests")
    for m in mods:
        starter = m / "starter"
        solution = m / "project_solution"
        if not starter.is_dir() or not solution.is_dir():
            failures.append(f"{m.name}: missing starter/ or project_solution/")
            continue
        proc = run([sys.executable, "-m", "pytest", str(solution), "-q"], cwd=starter)
        if "failed" not in proc.stdout:
            failures.append(
                f"{m.name}: starter PASSES the shipped tests - the grading loop "
                f"is certifying non-work"
            )
            print(f"  FAIL  {m.name[:56]}")
        else:
            print(f"  ok    {m.name[:56]}")

    # -- 2. problem-bank stubs must FAIL ------------------------------------
    print("\n[2] problem-bank stubs must fail their tests")
    for m in mods:
        problems = m / "problems"
        if not problems.is_dir():
            failures.append(f"{m.name}: missing problems/")
            continue
        proc = run([sys.executable, "-m", "pytest", "tests", "-q"], cwd=problems)
        if "failed" not in proc.stdout:
            failures.append(f"{m.name}: problem-bank stubs PASS - grading loop broken")
            print(f"  FAIL  {m.name[:56]}")
        else:
            print(f"  ok    {m.name[:56]}")

    # -- 3. reference solutions must PASS -----------------------------------
    print("\n[3] reference solutions must pass")
    for m in mods:
        problems = m / "problems"
        if not problems.is_dir():
            continue
        proc = run([sys.executable, "-m", "pytest", str(problems), "-q"], cwd=ROOT)
        if proc.returncode != 0:
            failures.append(f"{m.name}: reference solutions FAIL their own tests")
            print(f"  FAIL  {m.name[:56]}")
        else:
            print(f"  ok    {m.name[:56]}")

    # -- 4. debug labs must exit 0 ------------------------------------------
    print("\n[4] debug labs must exit 0 (defects silent, not crashing)")
    for m in mods:
        lab_dir = m / "debug_lab"
        scripts = sorted(lab_dir.glob("broken_*.py")) if lab_dir.is_dir() else []
        if not scripts:
            failures.append(f"{m.name}: no debug_lab/broken_*.py")
            print(f"  FAIL  {m.name[:56]}  (no lab)")
            continue
        bad = []
        for script in scripts:
            proc = run([sys.executable, script.name], cwd=lab_dir)
            if proc.returncode != 0:
                bad.append(f"{script.name} exited {proc.returncode}")
        if bad:
            failures.append(f"{m.name}: debug lab crashes - {'; '.join(bad)}")
            print(f"  FAIL  {m.name[:56]}  {bad[0]}")
        else:
            print(f"  ok    {m.name[:56]}")

    # -- 5. SYMPTOMS must not spoil -----------------------------------------
    print("\n[5] SYMPTOMS.md must not reveal the fix")
    for m in mods:
        symptoms = m / "debug_lab" / "SYMPTOMS.md"
        if not symptoms.is_file():
            failures.append(f"{m.name}: no debug_lab/SYMPTOMS.md")
            print(f"  FAIL  {m.name[:56]}  (missing)")
            continue
        text = symptoms.read_text(encoding="utf-8").lower()
        hits = [p for p in SPOILER_PATTERNS if re.search(p, text)]
        if hits:
            failures.append(f"{m.name}: SYMPTOMS.md contains a spoiler ({hits[0]})")
            print(f"  FAIL  {m.name[:56]}  {hits[0]}")
        else:
            print(f"  ok    {m.name[:56]}")

    # -- 6. artifact completeness -------------------------------------------
    print("\n[6] every module carries the full artifact set")
    required = [
        ("README", lambda m: any(p.name.endswith("README.md") for p in m.glob("*.md"))),
        ("project guide", lambda m: any("PROJECT_GUIDE" in p.name for p in m.glob("*.md"))),
        ("self assessment", lambda m: any("SELF_ASSESSMENT" in p.name for p in m.glob("*.md"))),
        ("troubleshooting", lambda m: any("TROUBLESHOOTING" in p.name for p in m.glob("*.md"))),
        ("starter", lambda m: (m / "starter").is_dir()),
        ("starter conftest", lambda m: (m / "starter" / "conftest.py").is_file()),
        ("project_solution", lambda m: (m / "project_solution").is_dir()),
        ("problems", lambda m: (m / "problems").is_dir()),
        ("problems README", lambda m: (m / "problems" / "README.md").is_file()),
        ("solutions", lambda m: (m / "problems" / "solutions").is_dir()),
        ("debug_lab", lambda m: (m / "debug_lab").is_dir()),
        ("SYMPTOMS", lambda m: (m / "debug_lab" / "SYMPTOMS.md").is_file()),
        ("ANSWERS", lambda m: (m / "debug_lab" / "ANSWERS.md").is_file()),
    ]
    for m in mods:
        missing = [name for name, check in required if not check(m)]
        if missing:
            failures.append(f"{m.name}: missing {', '.join(missing)}")
            print(f"  FAIL  {m.name[:56]}  missing {missing[0]}")
        else:
            print(f"  ok    {m.name[:56]}")

    print()
    if failures:
        print(f"INTEGRITY CHECK FAILED: {len(failures)} problem(s)")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"INTEGRITY CHECK PASSED: all 6 invariants hold across {len(mods)} modules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
