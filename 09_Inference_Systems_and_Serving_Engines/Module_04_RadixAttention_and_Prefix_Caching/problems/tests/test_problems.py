"""Tests for Radix Tree Prefix Matcher."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_radix_tree_prefix_matcher import radix_tree_prefix_matcher
except ImportError:
    from p01_radix_tree_prefix_matcher import radix_tree_prefix_matcher


def test_radix_tree_prefix_matcher():
    prefixes = [
        [101, 205, 303],
        [101, 205, 999],
        [555]
    ]
    query = [101, 205, 303, 404]
    idx, l = radix_tree_prefix_matcher(prefixes, query)
    assert idx == 0 and l == 3
