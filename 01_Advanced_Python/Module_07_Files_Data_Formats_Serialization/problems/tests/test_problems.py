"""Tests for Atomic File Write Commit."""
from __future__ import annotations

import pytest
from p01_atomic_write_simulation import atomic_commit_payload


def test_atomic_commit_payload():
    d = {}
    assert atomic_commit_payload(d, 'config.json', '{"port": 8080}') is True
    assert 'config.json' in d
    assert 'config.json.tmp' not in d
    assert d['config.json'] == '{"port": 8080}'
