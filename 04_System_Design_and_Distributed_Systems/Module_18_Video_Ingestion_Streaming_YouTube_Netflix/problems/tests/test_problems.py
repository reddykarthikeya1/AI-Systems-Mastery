"""Tests for Adaptive Bitrate Manifest."""
from __future__ import annotations

import pytest
from p01_adaptive_bitrate_manifest import adaptive_bitrate_manifest


def test_adaptive_bitrate_manifest():
    assert adaptive_bitrate_manifest(15.0, 6.0) == [(0, 6.0), (1, 6.0), (2, 3.0)]
    assert adaptive_bitrate_manifest(0.0) == []
