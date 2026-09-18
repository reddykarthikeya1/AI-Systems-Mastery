"""Tests for Weighted Least Connections."""
from __future__ import annotations

import pytest
from p01_weighted_least_connections import weighted_least_connections


def test_weighted_least_connections():
    servers = [
        {'id': 'srv1', 'weight': 2, 'active_conns': 10, 'is_healthy': True},   # 10/2 = 5.0
        {'id': 'srv2', 'weight': 1, 'active_conns': 4, 'is_healthy': True},    # 4/1 = 4.0
        {'id': 'srv3', 'weight': 5, 'active_conns': 2, 'is_healthy': False},   # unhealthy
    ]
    assert weighted_least_connections(servers) == 'srv2'
    assert weighted_least_connections([{'id': 's1', 'weight': 1, 'active_conns': 0, 'is_healthy': False}]) is None
