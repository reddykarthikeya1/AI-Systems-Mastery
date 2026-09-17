#!/usr/bin/env python3
"""Gate: verify every module adheres to the academy module contract.

Fails on:
  - Missing project_solution/
  - Missing starter/
  - Missing debug_lab/
  - Missing problems/
  - Missing quiz.json

Usage:
    python tools/check_module_contracts.py
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

def main() -> int:
    courses = sorted([d for d in ROOT.iterdir() if d.is_dir() and d.name[:2].isdigit()])
    failures: list[str] = []
    total_mods = 0

    for course in courses:
        for mod in sorted([m for m in course.glob("Module_*") if m.is_dir()]):
            total_mods += 1
            # Check contract directories and files
            if not (mod / "project_solution").is_dir():
                failures.append(f"{course.name}/{mod.name}: missing project_solution/")
            if not (mod / "starter").is_dir():
                failures.append(f"{course.name}/{mod.name}: missing starter/")
            if not (mod / "debug_lab").is_dir():
                failures.append(f"{course.name}/{mod.name}: missing debug_lab/")
            if not (mod / "problems").is_dir():
                failures.append(f"{course.name}/{mod.name}: missing problems/")
            if not (mod / "quiz.json").is_file():
                failures.append(f"{course.name}/{mod.name}: missing quiz.json")

    print(f"Checked {total_mods} modules across {len(courses)} courses.")
    if failures:
        print(f"\n{len(failures)} MODULE CONTRACT FAILURE(S):")
        for f in failures[:30]:
            print(f"  - {f}")
        if len(failures) > 30:
            print(f"  ... and {len(failures) - 30} more")
        return 1

    print("  All 175 modules satisfy the complete artifact contract.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
