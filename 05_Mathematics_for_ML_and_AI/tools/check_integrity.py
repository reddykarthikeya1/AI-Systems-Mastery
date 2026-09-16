#!/usr/bin/env python3
"""Assert the pedagogical invariants a file-presence check cannot see.

A structural checklist can confirm that `starter/` exists. It cannot confirm
that the starter *fails*, and that is the property that matters: a grading loop
which passes on an unimplemented stub tells the learner their work is correct
when it has not been done.

Five checks:

1. **Module starters must fail the shipped tests.**
2. **Debug labs must exit 0.** A lab that crashes teaches "read the traceback",
   not "diagnose a plausible wrong answer". Every planted defect must be silent.
3. **`SYMPTOMS.md` must not give away the fix.**
4. **Every module carries the required artifacts.**
5. **Scaffold content is counted, not hidden.** This course is partly written.
   The count is reported every run so that "how much is real" is never a
   surprise - and the exit status does not depend on it, because a scaffold is
   an honest state, not a defect.

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

SPOILER_PATTERNS = [
    r"\bthe (?:bug|defect|fix|cause) is\b",
    r"\bshould (?:be|have been) `?(?:max|min|sorted|all|any|while|<=|>=)\b",
    r"\breplace .{0,30} with\b",
    r"\bchange .{0,20} to `?(?:max|min|all|any)\b",
    r"\bforgot to\b",
    r"\bmissing (?:a )?(?:call to|delete|rebalance|sort)\b",
]

SCAFFOLD_MARKERS = ("Not written", "🔴 Scaffold", "TODO")


def modules(only: str | None) -> list[Path]:
    found = sorted(p for p in ROOT.glob("Module_*") if p.is_dir())
    if only:
        want = only.zfill(2)
        found = [p for p in found if p.name.split("_")[1] == want]
    return found


def run(args: list[str], cwd: Path, timeout: int = 600):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout, encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="only this module number, e.g. 07")
    args = parser.parse_args()

    mods = modules(args.module)
    if not mods:
        print("no modules matched")
        return 1

    failures: list[str] = []

    print("[1] module starters must fail the shipped tests")
    for m in mods:
        starter, solution = m / "starter", m / "project_solution"
        if not starter.is_dir() or not solution.is_dir():
            print(f"  skip  {m.name[:52]}  (no starter/ or project_solution/)")
            continue
        if not list(solution.glob("test_*.py")):
            print(f"  skip  {m.name[:52]}  (no shipped tests yet)")
            continue
        proc = run([sys.executable, "-m", "pytest", str(solution), "-q"], cwd=starter)
        if "failed" not in proc.stdout:
            failures.append(f"{m.name}: starter PASSES the shipped tests")
            print(f"  FAIL  {m.name[:52]}")
        else:
            print(f"  ok    {m.name[:52]}")

    print("\n[2] debug labs must exit 0 (defects silent, not crashing)")
    for m in mods:
        lab = m / "debug_lab"
        scripts = sorted(lab.glob("broken_*.py")) if lab.is_dir() else []
        if not scripts:
            failures.append(f"{m.name}: no debug_lab/broken_*.py")
            print(f"  FAIL  {m.name[:52]}  (no lab script)")
            continue
        proc = run([sys.executable, scripts[0].name], cwd=lab)
        if proc.returncode != 0:
            failures.append(f"{m.name}: debug lab exited {proc.returncode}")
            print(f"  FAIL  {m.name[:52]}  exit={proc.returncode}")
        else:
            print(f"  ok    {m.name[:52]}")

    print("\n[3] SYMPTOMS.md must not reveal the fix")
    for m in mods:
        symptoms = m / "debug_lab" / "SYMPTOMS.md"
        if not symptoms.is_file():
            failures.append(f"{m.name}: no debug_lab/SYMPTOMS.md")
            print(f"  FAIL  {m.name[:52]}  (missing)")
            continue
        text = symptoms.read_text(encoding="utf-8")
        hits = [p for p in SPOILER_PATTERNS if re.search(p, text, re.I)]
        if hits:
            failures.append(f"{m.name}: SYMPTOMS.md spoiler ({hits[0]})")
            print(f"  FAIL  {m.name[:52]}  {hits[0]}")
        else:
            print(f"  ok    {m.name[:52]}")

    print("\n[4] every module carries the required artifacts")
    required = [
        ("lessons", lambda m: (m / "lessons").is_dir()),
        ("beginner playground",
         lambda m: any("W3_BEGINNER" in p.name for p in m.glob("*.md"))),
        ("project guide", lambda m: any("PROJECT_GUIDE" in p.name for p in m.glob("*.md"))),
        ("self assessment",
         lambda m: any("SELF_ASSESSMENT" in p.name for p in m.glob("*.md"))),
        ("troubleshooting",
         lambda m: any("TROUBLESHOOTING" in p.name for p in m.glob("*.md"))),
        ("debug_lab", lambda m: (m / "debug_lab").is_dir()),
        ("SYMPTOMS", lambda m: (m / "debug_lab" / "SYMPTOMS.md").is_file()),
        ("ANSWERS", lambda m: (m / "debug_lab" / "ANSWERS.md").is_file()),
        ("lab script", lambda m: bool(list((m / "debug_lab").glob("broken_*.py")))),
    ]
    for m in mods:
        missing = [name for name, check in required if not check(m)]
        if missing:
            failures.append(f"{m.name}: missing {', '.join(missing)}")
            print(f"  FAIL  {m.name[:52]}  missing {missing[0]}")
        else:
            print(f"  ok    {m.name[:52]}")

    print("\n[5] how much of this course is still scaffold")
    lessons = list(ROOT.glob("Module_*/lessons/*.md"))
    unwritten = [p for p in lessons
                 if any(marker in p.read_text(encoding="utf-8")
                        for marker in SCAFFOLD_MARKERS)]
    written = len(lessons) - len(unwritten)
    print(f"  lessons written : {written} / {len(lessons)}")
    print(f"  lessons scaffold: {len(unwritten)}")
    if unwritten:
        print("  NOTE: the scaffold count is reported, not enforced. The lesson")
        print("        prose is the course's remaining work; the code, labs and")
        print("        grading loop below it are real and are checked above.")

    print()
    if failures:
        print(f"INTEGRITY CHECK FAILED - {len(failures)} problem(s):")
        for line in failures:
            print(f"  - {line}")
        return 1
    print(f"INTEGRITY CHECK PASSED: all 4 enforced invariants hold across "
          f"{len(mods)} modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
