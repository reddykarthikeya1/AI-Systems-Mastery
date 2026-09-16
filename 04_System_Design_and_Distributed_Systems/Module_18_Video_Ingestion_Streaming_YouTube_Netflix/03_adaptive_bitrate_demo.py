#!/usr/bin/env python3
"""Module 18 Demo: Resumable Chunked Upload & Adaptive Bitrate Streaming Simulation."""

import sys
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from video_pipeline import (
    ChunkedUploadCoordinator,
    HLSManifestGenerator,
    TranscodeJobDAG,
)


def main() -> None:
    print("=" * 72)
    print("  MODULE 18: VIDEO INGESTION & HLS ADAPTIVE STREAMING DEMO")
    print("=" * 72)

    # 1. Resumable Chunked Upload
    print("\n--- 1. Resumable Multipart Upload (Uploading 15MB 4K Raw Segment) ---")
    coordinator = ChunkedUploadCoordinator(upload_id="upload-4k-alpha", total_chunks=3)

    chunks = [
        (0, b"[H.264 HEVC HEADER 0x001]" * 100),
        (1, b"[I-FRAME KEYFRAME DATA 0x002]" * 100),
        (2, b"[AUDIO AAC STEREO 0x003]" * 100),
    ]

    for idx, data in chunks:
        coordinator.upload_chunk(idx, data)
        print(f"  Uploaded Chunk #{idx}: {len(data):,d} bytes | Checksum: {coordinator.uploaded_chunks[idx].checksum[:10]}...")

    raw_video = coordinator.assemble_file()
    print(f"Assembly Complete! Total Video File Size: {len(raw_video):,d} bytes")

    # 2. Transcoding DAG
    print("\n--- 2. Parallel Transcoding DAG Pipeline ---")
    dag = TranscodeJobDAG(video_id="video-tutorial-42")
    variants = dag.execute_dag(raw_video)

    for name, var in variants.items():
        print(f"  Encoded Variant [{name}]: Bitrate={var.profile.target_bitrate_kbps} kbps | Segments={len(var.segment_uris)} .ts files")

    # 3. Master HLS Manifest Generation
    print("\n--- 3. RFC-8216 HLS Master Playlist (master.m3u8) ---")
    manifest = HLSManifestGenerator.generate_master_manifest(variants)
    print(manifest.strip())

    # 4. Adaptive Bitrate Client Simulation
    print("\n--- 4. Client Video Player Adaptive Bitrate (ABR) Switching ---")
    bandwidth_scenarios = [
        (8000, "High-Speed Fiber (8 Mbps)"),
        (2200, "4G Mobile Congestion (2.2 Mbps)"),
        (800,  "Weak 3G Signal (800 kbps)"),
    ]

    for bw_kbps, label in bandwidth_scenarios:
        # Find best variant that fits within bandwidth with 20% safety margin
        budget = bw_kbps * 0.80
        playable = [v for v in variants.values() if v.profile.target_bitrate_kbps <= budget]
        chosen = max(playable, key=lambda v: v.profile.target_bitrate_kbps) if playable else variants["480p"]
        print(f"  Network: {label:<30} -> ABR Player switches to: {chosen.profile.resolution_name} ({chosen.profile.target_bitrate_kbps} kbps)")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
