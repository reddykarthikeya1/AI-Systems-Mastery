"""Tests for SemVer 2.0.0 Tri-Part Comparison."""
from __future__ import annotations

import pytest
from p01_semver_comparator import compare_semver


def test_semver_comparator():
    assert compare_semver('1.2.3', '1.2.4') == -1
    assert compare_semver('2.0.0', '1.9.9') == 1
    assert compare_semver('1.0.0', '1.0.0') == 0
