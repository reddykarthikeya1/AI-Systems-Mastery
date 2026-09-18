"""Tests for Entity Relation Subgraph Extract."""
from __future__ import annotations

import pytest
from p01_entity_relation_subgraph_extract import entity_relation_subgraph_extract


def test_entity_relation_subgraph_extract():
    triplets = [
        ("Python", "designed_by", "Guido"),
        ("Guido", "worked_at", "Google"),
        ("Java", "designed_by", "Gosling")
    ]
    sub = entity_relation_subgraph_extract(triplets, "Guido")
    assert len(sub) == 2
    assert ("Python", "designed_by", "Guido") in sub
    assert ("Guido", "worked_at", "Google") in sub
