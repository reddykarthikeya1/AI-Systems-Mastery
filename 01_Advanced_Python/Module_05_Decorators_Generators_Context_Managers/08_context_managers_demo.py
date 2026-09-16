#!/usr/bin/env python3
"""Module 05: Context Managers Demonstration.

This script demonstrates class-based context managers (__enter__ / __exit__),
@contextlib.contextmanager generator syntax, and exception handling inside context blocks.
"""

from __future__ import annotations

import time
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path


class ManagedTemporaryFile:
    """Class-based context manager creating an auto-deleting scratch file."""

    def __init__(self, filename: str) -> None:
        self.path = Path(filename)

    def __enter__(self) -> Path:
        print(f"[ENTER] Creating scratch file: {self.path.name}")
        self.path.write_text("Temporary scratch buffer data", encoding="utf-8")
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        print(f"[EXIT] Cleaning up scratch file: {self.path.name}")
        self.path.unlink(missing_ok=True)
        # Returning False allows any exception to propagate naturally
        return False


@contextmanager
def execution_block_timer(task_name: str) -> Generator[None, None, None]:
    """Generator-based context manager measuring execution time."""
    start = time.perf_counter()
    print(f"\n[START] Task: {task_name}")
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[FINISH] Task '{task_name}' completed in {elapsed:.4f}s")


def main() -> None:
    print("=" * 60)
    print("  1. Class-Based Context Manager (ManagedTemporaryFile)")
    print("=" * 60)

    with ManagedTemporaryFile("scratch_demo.tmp") as temp_file:
        print(f"Inside 'with' block -> File exists: {temp_file.exists()}")
        content = temp_file.read_text(encoding="utf-8")
        print(f"Read content: '{content}'")

    print(f"Outside 'with' block -> File exists: {Path('scratch_demo.tmp').exists()}")

    print("\n" + "=" * 60)
    print("  2. Generator-Based Context Manager (@contextmanager)")
    print("=" * 60)

    with execution_block_timer("Data Transformation Block"):
        total = sum(x ** 2 for x in range(500_000))
        print(f"Sum computed: {total}")


if __name__ == "__main__":
    main()
