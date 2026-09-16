#!/usr/bin/env python3
"""High-Throughput Asynchronous Web Scraper & Health-Monitoring Daemon.

Module 10 Turnkey Project Implementation.
Demonstrates asyncio, asyncio.Queue, asyncio.Semaphore, and Async Worker Pools.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass


@dataclass
class HealthReport:
    url: str
    status_code: int
    response_time_ms: float
    is_healthy: bool
    error: str | None = None


class AsyncHealthMonitorDaemon:
    """Asynchronous monitoring daemon processing URLs via worker pools and semaphores."""

    def __init__(self, max_concurrency: int = 5, request_timeout: float = 1.0) -> None:
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.timeout = request_timeout
        self.queue: asyncio.Queue[str] = asyncio.Queue()
        self.reports: list[HealthReport] = []

    async def _fetch_url(self, url: str) -> HealthReport:
        """Simulates asynchronous HTTP GET with timeout and semaphore rate-limiting."""
        async with self.semaphore:
            start = time.perf_counter()
            try:
                # Enforce timeout deadline
                async with asyncio.timeout(self.timeout):
                    # Simulate variable network latency
                    if "timeout" in url:
                        await asyncio.sleep(2.0)
                    elif "error" in url:
                        await asyncio.sleep(0.02)
                        return HealthReport(url, 500, 20.0, False, "500 Internal Server Error")
                    else:
                        await asyncio.sleep(0.04)
                        elapsed_ms = (time.perf_counter() - start) * 1000
                        return HealthReport(url, 200, round(elapsed_ms, 2), True)
            except TimeoutError:
                return HealthReport(url, 504, self.timeout * 1000, False, "Request Timeout")

        return HealthReport(url, 0, 0.0, False, "Unknown Error")

    async def _worker(self, worker_id: int) -> None:
        """Background consumer coroutine."""
        while True:
            url = await self.queue.get()
            try:
                report = await self._fetch_url(url)
                self.reports.append(report)
            finally:
                self.queue.task_done()

    async def run_audit(self, urls: list[str], worker_count: int = 4) -> list[HealthReport]:
        """Populates queue and coordinates concurrent worker pool execution."""
        self.reports.clear()

        # Launch worker coroutines
        workers = [asyncio.create_task(self._worker(i)) for i in range(worker_count)]

        # Enqueue all target URLs
        for u in urls:
            await self.queue.put(u)

        # Wait until all URLs are fully processed
        await self.queue.join()

        # Cancel workers cleanly
        for w in workers:
            w.cancel()

        return list(self.reports)


async def main() -> None:
    print("=" * 65)
    print("      ASYNC WEB HEALTH MONITORING DAEMON DEMO")
    print("=" * 65)

    urls = [
        "https://api.gateway.com/health",
        "https://auth.service.com/ping",
        "https://billing.service.com/timeout",
        "https://database.node1.com/health",
        "https://cache.redis.com/error",
        "https://search.node.com/health",
    ]

    daemon = AsyncHealthMonitorDaemon(max_concurrency=3, request_timeout=0.2)

    start = time.perf_counter()
    reports = await daemon.run_audit(urls, worker_count=3)
    duration = time.perf_counter() - start

    print(f"\nAudited {len(reports)} services concurrently in {duration:.3f}s:")
    for r in reports:
        status_symbol = "[OK]    " if r.is_healthy else "[FAILED]"
        print(f"  {status_symbol} {r.url:<35} | Code: {r.status_code} | Latency: {r.response_time_ms:.1f}ms | Err: {r.error}")


if __name__ == "__main__":
    asyncio.run(main())
