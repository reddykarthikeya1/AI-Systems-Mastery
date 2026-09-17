"""Unit tests for Globally Distributed URL Shortener Service."""

from __future__ import annotations

import concurrent.futures
import time

import pytest
from url_shortener_service import (
    Base62Encoder,
    KeyGenerationService,
    URLShortenerService,
)


def test_base62_bijective_symmetry() -> None:
    test_numbers = [0, 1, 61, 62, 125, 999_999, 100_000_000, 3_500_000_000_000]

    for num in test_numbers:
        encoded = Base62Encoder.encode(num, min_length=7)
        assert len(encoded) >= 7
        decoded = Base62Encoder.decode(encoded)
        assert decoded == num


def test_url_shorten_and_resolve_lifecycle() -> None:
    kgs = KeyGenerationService(start_id=100_000)
    service = URLShortenerService(kgs)

    original = "https://www.google.com/search?q=system+design+mastery"
    short_url = service.shorten_url(original)

    assert short_url.startswith("https://tiny.url/")
    token = short_url.split("/")[-1]
    assert len(token) == 7

    # Resolve URL
    resolved = service.resolve_url(short_url)
    assert resolved == original

    # Analytics check
    stats = service.get_analytics(token)
    assert stats["clicks"] == 1

    # Second click
    service.resolve_url(short_url)
    stats2 = service.get_analytics(token)
    assert stats2["clicks"] == 2


def test_ttl_expiration_behavior() -> None:
    kgs = KeyGenerationService()
    service = URLShortenerService(kgs)

    # 0.2 second TTL
    short_url = service.shorten_url("https://fast-expire.com", ttl_seconds=0.2)
    assert service.resolve_url(short_url) == "https://fast-expire.com"

    time.sleep(0.3)  # wait for expiration

    with pytest.raises(KeyError, match="does not exist or expired"):
        service.resolve_url(short_url)


def test_concurrent_url_shortening_uniqueness() -> None:
    kgs = KeyGenerationService(start_id=500_000, block_size=100)
    service = URLShortenerService(kgs)
    total_requests = 1000

    def shorten_task(i: int) -> str:
        return service.shorten_url(f"https://domain-{i}.com/page")

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(shorten_task, range(total_requests)))

    # Invariant: Every generated short URL must be strictly unique
    assert len(results) == total_requests
    assert len(set(results)) == total_requests
