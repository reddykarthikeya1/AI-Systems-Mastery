"""Tests for Base62 Url Encoder."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_base62_url_encoder import base62_url_encoder
except ImportError:
    from p01_base62_url_encoder import base62_url_encoder


def test_base62_url_encoder():
    assert base62_url_encoder(0) == "0"
    assert base62_url_encoder(61) == "Z"
    assert base62_url_encoder(62) == "10"
    assert len(base62_url_encoder(125_000_000_000)) <= 7
