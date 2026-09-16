"""Automated pytest test suite for Module 10 MongoDB BSON & Schema Engine."""

import time
import pytest
from bson_document_engine import BSONCodec, DocumentCollection, ObjectId


def test_object_id_generation_and_timestamp() -> None:
    now = int(time.time())
    oid = ObjectId.generate()
    assert len(oid.bytes_val) == 12
    # Timestamp extracted should be within 2 seconds of current time
    assert abs(oid.timestamp - now) <= 2

    # Two sequentially generated IDs must be distinct
    oid2 = ObjectId.generate()
    assert oid.to_hex() != oid2.to_hex()


def test_bson_codec_primitive_types() -> None:
    doc = {
        "active": True,
        "age": 28,  # int32
        "large_number": 5_000_000_000,  # int64
        "rating": 4.85,  # double
        "name": "Karthikeya",  # string
    }

    encoded = BSONCodec.encode_document(doc)
    assert len(encoded) > 5

    decoded = BSONCodec.decode_document(encoded)
    assert decoded["active"] is True
    assert decoded["age"] == 28
    assert decoded["large_number"] == 5_000_000_000
    assert pytest.approx(decoded["rating"], 0.01) == 4.85
    assert decoded["name"] == "Karthikeya"


def test_bson_codec_nested_document() -> None:
    doc = {
        "user": "Alice",
        "profile": {
            "city": "London",
            "score": 99.5,
        },
    }

    encoded = BSONCodec.encode_document(doc)
    decoded = BSONCodec.decode_document(encoded)
    assert decoded["user"] == "Alice"
    assert decoded["profile"]["city"] == "London"
    assert pytest.approx(decoded["profile"]["score"], 0.01) == 99.5


def test_collection_schema_validation() -> None:
    collection = DocumentCollection(
        name="users",
        schema_validator={"name": str, "age": int, "balance": float},
    )

    # Valid document
    doc_id = collection.insert_one({"name": "Bob", "age": 30, "balance": 150.75})
    assert doc_id is not None

    # Invalid document (age passed as string instead of int)
    with pytest.raises(TypeError, match="field 'age' must be int"):
        collection.insert_one({"name": "Charlie", "age": "thirty", "balance": 50.0})


def test_collection_find_one(test_doc: dict = None) -> None:
    collection = DocumentCollection("products")
    collection.insert_one({"sku": "LAPTOP-01", "brand": "ThinkPad", "price": 1200})
    collection.insert_one({"sku": "PHONE-01", "brand": "Pixel", "price": 800})

    found = collection.find_one({"sku": "PHONE-01"})
    assert found is not None
    assert found["brand"] == "Pixel"
    assert found["price"] == 800

    not_found = collection.find_one({"sku": "NON_EXISTENT"})
    assert not_found is None


def test_time_series_bucket_pattern() -> None:
    collection = DocumentCollection("sensor_buckets")

    # Add 3 readings for Hour 14
    collection.add_bucket_reading(sensor_id="SN-01", hour=14, reading_sec=0, temperature=21.4)
    collection.add_bucket_reading(sensor_id="SN-01", hour=14, reading_sec=1, temperature=21.6)
    doc_id = collection.add_bucket_reading(sensor_id="SN-01", hour=14, reading_sec=2, temperature=21.5)

    bucket = collection.find_one({"_id": doc_id})
    assert bucket is not None
    assert bucket["sensor_id"] == "SN-01"
    assert bucket["hour"] == 14
    assert bucket["count"] == 3
    assert len(bucket["readings"]) == 3
