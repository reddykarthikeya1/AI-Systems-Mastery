"""Tests for Binary Struct Network Protocol Header."""
from __future__ import annotations

import pytest
from p01_binary_header_packer import pack_protocol_header, unpack_protocol_header


def test_binary_header_packer():
    b = pack_protocol_header(1, 1024, 0xAA55)
    assert len(b) == 8
    assert unpack_protocol_header(b) == (1, 1024, 0xAA55)
