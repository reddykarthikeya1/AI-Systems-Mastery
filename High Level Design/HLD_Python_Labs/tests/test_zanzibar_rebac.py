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


def test_nested_group_expansion():
    """Multi-tier nested groups: doc -> group:a#member -> group:b#member -> user:dave"""
    engine = ZanzibarEngine()
    engine.write_tuple(RelationTuple("doc", "secret_project", "viewer", "group:core#member"))
    engine.write_tuple(RelationTuple("group", "core", "member", "group:backend#member"))
    engine.write_tuple(RelationTuple("group", "backend", "member", "user:dave"))

    assert engine.check("user:dave", "viewer", "doc:secret_project") is True
    assert engine.check("user:stranger", "viewer", "doc:secret_project") is False


def test_delete_tuple_revocation():
    """Verify revoking tuple immediately removes access."""
    engine = ZanzibarEngine()
    t = RelationTuple("doc", "report_q3", "viewer", "user:grace")
    engine.write_tuple(t)
    assert engine.check("user:grace", "viewer", "doc:report_q3") is True

    # Revoke
    engine.delete_tuple(t)
    assert engine.check("user:grace", "viewer", "doc:report_q3") is False


def test_service_unavailability_raises_error():
    """Fail-closed: service unavailability must raise error."""
    engine = ZanzibarEngine()
    engine.write_tuple(RelationTuple("doc", "public_doc", "viewer", "user:anyone"))

    engine.is_available = False
    with pytest.raises(RuntimeError, match="service unavailable"):
        engine.check("user:anyone", "viewer", "doc:public_doc")

