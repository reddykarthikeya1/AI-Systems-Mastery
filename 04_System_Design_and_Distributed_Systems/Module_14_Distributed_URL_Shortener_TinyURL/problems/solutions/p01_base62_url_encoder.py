"""Reference Solution — Problem 01: Base62 Url Encoder

Topic: 14 Distributed URL Shortener TinyURL
"""

from __future__ import annotations


def base62_url_encoder(num: int) -> str:
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return "0"
    res = []
    while num > 0:
        res.append(chars[num % 62])
        num //= 62
    return "".join(reversed(res))
