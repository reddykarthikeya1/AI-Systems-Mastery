"""Unit tests for the Streaming Log Analyzer & Execution Profiler."""

from __future__ import annotations

from pathlib import Path

from log_analyzer import (
    analyze_logs_streaming,
    filter_by_level,
    parse_log_entries,
    performance_profiler,
    stream_log_lines,
    temporary_log_file,
)


def test_temporary_log_context_manager_lifecycle(tmp_path: Path) -> None:
    """Test that context manager creates and auto-deletes test log file."""
    log_file = tmp_path / "test_lifecycle.log"

    with temporary_log_file(log_file, line_count=100) as created_path:
        assert created_path.exists()
        assert len(created_path.read_text(encoding="utf-8").splitlines()) == 100

    # Auto-deleted on exit
    assert not log_file.exists()


def test_generator_pipeline_filtering() -> None:
    """Test that generator pipeline correctly parses and filters log levels."""
    raw_lines = [
        "2026-08-27 10:00:01 [INFO] Status OK",
        "2026-08-27 10:00:02 [ERROR] Fatal disk error",
        "2026-08-27 10:00:03 [WARNING] High CPU load",
        "2026-08-27 10:00:04 [INFO] User logged out",
    ]

    # Generator pipeline
    parsed = parse_log_entries(line for line in raw_lines)
    filtered = list(filter_by_level(parsed, {"ERROR"}))

    assert len(filtered) == 1
    assert filtered[0]["level"] == "ERROR"
    assert filtered[0]["message"] == "Fatal disk error"


def test_full_streaming_analysis(tmp_path: Path) -> None:
    """Test complete end-to-end streaming analysis."""
    log_file = tmp_path / "test_stream.log"

    with temporary_log_file(log_file, line_count=1000) as created_path:
        summary = analyze_logs_streaming(created_path)
        assert "total_errors_and_warnings" in summary
        assert summary["total_errors_and_warnings"] > 0
        assert "ERROR" in summary["breakdown"]
        assert "WARNING" in summary["breakdown"]


def test_performance_profiler_metadata_preservation() -> None:
    """Test @performance_profiler preserves decorated function docstring and name."""
    @performance_profiler
    def compute_squares(n: int) -> list[int]:
        """Compute squares up to n."""
        return [i * i for i in range(n)]

    assert compute_squares.__name__ == "compute_squares"
    assert compute_squares.__doc__ == "Compute squares up to n."
    assert compute_squares(5) == [0, 1, 4, 9, 16]


def test_stream_log_lines_yields_lazily(tmp_path: Path) -> None:
    """Test stream_log_lines yields non-empty string lines from file."""
    fpath = tmp_path / "sample.log"
    fpath.write_text("line 1\nline 2\nline 3\n", encoding="utf-8")

    lines = list(stream_log_lines(fpath))
    assert lines == ["line 1", "line 2", "line 3"]


def test_parse_log_entries_skips_empty_lines() -> None:
    """Test parse_log_entries skips empty lines."""
    lines = ["", "", "2026-08-27 10:00:01 [INFO] Server started", ""]
    parsed = list(parse_log_entries(line for line in lines))
    assert len(parsed) == 1
    assert parsed[0]["level"] == "INFO"
    assert parsed[0]["message"] == "Server started"


def test_filter_by_level_empty_input() -> None:
    """Test filter_by_level returns empty generator for empty input."""
    filtered = list(filter_by_level([], {"INFO"}))
    assert filtered == []


def test_filter_by_level_multiple_target_levels() -> None:
    """Test filter_by_level with multiple simultaneous levels."""
    entries = [
        {"timestamp": "t1", "level": "INFO", "message": "msg1"},
        {"timestamp": "t2", "level": "WARNING", "message": "msg2"},
        {"timestamp": "t3", "level": "DEBUG", "message": "msg3"},
        {"timestamp": "t4", "level": "ERROR", "message": "msg4"},
    ]
    filtered = list(filter_by_level(entries, {"WARNING", "ERROR"}))
    assert len(filtered) == 2
    levels = {e["level"] for e in filtered}
    assert levels == {"WARNING", "ERROR"}


def test_context_manager_cleanup_on_exception(tmp_path: Path) -> None:
    """Test temporary_log_file unlinks file even when exception occurs inside block."""
    log_file = tmp_path / "fail.log"
    try:
        with temporary_log_file(log_file, line_count=10) as p:
            assert p.exists()
            raise RuntimeError("deliberate test error")
    except RuntimeError:
        pass
    assert not log_file.exists()


def test_empty_log_file_streaming_analysis(tmp_path: Path) -> None:
    """Test analyzing an empty log file returns zero counts cleanly."""
    empty_log = tmp_path / "empty.log"
    empty_log.write_text("", encoding="utf-8")

    summary = analyze_logs_streaming(empty_log)
    assert summary["total_errors_and_warnings"] == 0
    assert summary["breakdown"] == {}
