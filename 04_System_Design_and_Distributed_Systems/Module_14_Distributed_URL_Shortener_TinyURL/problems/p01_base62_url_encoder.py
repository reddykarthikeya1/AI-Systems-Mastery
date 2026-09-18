"""Problem 01 — Base62 Url Encoder

Topic: 14 Distributed URL Shortener TinyURL
Target: Production-grade implementation

Encode 64-bit integer ID to Base62 short URL token and decode back.

Example:
    >>> base62_url_encoder(0)
    '0'
    >>> base62_url_encoder(62)
    '10'

Hints:
    Hint 1: This is the same idea as converting a number to hex or binary,
        just with a 62-character alphabet instead of 16 or 2 symbols.
    Hint 2: Repeatedly take `num % 62` and `num //= 62`, collecting each
        remainder as a character from the charset, then reverse the
        collected characters at the end.
    Hint 3: `0` is a special case that must explicitly return `'0'` --
        the divmod loop body never executes for it and would otherwise
        produce an empty string; the charset order matters too, digits
        '0'-'9' before lowercase 'a'-'z' before uppercase 'A'-'Z', since
        swapping that order silently breaks any encode/decode round-trip.
"""

from __future__ import annotations


def base62_url_encoder(num: int) -> str:
    """Convert non-negative integer to Base62 string using charset '0-9a-zA-Z'.
    0 encodes to '0'.
    """
    raise NotImplementedError("Implement base62_url_encoder")
