#!/usr/bin/env python3
"""Module 14: In-Process Architectural Simulation Model: Globally Distributed URL Shortener Service.

Implements:
- Base62 bijective encoding/decoding ([0-9a-zA-Z])
- Key Generation Service (KGS) with batched token pre-allocation
- Cache-Aside redirection tier with LRU/TTL expiration
- Click telemetry and access counter analytics
"""

from __future__ import annotations

import string
import threading
import time
from dataclasses import dataclass

BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase  # 0-9, a-z, A-Z (length 62)
BASE62_MAP = {c: i for i, c in enumerate(BASE62_CHARS)}


class Base62Encoder:
    """Bijective base-10 integer to Base-62 alphanumeric string conversion."""

    @staticmethod
    def encode(num: int, min_length: int = 7) -> str:
        if num < 0:
            raise ValueError("Cannot encode negative integer")
        if num == 0:
            return BASE62_CHARS[0] * min_length

        digits = []
        while num > 0:
            rem = num % 62
            digits.append(BASE62_CHARS[rem])
            num //= 62

        encoded = "".join(reversed(digits))
        # Pad with leading '0' characters up to min_length
        if len(encoded) < min_length:
            encoded = (BASE62_CHARS[0] * (min_length - len(encoded))) + encoded
        return encoded

    @staticmethod
    def decode(s: str) -> int:
        num = 0
        for char in s:
            if char not in BASE62_MAP:
                raise ValueError(f"Invalid Base62 character: {char}")
            num = num * 62 + BASE62_MAP[char]
        return num


class KeyGenerationService:
    """Simulates a distributed KGS that dispenses pre-generated unique integer blocks."""

    def __init__(self, start_id: int = 100_000_000, block_size: int = 1000) -> None:
        self._current_id = start_id
        self._block_size = block_size
        self._lock = threading.Lock()

    def allocate_block(self) -> tuple[int, int]:
        """Allocates an exclusive range [start, end) of IDs to a web worker server."""
        with self._lock:
            start = self._current_id
            end = start + self._block_size
            self._current_id = end
            return start, end


@dataclass
class URLEntry:
    short_token: str
    original_url: str
    created_at: float
    expires_at: float | None = None
    click_count: int = 0

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return time.monotonic() > self.expires_at


class URLShortenerService:
    """Production URL Shortener service with KGS, cache tier, and analytics."""

    def __init__(self, kgs: KeyGenerationService, base_url: str = "https://tiny.url/") -> None:
        self.kgs = kgs
        self.base_url = base_url.rstrip("/") + "/"
        self._db: dict[str, URLEntry] = {}
        self._cache: dict[str, str] = {}  # short_token -> original_url
        self._curr_id = 0
        self._end_id = 0
        self._lock = threading.Lock()

    def _next_token_id(self) -> int:
        """Returns next sequential ID, allocating a new KGS block when exhausted."""
        with self._lock:
            if self._curr_id >= self._end_id:
                self._curr_id, self._end_id = self.kgs.allocate_block()
            token_id = self._curr_id
            self._curr_id += 1
            return token_id

    def shorten_url(self, original_url: str, ttl_seconds: float | None = None) -> str:
        if not original_url.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")

        token_id = self._next_token_id()
        short_token = Base62Encoder.encode(token_id)

        now = time.monotonic()
        expires_at = (now + ttl_seconds) if ttl_seconds else None

        entry = URLEntry(
            short_token=short_token,
            original_url=original_url,
            created_at=now,
            expires_at=expires_at,
        )

        with self._lock:
            self._db[short_token] = entry
            self._cache[short_token] = original_url

        return f"{self.base_url}{short_token}"

    def resolve_url(self, short_url_or_token: str) -> str:
        """Resolves short token back to original URL with click tracking."""
        token = short_url_or_token.split("/")[-1]

        # 1. Check L1 cache
        with self._lock:
            cached_url = self._cache.get(token)
            entry = self._db.get(token)
            if cached_url and entry and not entry.is_expired:
                entry.click_count += 1
                return cached_url

        if entry is None or entry.is_expired:
            with self._lock:
                self._cache.pop(token, None)
                self._db.pop(token, None)
            raise KeyError(f"404 Not Found: Short token '{token}' does not exist or expired")

        # 2. Increment analytics
        with self._lock:
            entry.click_count += 1

        return entry.original_url

    def get_analytics(self, short_token: str) -> dict[str, int | str]:
        token = short_token.split("/")[-1]
        with self._lock:
            entry = self._db.get(token)
            if entry is None or entry.is_expired:
                raise KeyError(f"Short token '{token}' not found")
            return {
                "token": entry.short_token,
                "original_url": entry.original_url,
                "clicks": entry.click_count,
            }
