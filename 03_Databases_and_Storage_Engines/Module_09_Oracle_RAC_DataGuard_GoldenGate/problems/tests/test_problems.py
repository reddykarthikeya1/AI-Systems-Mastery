"""Tests for Two Phase Commit Coordinator."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_two_phase_commit_coordinator import two_phase_commit_coordinator
except ImportError:
    from p01_two_phase_commit_coordinator import two_phase_commit_coordinator


def test_two_phase_commit_coordinator():
    nodes = ['nodeA', 'nodeB', 'nodeC']
    assert two_phase_commit_coordinator(nodes, {'nodeA': True, 'nodeB': True, 'nodeC': True}) == 'COMMIT'
    assert two_phase_commit_coordinator(nodes, {'nodeA': True, 'nodeB': False, 'nodeC': True}) == 'ABORT'
    assert two_phase_commit_coordinator(nodes, {'nodeA': True, 'nodeB': True}) == 'ABORT'
