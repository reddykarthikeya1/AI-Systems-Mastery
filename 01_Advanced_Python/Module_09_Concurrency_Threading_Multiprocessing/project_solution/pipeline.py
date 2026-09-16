#!/usr/bin/env python3
"""Hybrid Media Processing Pipeline (Threading + Multiprocessing).

Module 09 Turnkey Project Implementation.
Demonstrates ThreadPoolExecutor for I/O and ProcessPoolExecutor for CPU parallelism.
"""

from __future__ import annotations

import hashlib
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass


@dataclass
class RawAsset:
    asset_id: str
    url: str
    raw_data: bytes


@dataclass
class ProcessedAsset:
    asset_id: str
    checksum: str
    transformed_size: int
    duration: float


# ==========================================
# 1. I/O-Bound Download Worker (Thread-Safe)
# ==========================================

def fetch_media_chunk(asset_id: str) -> RawAsset:
    """Simulates high-speed network download of a raw media file (I/O-Bound)."""
    # Simulate network latency
    time.sleep(0.05)
    mock_payload = f"RAW_MEDIA_STREAM_DATA_FOR_{asset_id}_{time.time()}".encode() * 1000
    return RawAsset(asset_id=asset_id, url=f"https://s3.cloud.com/media/{asset_id}", raw_data=mock_payload)


# ==========================================
# 2. CPU-Bound Transcoding Worker (Process-Safe)
# ==========================================

def transcode_and_hash(asset: RawAsset) -> ProcessedAsset:
    """Simulates CPU-heavy image resizing, frame transformations, and SHA-256 hashing."""
    start = time.perf_counter()

    # Heavy CPU crunch simulation
    hasher = hashlib.sha256()
    for _ in range(50_000):
        hasher.update(asset.raw_data[:256])

    elapsed = time.perf_counter() - start
    return ProcessedAsset(
        asset_id=asset.asset_id,
        checksum=hasher.hexdigest(),
        transformed_size=len(asset.raw_data),
        duration=elapsed,
    )


# ==========================================
# 3. Hybrid Orchestrator Pipeline
# ==========================================

class HybridMediaPipeline:
    """Orchestrates I/O thread pool downloads followed by multi-process CPU crunching."""

    def __init__(self, io_workers: int = 8, cpu_workers: int | None = None) -> None:
        self.io_workers = io_workers
        self.cpu_workers = cpu_workers

    def run_pipeline(self, asset_ids: list[str]) -> list[ProcessedAsset]:
        print(f"\n[PHASE 1] Concurrently downloading {len(asset_ids)} assets using {self.io_workers} I/O threads...")
        start_download = time.perf_counter()
        with ThreadPoolExecutor(max_workers=self.io_workers) as thread_pool:
            raw_assets = list(thread_pool.map(fetch_media_chunk, asset_ids))
        download_time = time.perf_counter() - start_download
        print(f"  Downloaded {len(raw_assets)} assets in {download_time:.3f}s")

        print(f"\n[PHASE 2] Parallel CPU transcoding {len(raw_assets)} assets across CPU cores...")
        start_cpu = time.perf_counter()
        with ProcessPoolExecutor(max_workers=self.cpu_workers) as process_pool:
            processed_assets = list(process_pool.map(transcode_and_hash, raw_assets))
        cpu_time = time.perf_counter() - start_cpu
        print(f"  Transcoded {len(processed_assets)} assets in {cpu_time:.3f}s")

        return processed_assets


def main() -> None:
    print("=" * 65)
    print("      HYBRID MEDIA & TRANSCODING PIPELINE SIMULATION")
    print("=" * 65)

    asset_ids = [f"ASSET-{i:03d}" for i in range(1, 13)]
    pipeline = HybridMediaPipeline(io_workers=6)

    total_start = time.perf_counter()
    results = pipeline.run_pipeline(asset_ids)
    total_elapsed = time.perf_counter() - total_start

    print("\n" + "=" * 65)
    print(f"Pipeline Completed {len(results)} assets in {total_elapsed:.3f} total seconds!")
    print(f"First Processed Asset Checksum: {results[0].checksum[:16]}...")


if __name__ == "__main__":
    main()
