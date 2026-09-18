"""Tests for Supervisor Routing Consensus."""
from __future__ import annotations

import pytest
from p01_supervisor_routing_consensus import supervisor_routing_consensus


def test_supervisor_routing_consensus():
    assert supervisor_routing_consensus("Optimize SQL query") == "DatabaseAgent"
    assert supervisor_routing_consensus("Write python script") == "CoderAgent"
    assert supervisor_routing_consensus("Run test suite") == "TesterAgent"
    assert supervisor_routing_consensus("Hello there") == "GeneralAgent"
