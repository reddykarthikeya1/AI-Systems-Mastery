#!/usr/bin/env python3
"""Broken Asyncio Scraper demonstrating blocking sleep, forgotten await, and unretrieved exceptions."""

import asyncio
import time

async def fetch_url(url: str) -> str:
    time.sleep(0.5)
    return f"Content of {url}"

async def run_scraper():
    task = fetch_url("https://example.com")
    print(f"Task result without await: {task}")

async def faulty_background_task():
    await asyncio.sleep(0.1)
    raise ConnectionResetError("Remote server terminated connection")

async def main():
    print("Testing async loop...")
    t0 = time.perf_counter()
    await asyncio.gather(fetch_url("url1"), fetch_url("url2"))
    print(f"Elapsed: {time.perf_counter() - t0:.2f}s (Expected concurrent execution ~0.5s, got ~1.0s!)")

    await run_scraper()

    # Launch background task without error inspection
    bg = asyncio.create_task(faulty_background_task())
    await asyncio.sleep(0.2)

if __name__ == "__main__":
    asyncio.run(main())
