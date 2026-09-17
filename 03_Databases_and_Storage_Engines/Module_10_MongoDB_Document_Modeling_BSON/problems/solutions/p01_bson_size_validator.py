"""Reference Solution — Problem 01: Bson Size Validator

Topic: 10 MongoDB Document Modeling BSON
"""

from __future__ import annotations


def bson_size_validator(doc: dict, max_bytes: int = 16 * 1024 * 1024) -> tuple[bool, int]:
    def calc_size(d: dict) -> int:
        total = 5  # 4 bytes int32 length + 1 byte null
        for k, v in d.items():
            total += 1 + len(k.encode('utf-8')) + 1  # type + cstring
            if isinstance(v, bool):
                total += 1
            elif isinstance(v, int):
                total += 8
            elif isinstance(v, float):
                total += 8
            elif isinstance(v, str):
                total += 4 + len(v.encode('utf-8')) + 1
            elif isinstance(v, dict):
                total += calc_size(v)
            else:
                total += 8
        return total
    sz = calc_size(doc)
    return (sz <= max_bytes, sz)
