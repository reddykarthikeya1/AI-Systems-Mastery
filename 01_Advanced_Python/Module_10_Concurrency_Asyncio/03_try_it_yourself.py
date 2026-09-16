"""
Module 10: Interactive AsyncIO Concurrency Demo
Run: python try_it_yourself.py
"""

import asyncio
import time


async def download_file(filename, wait_seconds):
    print(f"  [+] Downloading {filename} ({wait_seconds}s)...")
    await asyncio.sleep(wait_seconds)
    print(f"  [OK] Saved {filename}!")
    return f"{filename} (OK)"


async def async_main():
    print("=" * 60)
    print("  MODULE 10: ASYNCIO EVENT LOOP PLAYGROUND [*]")
    print("=" * 60)
    start = time.time()

    print("\nLaunching 3 concurrent downloads on 1 single thread:")
    results = await asyncio.gather(
        download_file("file_1.zip", 0.6),
        download_file("file_2.zip", 0.4),
        download_file("file_3.zip", 0.5),
    )

    elapsed = time.time() - start
    print(f"\nAll downloads completed in {elapsed:.2f}s!")
    print("If run sequentially, it would have taken 1.50s.")
    print("Results:", results)


if __name__ == "__main__":
    asyncio.run(async_main())
