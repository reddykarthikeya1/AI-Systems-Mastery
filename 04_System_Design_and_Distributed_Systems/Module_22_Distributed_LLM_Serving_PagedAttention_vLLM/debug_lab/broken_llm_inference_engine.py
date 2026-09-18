#!/usr/bin/env python3
"""DEBUG LAB: GPU Out-of-Memory Crash Caused by KV-Cache Internal Fragmentation

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def preallocate_kv_cache(max_seq_len: int = 4096, batch_size: int = 12, bytes_per_token: int = 2097152):
    total_needed = max_seq_len * batch_size * bytes_per_token
    if total_needed > 80 * 1024 * 1024 * 1024:
        raise MemoryError(f'GPU OOM! Required {total_needed / 10**9:.1f} GB VRAM for static allocation!')


def reproduce_defect():
    print("Executing defective simulation for Module_22_Distributed_LLM_Serving_PagedAttention_vLLM...")
    preallocate_kv_cache()
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
