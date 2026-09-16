"""Property and performance assertions for Distributed Web Crawler & Deduplication.

These complement the correctness tests in `test_web_crawler_frontier.py`. A correctness test says
the operation does the right thing; these say the *claim the module makes about
it* is true - and they fail when it stops being true.

    pytest -m perf -v          # just the performance assertions
    pytest -m "not slow" -q    # skip the long ones
"""

from __future__ import annotations

from web_crawler_frontier import (
    ContentDeduplicator,
    MercatorFrontier,
    RobotsTxtParser,
    SimHashEngine,
    URLCanonicalizer,
)


def test_canonicalisation_is_idempotent() -> None:
    """Canonicalising twice must not change the answer, or dedup is unreliable."""
    canon = URLCanonicalizer()
    for raw in (
        "HTTP://Example.COM:80/a/../b?z=1&a=2#frag",
        "http://example.com/b?a=2&z=1",
    ):
        once = canon.canonicalize(raw)
        assert canon.canonicalize(once) == once


def test_urls_differing_only_cosmetically_canonicalise_together() -> None:
    canon = URLCanonicalizer()
    a = canon.canonicalize("http://example.com/page#section")
    b = canon.canonicalize("http://example.com/page")
    assert a == b


def test_near_duplicate_content_is_detected() -> None:
    """URL comparison cannot catch this; SimHash is why the module exists."""
    dedup = ContentDeduplicator(max_hamming_distance=3)
    original = "the quick brown fox jumps over the lazy dog " * 12
    almost = "the quick brown fox jumps over the lazy dog " * 12 + "extra tail"

    dedup.add_document("doc1", original)

    # is_duplicate returns (is_dup, matched_doc_id, hamming_distance). Asserting
    # on the tuple itself would always pass - a non-empty tuple is truthy. That
    # is the exact defect this course's Module 08 diagnostic covers, so unpack.
    is_dup, matched, distance = dedup.is_duplicate(almost)
    assert is_dup, f"near-duplicate slipped through at hamming distance {distance}"
    assert matched == "doc1"


def test_genuinely_different_content_is_not_flagged() -> None:
    dedup = ContentDeduplicator(max_hamming_distance=3)
    dedup.add_document("doc1", "distributed systems consensus raft paxos " * 12)
    is_dup, _matched, distance = dedup.is_duplicate(
        "geospatial indexing quadtree geohash uber " * 12
    )
    assert not is_dup, f"unrelated text flagged as duplicate at distance {distance}"
    assert distance > 3, "unrelated documents should be far apart in SimHash space"


def test_simhash_distance_is_zero_for_identical_text() -> None:
    text = "identical content here " * 8
    a = SimHashEngine.compute_fingerprint(text)
    b = SimHashEngine.compute_fingerprint(text)
    assert SimHashEngine.hamming_distance(a, b) == 0


def test_robots_disallow_is_respected() -> None:
    """Politeness is a correctness requirement, not etiquette."""
    parser = RobotsTxtParser("User-agent: *\nDisallow: /private/\n", user_agent="*")
    assert not parser.is_allowed("/private/secret")
    assert parser.is_allowed("/public/page")


def test_a_spider_trap_is_recognised() -> None:
    canon = URLCanonicalizer()
    trap = "http://example.com/" + "a/" * 40
    assert canon.is_spider_trap(trap, max_depth=10, max_repeats=3)


def test_frontier_dedups_repeated_enqueues() -> None:
    """Without this a crawler loops forever between two mutually-linking pages."""
    frontier = MercatorFrontier()
    for _ in range(5):
        frontier.enqueue("http://example.com/page", priority=1)
    assert frontier.size() <= 1


def test_frontier_honours_per_host_politeness_delay() -> None:
    frontier = MercatorFrontier(default_politeness_delay=10.0)
    frontier.enqueue("http://example.com/a", priority=1)
    frontier.enqueue("http://example.com/b", priority=1)

    first = frontier.poll(current_time=1000.0)
    assert first is not None
    assert frontier.poll(current_time=1001.0) is None, "ignored the politeness delay"
    assert frontier.poll(current_time=1011.0) is not None
