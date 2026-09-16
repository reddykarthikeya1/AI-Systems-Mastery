#!/usr/bin/env python3
"""Module 18: In-Process Architectural Simulation Model: Video Ingestion, Transcoding DAG & HLS Streaming Engine.

Implements:
- Resumable Chunked Multipart Upload Coordinator
- Asynchronous Video Transcoding DAG (Directed Acyclic Graph)
- Adaptive Bitrate (ABR) HLS Master Playlist & Variant Generator
"""

from __future__ import annotations

import hashlib
import threading
from dataclasses import dataclass
from enum import StrEnum


class UploadStatus(StrEnum):
    UPLOADING = "UPLOADING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class UploadChunk:
    chunk_index: int
    data_bytes: bytes
    checksum: str


class ChunkedUploadCoordinator:
    """Manages resumable multipart uploads for large multi-gigabyte video files."""

    def __init__(self, upload_id: str, total_chunks: int) -> None:
        self.upload_id = upload_id
        self.total_chunks = total_chunks
        self.uploaded_chunks: dict[int, UploadChunk] = {}
        self.status = UploadStatus.UPLOADING
        self._lock = threading.Lock()

    def upload_chunk(self, chunk_index: int, data: bytes) -> bool:
        if chunk_index < 0 or chunk_index >= self.total_chunks:
            raise ValueError(f"Chunk index {chunk_index} out of range [0, {self.total_chunks - 1}]")

        computed_checksum = hashlib.md5(data).hexdigest()
        with self._lock:
            self.uploaded_chunks[chunk_index] = UploadChunk(
                chunk_index=chunk_index,
                data_bytes=data,
                checksum=computed_checksum,
            )
            if len(self.uploaded_chunks) == self.total_chunks:
                self.status = UploadStatus.COMPLETED
            return True

    def assemble_file(self) -> bytes:
        """Reassembles all ordered chunks into the complete raw video payload."""
        with self._lock:
            if self.status != UploadStatus.COMPLETED:
                raise RuntimeError(
                    f"Cannot assemble upload: only {len(self.uploaded_chunks)}/{self.total_chunks} uploaded"
                )

            reassembled = bytearray()
            for idx in range(self.total_chunks):
                reassembled.extend(self.uploaded_chunks[idx].data_bytes)
            return bytes(reassembled)


@dataclass(frozen=True)
class TranscodeProfile:
    resolution_name: str  # e.g., "1080p", "720p", "480p"
    width: int
    height: int
    target_bitrate_kbps: int
    codec: str = "H.264"


STANDARD_PROFILES = [
    TranscodeProfile("1080p", 1920, 1080, 5000),
    TranscodeProfile("720p", 1280, 720, 2500),
    TranscodeProfile("480p", 854, 480, 1000),
]


@dataclass
class TranscodedVariant:
    profile: TranscodeProfile
    segment_uris: list[str]
    playlist_uri: str


class TranscodeJobDAG:
    """Orchestrates parallel encoding tasks across resolution profiles."""

    def __init__(self, video_id: str, profiles: list[TranscodeProfile] | None = None) -> None:
        self.video_id = video_id
        self.profiles = profiles or STANDARD_PROFILES

    def execute_dag(self, raw_data: bytes) -> dict[str, TranscodedVariant]:
        """Simulates executing transcoding tasks in parallel for all target profiles."""
        variants: dict[str, TranscodedVariant] = {}

        # Split simulated video into 3 chunks of 10-second segments per profile
        for prof in self.profiles:
            segment_uris = [
                f"/media/{self.video_id}/{prof.resolution_name}/segment_{i:03d}.ts"
                for i in range(3)
            ]
            playlist_uri = f"/media/{self.video_id}/{prof.resolution_name}/prog_index.m3u8"
            variants[prof.resolution_name] = TranscodedVariant(
                profile=prof,
                segment_uris=segment_uris,
                playlist_uri=playlist_uri,
            )

        return variants


class HLSManifestGenerator:
    """Generates standard RFC-8216 compliant HLS Master Playlist."""

    @staticmethod
    def generate_master_manifest(variants: dict[str, TranscodedVariant]) -> str:
        lines = [
            "#EXTM3U",
            "#EXT-X-VERSION:3",
        ]

        # Sort profiles from highest bitrate to lowest
        sorted_variants = sorted(
            variants.values(),
            key=lambda v: v.profile.target_bitrate_kbps,
            reverse=True,
        )

        for v in sorted_variants:
            bandwidth_bps = v.profile.target_bitrate_kbps * 1000
            res_str = f"{v.profile.width}x{v.profile.height}"
            lines.append(
                f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth_bps},RESOLUTION={res_str},CODECS=\"avc1.640028,mp4a.40.2\""
            )
            lines.append(v.playlist_uri)

        return "\n".join(lines) + "\n"
