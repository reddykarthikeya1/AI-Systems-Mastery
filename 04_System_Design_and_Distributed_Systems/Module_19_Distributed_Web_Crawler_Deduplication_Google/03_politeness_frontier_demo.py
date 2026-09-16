"""Module 19: Standalone Interactive Demo - Web Crawler Frontier & SimHash Deduplication."""

from project_solution.web_crawler_frontier import (
    ContentDeduplicator,
    MercatorFrontier,
    RobotsTxtParser,
    SimHashEngine,
    URLCanonicalizer,
)


def main() -> None:
    print("=" * 80)
    print(" MODULE 19: DISTRIBUTED WEB CRAWLER & SIMHASH DEDUPLICATION")
    print("=" * 80)

    # ---------------------------------------------------------
    # Step 1: URL Canonicalization & Trap Detection
    # ---------------------------------------------------------
    print("\n--- 1. URL Canonicalization & Spider Trap Detection ---")
    dirty_urls = [
        "HTTPS://Blog.Example.Com:443/posts/tech/?utm_source=twitter&ref=abc&b=2&a=1#section3",
        "http://example.com:80/dir1//dir2/index.html?utm_campaign=spring",
        "https://example.com/a/b/a/b/a/b/trap.html",
    ]

    for raw in dirty_urls:
        trap = URLCanonicalizer.is_spider_trap(raw)
        try:
            canon = URLCanonicalizer.canonicalize(raw)
            print(f" Raw:  {raw}")
            print(f"   -> Canonical: {canon} | Trap Detected: {trap}")
        except Exception as e:
            print(f" Raw:  {raw} -> Error: {e}")

    # ---------------------------------------------------------
    # Step 2: Robots.txt Parsing & Rule Enforcement
    # ---------------------------------------------------------
    print("\n--- 2. Robots.txt Compliance Evaluation ---")
    robots_sample = """
    User-agent: *
    Disallow: /admin
    Disallow: /checkout
    Allow: /admin/public
    Crawl-delay: 2.0
    """
    parser = RobotsTxtParser(robots_sample, user_agent="Googlebot")
    test_paths = ["/", "/news/article1", "/admin/settings", "/admin/public/faq", "/checkout/pay"]
    print(f" Parsed Crawl-Delay: {parser.crawl_delay_sec}s")
    for path in test_paths:
        allowed = parser.is_allowed(path)
        status = "ALLOWED" if allowed else "BLOCKED (Disallow)"
        print(f" Path: {path:<25} -> {status}")

    # ---------------------------------------------------------
    # Step 3: 64-Bit SimHash Near-Duplicate Detection
    # ---------------------------------------------------------
    print("\n--- 3. 64-Bit SimHash Near-Duplicate Content Detection ---")
    doc_original = (
        "Distributed systems achieve fault tolerance and high availability via consensus protocols like Raft and Paxos. "
        "High availability clusters require redundant nodes, heartbeats, write-ahead logs, snapshotting, and leader election."
    )
    doc_near_dup = doc_original.replace("redundant nodes", "replicated nodes")
    doc_different = (
        "Delicious authentic Italian pizza dough requires high hydration flour, active yeast, "
        "extra virgin olive oil, and baking in a 900 degree wood-fired stone pizza oven."
    )

    fp1 = SimHashEngine.compute_fingerprint(doc_original)
    fp2 = SimHashEngine.compute_fingerprint(doc_near_dup)
    fp3 = SimHashEngine.compute_fingerprint(doc_different)

    dist_near = SimHashEngine.hamming_distance(fp1, fp2)
    dist_diff = SimHashEngine.hamming_distance(fp1, fp3)

    print(f" Doc 1 Fingerprint: {bin(fp1)[2:].zfill(64)}")
    print(f" Doc 2 Fingerprint: {bin(fp2)[2:].zfill(64)}")
    print(f" Doc 3 Fingerprint: {bin(fp3)[2:].zfill(64)}")
    print(f"\n Hamming Distance (Doc 1 vs Doc 2 [Slight rephrase]): {dist_near} bits (Near-dup: {dist_near <= 3})")
    print(f" Hamming Distance (Doc 1 vs Doc 3 [Pizza recipe]):     {dist_diff} bits (Near-dup: {dist_diff <= 3})")

    dedup = ContentDeduplicator(max_hamming_distance=3)
    dedup.add_document("doc-raft-1", doc_original)
    is_dup, match_id, d = dedup.is_duplicate(doc_near_dup)
    print(f"\n Deduplication Index Result for Doc 2: Duplicate={is_dup}, MatchedDoc='{match_id}', Distance={d}")

    # ---------------------------------------------------------
    # Step 4: Mercator Two-Tier Politeness Frontier Simulation
    # ---------------------------------------------------------
    print("\n--- 4. Mercator URL Frontier Crawl Simulation ---")
    frontier = MercatorFrontier(default_politeness_delay=0.5)
    frontier.set_host_delay("slow-api.org", delay_sec=1.5)

    urls_to_crawl = [
        ("https://alpha.com/page1", 1),
        ("https://alpha.com/page2", 1),
        ("https://alpha.com/page3", 1),
        ("https://beta.com/article1", 0),  # Higher priority
        ("https://slow-api.org/data1", 1),
        ("https://slow-api.org/data2", 1),
    ]

    for u, p in urls_to_crawl:
        frontier.enqueue(u, priority=p)

    print(f" Initial Frontier Size: {frontier.size()} URLs queued.")

    # Step through simulated discrete clock
    simulated_clock = 0.0
    crawled_count = 0

    while frontier.size() > 0 or frontier.host_ready_heap:
        url = frontier.poll(simulated_clock)
        if url:
            crawled_count += 1
            print(f" [T={simulated_clock:04.1f}s] Crawled -> {url}")
        else:
            # Advance clock to next earliest ready host
            if frontier.host_ready_heap:
                simulated_clock = frontier.host_ready_heap[0].ready_time
            else:
                break
        simulated_clock += 0.1  # Fetch duration tick

    print(f"\n Crawl cycle completed! Total documents crawled: {crawled_count}")
    print("=" * 80)


if __name__ == "__main__":
    main()
