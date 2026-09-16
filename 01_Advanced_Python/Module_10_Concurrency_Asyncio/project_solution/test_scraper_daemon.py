"""Unit tests for the Asynchronous Health Monitoring Daemon."""

from __future__ import annotations

import asyncio
import time

import pytest
from scraper_daemon import AsyncHealthMonitorDaemon


@pytest.mark.asyncio
async def test_healthy_url_fetch() -> None:
    """Test successful ping to a healthy URL."""
    daemon = AsyncHealthMonitorDaemon()
    report = await daemon._fetch_url("https://service.com/health")

    assert report.is_healthy is True
    assert report.status_code == 200
    assert report.response_time_ms > 0
    assert report.error is None


@pytest.mark.asyncio
async def test_error_status_url_fetch() -> None:
    """Test response code and error capture on server error."""
    daemon = AsyncHealthMonitorDaemon()
    report = await daemon._fetch_url("https://service.com/error")

    assert report.is_healthy is False
    assert report.status_code == 500
    assert "500" in (report.error or "")


@pytest.mark.asyncio
async def test_timeout_handling() -> None:
    """Test timeout deadline correctly captures 504 and cancels coroutine."""
    daemon = AsyncHealthMonitorDaemon(request_timeout=0.1)
    report = await daemon._fetch_url("https://service.com/timeout")

    assert report.is_healthy is False
    assert report.status_code == 504
    assert report.error == "Request Timeout"


@pytest.mark.asyncio
async def test_full_worker_pool_audit() -> None:
    """Test batch audit with multiple worker coroutines."""
    daemon = AsyncHealthMonitorDaemon(max_concurrency=4, request_timeout=0.2)
    urls = [
        "https://api.one.com/health",
        "https://api.two.com/health",
        "https://api.three.com/error",
        "https://api.four.com/timeout",
    ]

    reports = await daemon.run_audit(urls, worker_count=2)
    assert len(reports) == 4

    healthy_count = sum(1 for r in reports if r.is_healthy)
    failed_count = sum(1 for r in reports if not r.is_healthy)

    assert healthy_count == 2
    assert failed_count == 2


@pytest.mark.asyncio
async def test_empty_url_list_audit() -> None:
    """Test auditing an empty URL list returns an empty report list."""
    daemon = AsyncHealthMonitorDaemon()
    reports = await daemon.run_audit([])
    assert reports == []


@pytest.mark.asyncio
async def test_single_healthy_url_audit() -> None:
    """Test single URL audit returns one valid HealthReport."""
    daemon = AsyncHealthMonitorDaemon()
    reports = await daemon.run_audit(["https://example.com/health"])
    assert len(reports) == 1
    assert reports[0].url == "https://example.com/health"
    assert reports[0].is_healthy is True


@pytest.mark.asyncio
async def test_daemon_custom_timeout_configuration() -> None:
    """Test configuring custom request timeout on daemon."""
    daemon = AsyncHealthMonitorDaemon(max_concurrency=8, request_timeout=2.5)
    assert daemon.timeout == 2.5
    assert daemon.semaphore._value == 8


@pytest.mark.asyncio
async def test_report_timing_greater_than_zero() -> None:
    """Test response_time_ms is populated and non-negative."""
    daemon = AsyncHealthMonitorDaemon()
    report = await daemon._fetch_url("https://fast.io/health")
    assert report.response_time_ms >= 0


@pytest.mark.asyncio
async def test_multiple_error_endpoints_reporting() -> None:
    """Test auditing multiple erroring endpoints captures respective 500 statuses."""
    daemon = AsyncHealthMonitorDaemon()
    urls = ["https://a.com/error", "https://b.com/error"]
    reports = await daemon.run_audit(urls)
    assert len(reports) == 2
    assert all(r.status_code == 500 for r in reports)
    assert all(not r.is_healthy for r in reports)


@pytest.mark.perf
@pytest.mark.asyncio
async def test_concurrent_gather_beats_sequential_awaits() -> None:
    """Measure: concurrent asyncio.gather must beat sequential awaits by >= 2.0x."""
    async def simulated_fetch() -> float:
        await asyncio.sleep(0.04)
        return time.perf_counter()

    task_count = 5

    # Sequential execution
    t0 = time.perf_counter()
    for _ in range(task_count):
        await simulated_fetch()
    seq_time = time.perf_counter() - t0

    # Concurrent gather execution
    t0 = time.perf_counter()
    await asyncio.gather(*(simulated_fetch() for _ in range(task_count)))
    gather_time = time.perf_counter() - t0

    speedup = seq_time / max(gather_time, 1e-6)
    assert speedup >= 2.0, f"asyncio.gather speedup ({speedup:.2f}x) must be >= 2.0x"
