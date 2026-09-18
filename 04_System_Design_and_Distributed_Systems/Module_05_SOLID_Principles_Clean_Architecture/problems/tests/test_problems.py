"""Tests for Dependency Inversion Container."""
from __future__ import annotations

import pytest
from p01_dependency_inversion_container import dependency_inversion_container


def test_dependency_inversion_container():
    deps = {
        'Controller': ['Service'],
        'Service': ['Repository'],
        'Repository': ['Database'],
        'Database': []
    }
    order = dependency_inversion_container(deps)
    assert order.index('Database') < order.index('Repository') < order.index('Service') < order.index('Controller')
    
    cycle = {'A': ['B'], 'B': ['A']}
    import pytest
    with pytest.raises(ValueError):
        dependency_inversion_container(cycle)
