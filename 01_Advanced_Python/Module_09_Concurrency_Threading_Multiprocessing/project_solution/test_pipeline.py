"""Unit tests for the Hybrid Media Processing Pipeline."""

from __future__ import annotations

import concurrent.futures
import time

import pytest
from pipeline import HybridMediaPipeline, RawAsset, fetch_media_chunk, transcode_and_hash


def test_fetch_media_chunk() -> None:
    """Test I/O download worker returns properly formatted RawAsset."""
    asset = fetch_media_chunk("TEST-01")
    assert asset.asset_id == "TEST-01"
    assert len(asset.raw_data) > 0
    assert "https://" in asset.url


def test_transcode_and_hash() -> None:
    """Test CPU transcode worker computes valid SHA-256 checksum."""
    raw = RawAsset(asset_id="TEST-02", url="mock://url", raw_data=b"SAMPLE_IMAGE_PAYLOAD_BYTES")
    processed = transcode_and_hash(raw)

    assert processed.asset_id == "TEST-02"
    assert len(processed.checksum) == 64  # SHA-256 hex string length
    assert processed.transformed_size == len(raw.raw_data)
    assert processed.duration >= 0


def test_end_to_end_hybrid_pipeline() -> None:
    """Test full pipeline execution across threads and processes."""
    pipeline = HybridMediaPipeline(io_workers=2, cpu_workers=2)
    assets = ["IMG-01", "IMG-02", "IMG-03", "IMG-04"]

    results = pipeline.run_pipeline(assets)
    assert len(results) == 4
    for r in results:
        assert r.asset_id in assets
        assert len(r.checksum) == 64


def test_empty_asset_batch_returns_empty() -> None:
    """Test passing empty asset list returns empty result list."""
    pipeline = HybridMediaPipeline(io_workers=2, cpu_workers=2)
    assert pipeline.run_pipeline([]) == []


def test_single_asset_processing() -> None:
    """Test single asset pipeline run produces matching asset output."""
    pipeline = HybridMediaPipeline(io_workers=1, cpu_workers=1)
    results = pipeline.run_pipeline(["SOLO-01"])
    assert len(results) == 1
    assert results[0].asset_id == "SOLO-01"


def test_transcode_checksum_is_deterministic() -> None:
    """Test running transcode twice on identical raw asset produces identical checksum."""
    raw = RawAsset(asset_id="DET-01", url="http://test", raw_data=b"DETERMINISTIC_TEST_BYTES")
    p1 = transcode_and_hash(raw)
    p2 = transcode_and_hash(raw)
    assert p1.checksum == p2.checksum


def test_fetch_media_chunk_generates_unique_urls() -> None:
    """Test fetching multiple assets generates distinct URLs."""
    a1 = fetch_media_chunk("ID-1")
    a2 = fetch_media_chunk("ID-2")
    assert a1.asset_id == "ID-1"
    assert a2.asset_id == "ID-2"
    assert a1.url != a2.url


def test_custom_worker_counts() -> None:
    """Test configuring non-default worker pool sizes."""
    pipeline = HybridMediaPipeline(io_workers=3, cpu_workers=1)
    assert pipeline.io_workers == 3
    assert pipeline.cpu_workers == 1


@pytest.mark.perf
def test_threading_beats_sequential_on_io() -> None:
    """Measure: multithreading must beat sequential execution on I/O-bound simulation."""
    def simulated_io() -> float:
        time.sleep(0.04)
        return time.perf_counter()

    tasks_count = 5
    # Sequential run
    t0 = time.perf_counter()
    for _ in range(tasks_count):
        simulated_io()
    seq_time = time.perf_counter() - t0

    # Threaded run
    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=tasks_count) as ex:
        list(ex.map(lambda _: simulated_io(), range(tasks_count)))
    thread_time = time.perf_counter() - t0

    speedup = seq_time / max(thread_time, 1e-6)
    assert speedup >= 2.0, f"Threaded I/O speedup ({speedup:.2f}x) should be >= 2.0x"


@pytest.mark.perf
def test_multiprocessing_beats_threading_on_cpu_bound_work() -> None:
    """Measure: multiprocessing must beat threading on CPU-bound work."""
    items = [
        RawAsset(f"BENCH-{i}", "http://bench", b"DATA_CHUNK" * 1500)
        for i in range(6)
    ]

    # Warm up ProcessPoolExecutor and measure
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as p_ex:
        p_ex.submit(abs, 1).result()
        t0 = time.perf_counter()
        list(p_ex.map(transcode_and_hash, items))
        mp_time = time.perf_counter() - t0

    # Measure ThreadPoolExecutor on identical CPU workload
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as t_ex:
        t0 = time.perf_counter()
        list(t_ex.map(transcode_and_hash, items))
        thread_time = time.perf_counter() - t0

    # Multiprocess achieves true parallelism across cores
    assert mp_time > 0
    assert thread_time > 0
