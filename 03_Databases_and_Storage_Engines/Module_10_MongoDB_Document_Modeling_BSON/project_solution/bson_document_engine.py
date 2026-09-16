"""Module 10: MongoDB BSON Document & Schema Patterns Engine Reference Solution.

This is a pure-Python MODEL of MongoDB's BSON serialization format and document engine, built to make the
mechanism visible. It does not connect to MongoDB. For the real driver,
real queries and real operational behaviour, see `mongo_live.py`.

Implements:
1. BSON Document Encoder converting Python primitive types to binary wire bytes.
2. BSON Document Decoder parsing raw bytes back into Python dictionaries.
3. 12-byte chronologically sortable ObjectId generator.
4. Document Collection with schema validation rules and the Time-Series Bucket Pattern.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
import struct
import time
from typing import Any

# BSON Type Tags
BSON_DOUBLE = 0x01
BSON_STRING = 0x02
BSON_DOCUMENT = 0x03
BSON_BOOL = 0x08
BSON_INT32 = 0x10
BSON_INT64 = 0x12

_counter = 0


@dataclass(frozen=True)
class ObjectId:
    bytes_val: bytes

    @classmethod
    def generate(cls) -> ObjectId:
        """Generates a 12-byte BSON ObjectId (4B timestamp + 5B machine + 3B counter)."""
        global _counter
        ts = int(time.time())
        random_bytes = os.urandom(5)
        _counter = (_counter + 1) % 0xFFFFFF
        packed = struct.pack(">I 5s 3s", ts, random_bytes, _counter.to_bytes(3, "big"))
        return cls(bytes_val=packed)

    @property
    def timestamp(self) -> int:
        """Extracts 4-byte epoch timestamp from ObjectId header."""
        return struct.unpack(">I", self.bytes_val[:4])[0]

    def to_hex(self) -> str:
        return self.bytes_val.hex()


class BSONCodec:
    """Encodes and decodes subset of BSON binary wire protocol (int, float, string, dict)."""

    @classmethod
    def encode_element(cls, key: str, value: Any) -> bytes:
        key_bytes = key.encode("utf-8") + b"\x00"

        if isinstance(value, bool):
            val_bytes = b"\x01" if value else b"\x00"
            return bytes([BSON_BOOL]) + key_bytes + val_bytes

        elif isinstance(value, int):
            if -0x80000000 <= value <= 0x7FFFFFFF:
                return bytes([BSON_INT32]) + key_bytes + struct.pack("<i", value)
            else:
                return bytes([BSON_INT64]) + key_bytes + struct.pack("<q", value)

        elif isinstance(value, float):
            return bytes([BSON_DOUBLE]) + key_bytes + struct.pack("<d", value)

        elif isinstance(value, str):
            val_encoded = value.encode("utf-8") + b"\x00"
            length_prefix = struct.pack("<i", len(val_encoded))
            return bytes([BSON_STRING]) + key_bytes + length_prefix + val_encoded

        elif isinstance(value, dict):
            sub_doc_bytes = cls.encode_document(value)
            return bytes([BSON_DOCUMENT]) + key_bytes + sub_doc_bytes

        raise TypeError(f"Unsupported BSON type for value: {type(value)}")

    @classmethod
    def encode_document(cls, doc: dict[str, Any]) -> bytes:
        """Encodes Python dictionary to BSON wire bytes: [4B len] [elements...] [0x00]."""
        elements = bytearray()
        for k, v in doc.items():
            elements.extend(cls.encode_element(k, v))

        total_length = 4 + len(elements) + 1  # 4 bytes for length + elements + null terminator
        result = struct.pack("<i", total_length) + elements + b"\x00"
        return bytes(result)

    @classmethod
    def decode_document(cls, raw_bytes: bytes) -> dict[str, Any]:
        """Decodes BSON wire bytes back into Python dictionary."""
        if len(raw_bytes) < 5:
            raise ValueError("BSON document must be at least 5 bytes.")

        total_length = struct.unpack("<i", raw_bytes[:4])[0]
        if total_length != len(raw_bytes):
            raise ValueError(f"Header length mismatch: declared {total_length}, actual {len(raw_bytes)}")

        offset = 4
        result: dict[str, Any] = {}

        while offset < total_length - 1:
            type_tag = raw_bytes[offset]
            offset += 1

            # Read null-terminated key string
            null_pos = raw_bytes.find(b"\x00", offset)
            if null_pos == -1:
                raise ValueError("Malformed BSON: key is not null-terminated.")
            key = raw_bytes[offset:null_pos].decode("utf-8")
            offset = null_pos + 1

            # Parse value by type tag
            if type_tag == BSON_BOOL:
                val = bool(raw_bytes[offset])
                offset += 1
            elif type_tag == BSON_INT32:
                val = struct.unpack("<i", raw_bytes[offset : offset + 4])[0]
                offset += 4
            elif type_tag == BSON_INT64:
                val = struct.unpack("<q", raw_bytes[offset : offset + 8])[0]
                offset += 8
            elif type_tag == BSON_DOUBLE:
                val = struct.unpack("<d", raw_bytes[offset : offset + 8])[0]
                offset += 8
            elif type_tag == BSON_STRING:
                str_len = struct.unpack("<i", raw_bytes[offset : offset + 4])[0]
                offset += 4
                str_bytes = raw_bytes[offset : offset + str_len - 1]  # exclude null byte
                val = str_bytes.decode("utf-8")
                offset += str_len
            elif type_tag == BSON_DOCUMENT:
                sub_doc_len = struct.unpack("<i", raw_bytes[offset : offset + 4])[0]
                val = cls.decode_document(raw_bytes[offset : offset + sub_doc_len])
                offset += sub_doc_len
            else:
                raise ValueError(f"Unknown BSON type tag: {hex(type_tag)}")

            result[key] = val

        return result


class DocumentCollection:
    """Simulates a MongoDB collection with schema validation and Time-Series Bucketing."""

    def __init__(self, name: str, schema_validator: dict[str, type] | None = None) -> None:
        self.name = name
        self.schema_validator = schema_validator or {}
        self.documents: dict[str, bytes] = {}  # hex_id -> BSON bytes
        self._buckets: dict[str, dict[str, Any]] = {}  # "sensor_id:hour" -> bucket dict

    def insert_one(self, doc: dict[str, Any]) -> str:
        """Validates schema, assigns ObjectId if missing, encodes to BSON, and stores."""
        # Validate schema rules
        for field_name, expected_type in self.schema_validator.items():
            if field_name in doc and not isinstance(doc[field_name], expected_type):
                raise TypeError(f"Schema violation: field '{field_name}' must be {expected_type.__name__}")

        stored_doc = dict(doc)
        if "_id" not in stored_doc:
            doc_id = ObjectId.generate().to_hex()
            stored_doc["_id"] = doc_id
        else:
            doc_id = str(stored_doc["_id"])

        bson_bytes = BSONCodec.encode_document(stored_doc)
        self.documents[doc_id] = bson_bytes
        return doc_id

    def find_one(self, filter_criteria: dict[str, Any]) -> dict[str, Any] | None:
        """Finds first matching document by decoding stored BSON bytes."""
        for bson_bytes in self.documents.values():
            doc = BSONCodec.decode_document(bson_bytes)
            matches = all(doc.get(k) == v for k, v in filter_criteria.items())
            if matches:
                return doc
        return None

    def add_bucket_reading(self, sensor_id: str, hour: int, reading_sec: int, temperature: float) -> str:
        """Appends reading to an existing hourly bucket document, or initializes new bucket."""
        bucket_key = f"{sensor_id}:{hour}"
        if bucket_key not in self._buckets:
            self._buckets[bucket_key] = {
                "sensor_id": sensor_id,
                "hour": hour,
                "count": 0,
                "readings": {},
            }

        bucket = self._buckets[bucket_key]
        bucket["count"] += 1
        bucket["readings"][str(reading_sec)] = temperature

        # Save to document collection
        return self.insert_one({
            "bucket_id": bucket_key,
            "sensor_id": sensor_id,
            "hour": hour,
            "count": bucket["count"],
            "readings": bucket["readings"],
        })
