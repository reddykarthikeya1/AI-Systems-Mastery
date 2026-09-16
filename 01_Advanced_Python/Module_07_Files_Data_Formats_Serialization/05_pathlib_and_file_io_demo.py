#!/usr/bin/env python3
"""Module 07: pathlib & Modern File I/O Demonstration.

This script demonstrates cross-platform path manipulation, directory creation,
metadata inspection, and atomic file replacements using pathlib.Path.
"""

from __future__ import annotations

from pathlib import Path


def demo_pathlib_operations() -> None:
    print("=" * 60)
    print("  1. Modern Path Operations with pathlib.Path")
    print("=" * 60)

    work_dir = Path("sandbox_data") / "nested_dir"
    work_dir.mkdir(parents=True, exist_ok=True)

    file_path = work_dir / "report.txt"
    file_path.write_text("Line 1: Production Report\nLine 2: Status Normal", encoding="utf-8")

    print(f"Path Object      : {file_path}")
    print(f"File Name        : {file_path.name}")
    print(f"Stem (No suffix) : {file_path.stem}")
    print(f"Suffix           : {file_path.suffix}")
    print(f"Parent Directory : {file_path.parent}")
    print(f"File Size        : {file_path.stat().st_size} bytes")


def demo_atomic_file_write() -> None:
    print("\n" + "=" * 60)
    print("  2. Atomic File Replacement (Prevents Half-Written Corruptions)")
    print("=" * 60)

    target_file = Path("production_data.json")
    target_file.write_text('{"version": 1, "state": "old"}', encoding="utf-8")

    # Step 1: Write new content to a temporary sibling file
    temp_file = target_file.with_suffix(".tmp")
    temp_file.write_text('{"version": 2, "state": "updated"}', encoding="utf-8")

    # Step 2: Atomic rename replaces old file instantaneously at OS filesystem level
    temp_file.replace(target_file)

    print(f"Target File Content after Atomic Replace:\n  {target_file.read_text(encoding='utf-8')}")

    # Cleanup
    target_file.unlink(missing_ok=True)
    Path("sandbox_data/nested_dir/report.txt").unlink(missing_ok=True)
    Path("sandbox_data/nested_dir").rmdir()
    Path("sandbox_data").rmdir()


def main() -> None:
    demo_pathlib_operations()
    demo_atomic_file_write()


if __name__ == "__main__":
    main()
