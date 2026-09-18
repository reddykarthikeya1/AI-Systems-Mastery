"""Tests for Multi Head Attention Mask."""
from __future__ import annotations

import pytest
from p01_multi_head_attention_mask import multi_head_attention_mask


def test_multi_head_attention_mask():
    scores = [[1.0, 2.0], [3.0, 4.0]]
    masked = multi_head_attention_mask(scores)
    assert masked[0][0] == 1.0
    assert masked[0][1] == -1e9  # future masked
    assert masked[1][0] == 3.0
    assert masked[1][1] == 4.0
