#!/usr/bin/env python3
"""DEBUG LAB: Transcoding Worker OOM Crash on Unbounded Video Resolution Ingestion

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def transcode_video_chunk(chunk_bytes: bytes):
    if len(chunk_bytes) > 500 * 1024 * 1024:
        raise MemoryError('OOM: video chunk exceeds 500MB max buffer allocation!')


def reproduce_defect():
    print("Executing defective simulation for Module_18_Video_Ingestion_Streaming_YouTube_Netflix...")
    transcode_video_chunk(b'0' * (600 * 1024 * 1024))
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
