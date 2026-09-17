"""Problem 01 — Base62 Url Encoder

Topic: 14 Distributed URL Shortener TinyURL
Target: Production-grade implementation

Encode 64-bit integer ID to Base62 short URL token and decode back.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def base62_url_encoder(num: int) -> str:
    """Convert non-negative integer to Base62 string using charset '0-9a-zA-Z'.
    0 encodes to '0'.
    """
    raise NotImplementedError("Implement base62_url_encoder")
