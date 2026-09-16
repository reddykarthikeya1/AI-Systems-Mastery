#!/usr/bin/env python3
"""Streaming Log Analyzer & Execution Profiler.

Module 05 Turnkey Project Implementation.
Demonstrates Generators, Yield Pipelines, Decorators, and Context Managers.
"""

from __future__ import annotations

import functools
import time
from collections import Counter
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path


def performance_profiler(func):
    """Decorator measuring execution duration and line throughput."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"[PROFILER] '{func.__name__}' completed in {duration:.4f} seconds.")
        return result
    return wrapper


@contextmanager
def temporary_log_file(filepath: Path, line_count: int = 50_000) -> Generator[Path, None, None]:
    """Context manager that generates a mock high-volume server log and auto-cleans on exit."""
    print(f"[SETUP] Generating {line_count:,} mock log entries at '{filepath.name}'...")
    log_templates = [
        "2026-08-27 10:00:{sec:02d} [INFO] User {uid} GET /api/v1/status 200",
        "2026-08-27 10:00:{sec:02d} [INFO] User {uid} POST /api/v1/orders 201",
        "2026-08-27 10:00:{sec:02d} [WARNING] High response latency {uid} 429",
        "2026-08-27 10:00:{sec:02d} [ERROR] Database deadlock on user {uid} 500",
        "2026-08-27 10:00:{sec:02d} [ERROR] Redis timeout on session {uid} 503",
    ]

    with open(filepath, "w", encoding="utf-8") as f:
        for i in range(line_count):
            template = log_templates[i % len(log_templates)]
            f.write(template.format(sec=i % 60, uid=1000 + (i % 50)) + "\n")

    try:
        yield filepath
    finally:
        print(f"[CLEANUP] Removing mock log file: {filepath.name}")
        filepath.unlink(missing_ok=True)


def stream_log_lines(filepath: Path) -> Generator[str, None, None]:
    """Generator 1: Lazily streams lines from file without loading entire file into RAM."""
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            yield line.strip()


def parse_log_entries(line_stream: Generator[str, None, None]) -> Generator[dict[str, str], None, None]:
    """Generator 2: Lazily parses raw text lines into structured dictionaries."""
    for line in line_stream:
        if not line:
            continue
        parts = line.split(" ", 3)
        if len(parts) >= 4:
            yield {
                "timestamp": f"{parts[0]} {parts[1]}",
                "level": parts[2].strip("[]"),
                "message": parts[3],
            }


def filter_by_level(
    entry_stream: Generator[dict[str, str], None, None],
    target_levels: set[str],
) -> Generator[dict[str, str], None, None]:
    """Generator 3: Lazily filters log records matching target severity levels."""
    for entry in entry_stream:
        if entry["level"] in target_levels:
            yield entry


@performance_profiler
def analyze_logs_streaming(filepath: Path) -> dict[str, object]:
    """Connects the generator pipeline and aggregates frequency analytics."""
    raw_lines = stream_log_lines(filepath)
    parsed_entries = parse_log_entries(raw_lines)
    errors_and_warnings = filter_by_level(parsed_entries, {"ERROR", "WARNING"})

    severity_counts: Counter[str] = Counter()
    total_processed = 0

    for entry in errors_and_warnings:
        severity_counts[entry["level"]] += 1
        total_processed += 1

    return {
        "total_errors_and_warnings": total_processed,
        "breakdown": dict(severity_counts),
    }


def main() -> None:
    print("=" * 65)
    print("      STREAMING SERVER LOG ANALYZER & PROFILER")
    print("=" * 65)

    test_log_path = Path("production_server.log")

    # Use context manager to handle lifecycle of 50,000 log lines
    with temporary_log_file(test_log_path, line_count=50_000) as log_file:
        print("\n[STREAMING] Executing generator pipeline...")
        summary = analyze_logs_streaming(log_file)
        print("\nAnalysis Summary:")
        print(f"  Total Anomalies Detected: {summary['total_errors_and_warnings']:,}")
        print(f"  Severity Breakdown      : {summary['breakdown']}")


if __name__ == "__main__":
    main()
