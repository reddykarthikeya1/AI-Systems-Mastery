"""Automated pytest test suite for Module 04 PostgreSQL JSONB & TOAST Engine."""

from datetime import datetime
import pytest
from jsonb_document_store import JSONBDocumentStore, RangeExclusionIndex, TimeRange


@pytest.fixture
def doc_store() -> JSONBDocumentStore:
    store = JSONBDocumentStore(toast_threshold_bytes=500, toast_chunk_size=200)
    store.insert("doc_1", {"name": "Laptop", "category": "Electronics", "price": 1200, "tags": ["tech", "portable"]})
    store.insert("doc_2", {"name": "Mouse", "category": "Electronics", "price": 25, "tags": ["tech", "accessory"]})
    store.insert("doc_3", {"name": "Chair", "category": "Furniture", "price": 150, "tags": ["home", "office"]})
    return store


def test_insert_and_retrieve_inline_document(doc_store: JSONBDocumentStore) -> None:
    doc = doc_store.get("doc_1")
    assert doc["name"] == "Laptop"
    assert doc["price"] == 1200
    assert doc_store.is_toasted("doc_1") is False


def test_toast_chunking_and_transparent_decompression(doc_store: JSONBDocumentStore) -> None:
    # Insert large document exceeding 500 byte threshold
    large_payload = {
        "title": "PostgreSQL Architecture Guide",
        "content": "PostgreSQL internals, MVCC, shared_buffers, WAL writer, checkpointer, and TOAST. " * 30,
        "author": "Database Specialist",
    }
    doc_store.insert("doc_large", large_payload)

    # Verify TOAST activation
    assert doc_store.is_toasted("doc_large") is True

    # Retrieve and verify exact lossless decompression
    recovered = doc_store.get("doc_large")
    assert recovered["title"] == "PostgreSQL Architecture Guide"
    assert recovered["content"] == large_payload["content"]
    assert recovered["author"] == "Database Specialist"


def test_gin_index_containment_operator(doc_store: JSONBDocumentStore) -> None:
    # Simulating: SELECT * FROM docs WHERE data @> '{"category": "Electronics"}'
    results = doc_store.contains({"category": "Electronics"})
    assert results == ["doc_1", "doc_2"]

    # Simulating multiple field containment
    results_multiple = doc_store.contains({"category": "Electronics", "price": 25})
    assert results_multiple == ["doc_2"]

    # Non-existent property
    results_none = doc_store.contains({"category": "Automotive"})
    assert results_none == []


def test_gin_index_tag_array_containment(doc_store: JSONBDocumentStore) -> None:
    results_tech = doc_store.contains({"tags": ["tech"]})
    assert "doc_1" in results_tech
    assert "doc_2" in results_tech
    assert "doc_3" not in results_tech


def test_get_non_existent_document_raises_key_error(doc_store: JSONBDocumentStore) -> None:
    with pytest.raises(KeyError, match="Document with id 'ghost' not found"):
        doc_store.get("ghost")


def test_time_range_validation() -> None:
    t1 = datetime(2026, 6, 1, 10, 0)
    t2 = datetime(2026, 6, 1, 12, 0)

    # Valid range
    r = TimeRange(start=t1, end=t2)
    assert r.start == t1 and r.end == t2

    # Inverted range raises ValueError
    with pytest.raises(ValueError, match="start .* must precede end"):
        TimeRange(start=t2, end=t1)


def test_time_range_overlap_logic() -> None:
    r1 = TimeRange(datetime(2026, 6, 1, 10, 0), datetime(2026, 6, 1, 12, 0))
    # Overlapping interval (11:00 to 13:00)
    r2 = TimeRange(datetime(2026, 6, 1, 11, 0), datetime(2026, 6, 1, 13, 0))
    # Non-overlapping adjacent interval (12:00 to 14:00)
    r3 = TimeRange(datetime(2026, 6, 1, 12, 0), datetime(2026, 6, 1, 14, 0))
    # Completely disjoint interval (15:00 to 16:00)
    r4 = TimeRange(datetime(2026, 6, 1, 15, 0), datetime(2026, 6, 1, 16, 0))

    assert r1.overlaps(r2) is True
    assert r2.overlaps(r1) is True
    assert r1.overlaps(r3) is False  # Half-open interval [start, end)
    assert r1.overlaps(r4) is False


def test_range_exclusion_constraint_enforcement() -> None:
    index = RangeExclusionIndex()
    room_101 = "room_101"

    # Booking 1: 10:00 - 12:00
    index.add_reservation(room_101, "booking_1", TimeRange(datetime(2026, 6, 1, 10, 0), datetime(2026, 6, 1, 12, 0)))

    # Booking 2 on different room succeeds even at same time
    index.add_reservation("room_102", "booking_2", TimeRange(datetime(2026, 6, 1, 10, 0), datetime(2026, 6, 1, 12, 0)))

    # Booking 3 overlapping Booking 1 on room_101 fails with exclusion violation
    with pytest.raises(ValueError, match="Exclusion constraint violation"):
        index.add_reservation(room_101, "booking_3", TimeRange(datetime(2026, 6, 1, 11, 30), datetime(2026, 6, 1, 13, 0)))

    # Booking 4 strictly adjacent to Booking 1 succeeds
    index.add_reservation(room_101, "booking_4", TimeRange(datetime(2026, 6, 1, 12, 0), datetime(2026, 6, 1, 14, 0)))
    assert len(index.get_reservations(room_101)) == 2
