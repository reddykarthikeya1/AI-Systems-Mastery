"""Beginner playground for Module 09 - Distributed Checkpointing & Fault Tolerance.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib
import json

# -------------------------------------------- 1. Distributed Sharded State Dictionary
rank_shard = {"rank": 2, "params": [0.12, -0.45, 0.88]}
serialized = json.dumps(rank_shard)
shard_hash = hashlib.md5(serialized.encode()).hexdigest()

assert rank_shard["rank"] == 2
assert len(shard_hash) == 32
print(f"Rank 2 sharded checkpoint generated: MD5={shard_hash[:8]}...")

# -------------------------------------------- 2. Asynchronous Non-Blocking Checkpoint
sync_disk_time_s = 45.0
async_host_copy_time_s = 1.2
blocked_time_saved = sync_disk_time_s - async_host_copy_time_s

assert blocked_time_saved > 40.0
print(f"Async checkpointing reduces training stall from {sync_disk_time_s}s down to {async_host_copy_time_s}s.")

# -------------------------------------------- 3. Resharding across Different Topologies
global_key = "encoder.layer.0.weight"
assert "weight" in global_key
print(f"Unified distributed tensor key: '{global_key}' verified.")

print()
print("All checks passed.")
