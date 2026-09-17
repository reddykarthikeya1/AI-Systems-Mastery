"""Pytest suite for PyTorch Fundamentals problem bank."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Test the solution by default, or stub if imported from problems/
SOL_DIR = Path(__file__).resolve().parent.parent / "solutions"
PROB_DIR = Path(__file__).resolve().parent.parent
if str(SOL_DIR) not in sys.path:
    sys.path.insert(0, str(SOL_DIR))

from p01_compute_attention_budget import compute_attention_budget


def test_compute_attention_budget():
    res = compute_attention_budget(seq_len=1024, num_heads=32, head_dim=128, batch_size=2)
    assert res["kv_cache_bytes"] == 2 * 1024 * (4 * 32 * 128)
    assert res["attn_flops"] == 4 * 2 * 32 * (1024**2) * 128

