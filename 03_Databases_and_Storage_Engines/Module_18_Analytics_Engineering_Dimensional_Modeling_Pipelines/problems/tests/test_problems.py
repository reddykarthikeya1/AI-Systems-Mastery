"""Tests for Scd Type2 Dimension Merge."""
from __future__ import annotations

import pytest
from p01_scd_type2_dimension_merge import scd_type2_dimension_merge


def test_scd_type2_dimension_merge():
    dims = [{
        'id': 1, 'natural_key': 'cust_101', 'val': 'NY',
        'valid_from': '2025-01-01', 'valid_to': None, 'is_current': True
    }]
    updated = scd_type2_dimension_merge(dims, {'natural_key': 'cust_101', 'val': 'CA'}, '2025-06-01')
    assert len(updated) == 2
    assert updated[0]['is_current'] is False
    assert updated[0]['valid_to'] == '2025-06-01'
    assert updated[1]['is_current'] is True
    assert updated[1]['val'] == 'CA'
