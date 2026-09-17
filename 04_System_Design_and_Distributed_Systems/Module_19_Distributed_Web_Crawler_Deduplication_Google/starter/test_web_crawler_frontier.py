"""Unit and integration test suite for Module 19: Web Crawler & SimHash Deduplication."""

import pytest
from web_crawler_frontier import (
    ContentDeduplicator,
    MercatorFrontier,
    RobotsTxtParser,
    SimHashEngine,
    URLCanonicalizer,
)


def test_url_canonicalization_and_normalization() -> None:
    raw = "HTTPS://Example.COM:443/products//phones/?utm_source=fb&z=1&a=2#specs"
    canonical = URLCanonicalizer.canonicalize(raw)
    assert canonical == "https://example.com/products/phones?a=2&z=1"

    # Default port removal for HTTP
    assert URLCanonicalizer.canonicalize("http://example.com:80/about/") == "http://example.com/about"

    # Invalid scheme throws ValueError
    with pytest.raises(ValueError):
        URLCanonicalizer.canonicalize("ftp://example.com/files")


def test_spider_trap_detection() -> None:
    # Excessive path depth
    deep_url = "https://example.com/a/b/c/d/e/f/g/h"
    assert URLCanonicalizer.is_spider_trap(deep_url, max_depth=5) is True

    # Repeated directory loop
    loop_url = "https://example.com/category/books/category/books/category/books"
    assert URLCanonicalizer.is_spider_trap(loop_url, max_repeats=2) is True

    # Valid normal URL
    valid_url = "https://example.com/blog/2026/09/architecture-guide"
    assert URLCanonicalizer.is_spider_trap(valid_url) is False


def test_robots_txt_parser() -> None:
    robots_content = """
    User-agent: *
    Disallow: /private/
    Allow: /private/public-preview
    Crawl-delay: 1.5
    """
    parser = RobotsTxtParser(robots_content)
    assert parser.crawl_delay_sec == 1.5
    assert parser.is_allowed("/index.html") is True
    assert parser.is_allowed("/private/secret") is False
    assert parser.is_allowed("/private/public-preview") is True


def test_simhash_fingerprint_and_deduplication() -> None:
    # SimHash is designed for full-length documents where small variations (footers, minor edits)
    # produce Hamming distances <= 3, whereas orthogonal documents produce ~30 bits (half of 64).
    core_text = (
        "Apache Kafka is a distributed event streaming platform used by thousands of companies "
        "for high-performance data pipelines, streaming analytics, data integration, and mission-critical "
        "applications. Kafka provides publish and subscribe streams of records, similar to a message queue "
        "or enterprise messaging system. It stores streams of records accurately in a fault-tolerant durable way "
        "and processes streams of records as they occur."
    )
    # Near-duplicate: identical article with slight editorial paraphrase (e.g. syndicated rewrite)
    t1 = core_text
    t2 = core_text.replace("enterprise messaging system", "corporate messaging system")
    # Completely distinct document: cooking recipe
    t3 = (
        "Classic Neapolitan pizza dough requires high-protein flour, active dry yeast, sea salt, "
        "and lukewarm water. Ferment for twenty-four hours at room temperature, stretch by hand, "
        "top with San Marzano tomatoes and fresh mozzarella, then bake at 900 degrees in a wood-fired oven."
    )

    fp1 = SimHashEngine.compute_fingerprint(t1)
    fp2 = SimHashEngine.compute_fingerprint(t2)
    fp3 = SimHashEngine.compute_fingerprint(t3)

    assert fp1 != 0
    assert fp2 != 0
    assert fp3 != 0

    dist_near = SimHashEngine.hamming_distance(fp1, fp2)
    dist_diff = SimHashEngine.hamming_distance(fp1, fp3)

    # Near duplicates must have very small Hamming distance (<= 3)
    assert dist_near <= 3
    # Distinct topics should have high Hamming distance (> 15)
    assert dist_diff > 15

    # Content Deduplicator Index
    index = ContentDeduplicator(max_hamming_distance=3)
    index.add_document("doc-kafka-original", t1)

    is_dup, match_id, dist = index.is_duplicate(t2)
    assert is_dup is True
    assert match_id == "doc-kafka-original"
    assert dist <= 3

    is_dup3, _, _ = index.is_duplicate(t3)
    assert is_dup3 is False


def test_mercator_frontier_politeness_and_priority() -> None:
    frontier = MercatorFrontier(default_politeness_delay=1.0)

    # Enqueue multiple URLs for the same host
    assert frontier.enqueue("https://site-a.com/page1", priority=1) is True
    assert frontier.enqueue("https://site-a.com/page2", priority=1) is True
    assert frontier.enqueue("https://site-b.com/page1", priority=0) is True

    # Duplicate URLs should be rejected
    assert frontier.enqueue("https://site-a.com/page1", priority=1) is False

    assert frontier.size() == 3

    # At t=0.0, both site-a and site-b are ready
    u1 = frontier.poll(current_time=0.0)
    assert u1 is not None

    # Immediate next poll at t=0.0: should pick the other host since site-a or site-b is now on 1.0s cooldown
    u2 = frontier.poll(current_time=0.0)
    assert u2 is not None
    assert {u1, u2} == {"https://site-b.com/page1", "https://site-a.com/page1"}

    # Attempting to poll at t=0.5s: remaining URL is site-a/page2, but site-a cooldown is ready at t=1.0s
    assert frontier.poll(current_time=0.5) is None

    # Polling at t=1.0s: site-a is now eligible
    u3 = frontier.poll(current_time=1.0)
    assert u3 == "https://site-a.com/page2"
    assert frontier.size() == 0
