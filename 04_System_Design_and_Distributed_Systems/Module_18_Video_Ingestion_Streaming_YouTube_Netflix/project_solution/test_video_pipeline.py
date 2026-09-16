"""Unit tests for Video Ingest, Transcoding DAG & HLS Manifest Generation."""

from __future__ import annotations

import pytest
from video_pipeline import (
    ChunkedUploadCoordinator,
    HLSManifestGenerator,
    TranscodeJobDAG,
    UploadStatus,
)


def test_chunked_multipart_upload_reassembly() -> None:
    coord = ChunkedUploadCoordinator(upload_id="up-992", total_chunks=3)
    assert coord.status == UploadStatus.UPLOADING

    part0 = b"VIDEO_HEADER_METADATA_"
    part1 = b"FRAME_DATA_CHUNK_001_"
    part2 = b"AUDIO_TRACK_END"

    coord.upload_chunk(0, part0)
    assert coord.status == UploadStatus.UPLOADING

    coord.upload_chunk(1, part1)
    assert coord.status == UploadStatus.UPLOADING

    coord.upload_chunk(2, part2)
    assert coord.status == UploadStatus.COMPLETED

    assembled = coord.assemble_file()
    assert assembled == part0 + part1 + part2


def test_chunked_upload_premature_assembly_raises() -> None:
    coord = ChunkedUploadCoordinator(upload_id="up-incomplete", total_chunks=2)
    coord.upload_chunk(0, b"part0")

    with pytest.raises(RuntimeError, match="Cannot assemble upload"):
        coord.assemble_file()


def test_transcoding_dag_execution() -> None:
    dag = TranscodeJobDAG(video_id="vid-100")
    dummy_payload = b"0" * 1024

    variants = dag.execute_dag(dummy_payload)

    # Invariant: Must produce 3 standard profiles: 1080p, 720p, 480p
    assert "1080p" in variants
    assert "720p" in variants
    assert "480p" in variants

    v1080 = variants["1080p"]
    assert len(v1080.segment_uris) == 3
    assert v1080.profile.target_bitrate_kbps == 5000


def test_hls_master_manifest_generation() -> None:
    dag = TranscodeJobDAG(video_id="vid-200")
    variants = dag.execute_dag(b"raw_bytes")

    manifest = HLSManifestGenerator.generate_master_manifest(variants)

    assert "#EXTM3U" in manifest
    assert "BANDWIDTH=5000000,RESOLUTION=1920x1080" in manifest
    assert "BANDWIDTH=2500000,RESOLUTION=1280x720" in manifest
    assert "BANDWIDTH=1000000,RESOLUTION=854x480" in manifest
    assert "/media/vid-200/1080p/prog_index.m3u8" in manifest
