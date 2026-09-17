"""Verify the beginner layer across all courses in the repository.

Enforces:
  1. Every module has both beginner files (FOUNDATIONS_PLAYGROUND.md and try_it_yourself.py).
  2. Every try_it_yourself companion runs to completion and prints `All checks passed`.
  3. The markdown's python blocks, concatenated in order, ARE the script body.
  4. Every playground actually asserts something (>= 3 assertions).
  5. Standard library only - a beginner must not need pip install or external services.

Usage:
    python tools/check_beginner_layer.py
"""
from __future__ import annotations

import ast
import pathlib
import re
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
STDLIB = set(sys.stdlib_module_names)

BANNER = re.compile(r"^# -{4,} \d+\. ")
SIGN_OFF = ["print()", 'print("All checks passed.")', 'print("All checks passed!")']


def code_lines(text: str) -> list[str]:
    return [line.rstrip() for line in text.split("\n") if line.strip()]


def markdown_code(markdown: str) -> list[str]:
    blocks = re.findall(r"```python\n(.*?)```", markdown, re.DOTALL)
    return code_lines("\n".join(b.strip() for b in blocks))


def script_code(source: str) -> list[str]:
    lines = source.split("\n")
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("from __future__"):
            start = i + 1
            break
    body = code_lines("\n".join(line for line in lines[start:] if not BANNER.match(line)))
    while body and any(body[-1] == s for s in SIGN_OFF):
        body.pop()
    return body


def third_party_imports(tree: ast.AST) -> list[str]:
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            names = [(node.module or "").split(".")[0]]
        else:
            continue
        found += [n for n in names if n and n not in STDLIB and n != "__future__"]
    return found


def find_beginner_files(module: pathlib.Path) -> tuple[pathlib.Path | None, pathlib.Path | None]:
    for md_name, py_name in [
        ("00_FOUNDATIONS_PLAYGROUND.md", "00_try_it_yourself.py"),
        ("02_FOUNDATIONS_PLAYGROUND.md", "03_try_it_yourself.py"),
    ]:
        m = module / md_name
        p = module / py_name
        if m.exists() and p.exists():
            return m, p
    mds = list(module.glob("*PLAYGROUND*.md"))
    pys = list(module.glob("*try_it*.py"))
    return (mds[0] if mds else None, pys[0] if pys else None)


def main() -> int:
    courses = sorted(p for p in REPO_ROOT.glob("[0-1][0-9]_*") if p.is_dir())
    if not courses:
        print(f"no courses found under {REPO_ROOT}")
        return 1

    total_failures: list[str] = []
    total_checked = 0
    total_modules = 0

    for course in courses:
        modules = sorted(p for p in course.glob("Module_*") if p.is_dir())
        total_modules += len(modules)
        course_failures: list[str] = []

        for module in modules:
            md_path, py_path = find_beginner_files(module)
            name = f"{course.name}/{module.name}"

            if not md_path or not py_path or not md_path.exists() or not py_path.exists():
                course_failures.append(f"{name}: missing playground markdown or try_it_yourself companion")
                continue

            source = py_path.read_text(encoding="utf-8")
            markdown = md_path.read_text(encoding="utf-8")

            if script_code(source) != markdown_code(markdown):
                course_failures.append(f"{name}: playground markdown and companion script have drifted apart")

            try:
                tree = ast.parse(source)
            except SyntaxError as e:
                course_failures.append(f"{name}: companion script syntax error: {e}")
                continue

            asserts = sum(isinstance(n, ast.Assert) for n in ast.walk(tree))
            if asserts < 3:
                course_failures.append(f"{name}: only {asserts} assertions - claims go unchecked")

            for module_name in third_party_imports(tree):
                course_failures.append(f"{name}: imports third-party '{module_name}'")

            result = subprocess.run([sys.executable, py_path.name], cwd=module,
                                    capture_output=True, text=True, timeout=60)
            if result.returncode != 0 or "All checks passed" not in result.stdout:
                tail = (result.stderr or result.stdout).strip().split("\n")[-1:]
                course_failures.append(f"{name}: playground execution failed -> {' '.join(tail)}")

            total_checked += 1

        if course_failures:
            total_failures.extend(course_failures)
            print(f"FAILED: {course.name} ({len(course_failures)} issues)")
        else:
            print(f"PASSED: {course.name} ({len(modules)}/{len(modules)} modules)")

    print(f"\nBeginner layer check complete: {total_checked}/{total_modules} modules checked across {len(courses)} courses.")
    if total_failures:
        print(f"\n{len(total_failures)} TOTAL FAILURE(S):")
        for line in total_failures:
            print(f"  - {line}")
        return 1
    print("All beginner playground companions pass invariants 1-5!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
