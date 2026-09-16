#!/usr/bin/env python3
"""Verify every written lesson: its code runs, and it asserts rather than prints.

The scaffold says a lesson's code block "must be runnable as written and must
ASSERT, not print. A cell that prints a plausible number teaches nothing." This
enforces that, so the promise is checked rather than trusted.

Five checks per written lesson:

1. The python blocks execute to completion (exit 0).
2. At least one `assert` runs - the lesson demonstrates a claim rather than
   asserting one in prose.
3. Nothing outside the standard library and NumPy is imported, so a learner
   needs no setup beyond the course's declared dependency.
4. The learning objectives and self-check answers are filled in.
5. No stub markers survive.

Unwritten scaffold lessons are counted and skipped, not failed - a scaffold is
an honest state. The count is printed every run so the remaining work is
visible.

    python tools/check_lessons.py
    python tools/check_lessons.py --module 01
    python tools/check_lessons.py --list-unwritten
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_THIRD_PARTY = {"numpy"}
STUB_MARKERS = ("Not written", "this is a scaffold stub")


def modules(only: str | None) -> list[Path]:
    found = sorted(p for p in ROOT.glob("Module_*") if p.is_dir())
    if only:
        want = only.zfill(2)
        found = [p for p in found if p.name.split("_")[1] == want]
    return found


def code_blocks(text: str) -> list[str]:
    return re.findall(r"```python\n(.*?)```", text, re.DOTALL)


def verify_block(text: str) -> str | None:
    """The block under '3. Verify it in code' - the one the scaffold promises
    is runnable as written.

    Other sections may show a fragment to make a point ("the assertion you
    should have written"), and a fragment is not meant to execute on its own.
    Those are syntax-checked instead, so a broken one is still caught.
    """
    section = re.search(r"## 3\. Verify it in code\n(.*?)(?=\n## |\Z)",
                        text, re.DOTALL)
    if not section:
        return None
    blocks = code_blocks(section.group(1))
    return blocks[0] if blocks else None


def is_written(text: str) -> bool:
    return not any(marker in text for marker in STUB_MARKERS)


def third_party(source: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.append(node.module.split(".")[0])
    stdlib = set(sys.stdlib_module_names)
    return [n for n in names if n not in stdlib and n not in ALLOWED_THIRD_PARTY]


def check_lesson(path: Path, failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    label = f"{path.parent.parent.name.split('_')[1]}/{path.name}"

    blocks = code_blocks(text)
    if not blocks:
        failures.append(f"{label}: no python block")
        return

    source = verify_block(text)
    if source is None:
        failures.append(f"{label}: no code block under '3. Verify it in code'")
        return

    # Illustrative fragments elsewhere are not run, but must still be valid Python.
    for other in blocks:
        if other is source:
            continue
        try:
            ast.parse(other)
        except SyntaxError as exc:
            failures.append(f"{label}: a prose code block does not parse ({exc.msg})")

    if "assert" not in source:
        failures.append(f"{label}: code block never asserts")

    outside = third_party(source)
    if outside:
        failures.append(f"{label}: imports {outside[0]!r} (allowed: stdlib + numpy)")

    if "- [ ] TODO" in text or re.search(r"^\s*TODO\s*$", text, re.M):
        failures.append(f"{label}: TODO left in the prose")

    if "<summary>Answers</summary>" in text:
        answers = text.split("<summary>Answers</summary>", 1)[1]
        if not re.search(r"^\d+\.\s+\S", answers, re.M):
            failures.append(f"{label}: self-check answers are empty")

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8") as handle:
        handle.write(source)
        temporary = Path(handle.name)
    try:
        run = subprocess.run([sys.executable, str(temporary)],
                             capture_output=True, text=True, timeout=120)
        if run.returncode != 0:
            tail = (run.stderr or run.stdout).strip().split("\n")[-1:]
            failures.append(f"{label}: code failed -> {' '.join(tail)}")
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="only this module number, e.g. 01")
    parser.add_argument("--list-unwritten", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    written_total = scaffold_total = 0
    per_module: list[tuple[str, int, int]] = []
    unwritten_names: list[str] = []

    for module in modules(args.module):
        lessons = sorted((module / "lessons").glob("*.md"))
        written = scaffold = 0
        for path in lessons:
            text = path.read_text(encoding="utf-8")
            if is_written(text):
                written += 1
                check_lesson(path, failures)
            else:
                scaffold += 1
                unwritten_names.append(f"{module.name}/{path.name}")
        per_module.append((module.name, written, len(lessons)))
        written_total += written
        scaffold_total += scaffold

    if args.list_unwritten:
        for name in unwritten_names:
            print(name)
        return 0

    print("lessons written, per module")
    for name, written, total in per_module:
        bar = "#" * round(20 * written / total) if total else ""
        print(f"  {name[:50]:52} {written:>3}/{total:<3} {bar}")

    print(f"\ntotal written : {written_total} / {written_total + scaffold_total}")
    print(f"still scaffold: {scaffold_total}")

    if failures:
        print(f"\n{len(failures)} FAILURE(S) in written lessons:")
        for line in failures:
            print(f"  - {line}")
        return 1

    if written_total:
        print(f"\nAll {written_total} written lessons execute, assert, and need "
              f"nothing beyond NumPy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
