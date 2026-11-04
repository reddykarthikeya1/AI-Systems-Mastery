"""Tests for Google Zanzibar ReBAC Authorization Graph Engine (Chapter 24)."""
import pytest
from ch24_zanzibar_rebac.zanzibar_rebac import (
    ZanzibarEngine,
    RelationTuple,
)


def test_direct_relation():
    engine = ZanzibarEngine()
    engine.write_tuple(
        RelationTuple("doc", "architecture", "viewer", "user:charlie")
    )

    assert engine.check("user:charlie", "viewer", "doc:architecture") is True
    assert engine.check("user:eve", "viewer", "doc:architecture") is False


def test_rewrite_inheritance():
    """Default rules:

    owner -> editor -> viewer
    An owner must inherit editor and viewer permissions automatically.
    """
    engine = ZanzibarEngine()
    engine.write_tuple(
        RelationTuple("doc", "financials", "owner", "user:alice")
    )

    assert engine.check("user:alice", "owner", "doc:financials") is True
    assert engine.check("user:alice", "editor", "doc:financials") is True
    assert engine.check("user:alice", "viewer", "doc:financials") is True


def test_subject_set_group_expansion():
    """Group membership expansion:

    doc:design#viewer -> group:engineers#member
    group:engineers#member -> user:bob
    """
    engine = ZanzibarEngine()
    # Document shared with group
    engine.write_tuple(
        RelationTuple("doc", "design", "viewer", "group:engineers#member")
    )
    # Bob is member of group
    engine.write_tuple(
        RelationTuple("group", "engineers", "member", "user:bob")
    )

    assert engine.check("user:bob", "viewer", "doc:design") is True
    assert engine.check("user:mallory", "viewer", "doc:design") is False


def test_cycle_detection_safety():
    """Cycles in group memberships must not cause recursion or infinite loop."""
    engine = ZanzibarEngine()
    engine.write_tuple(RelationTuple("group", "A", "member", "group:B#member"))
    engine.write_tuple(RelationTuple("group", "B", "member", "group:A#member"))

    # Check non-existent user should terminate gracefully and return False
    res = engine.check("user:ghost", "member", "group:A")
    assert res is False


def test_list_authorized_objects():
    engine = ZanzibarEngine()
    engine.write_tuple(RelationTuple("doc", "doc_A", "owner", "user:alice"))
    engine.write_tuple(RelationTuple("doc", "doc_B", "viewer", "user:alice"))
    engine.write_tuple(RelationTuple("doc", "doc_C", "owner", "user:david"))

    authorized = engine.list_authorized_objects("user:alice", "viewer", "doc")
    assert authorized == ["doc:doc_A", "doc:doc_B"]
