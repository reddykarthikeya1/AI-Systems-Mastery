"""Module 19: Distributed Web Crawler Frontier & SimHash Deduplication Engine.

Reference implementation of Mercator two-tier politeness frontier,
RFC-compliant robots.txt rule evaluator, URL canonicalization, and 64-bit SimHash
Locality-Sensitive Hashing (LSH) near-duplicate content detection.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import contextlib
import hashlib
import heapq
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

# ============================================================================
# 1. URL Canonicalization & Trap Detection
# ============================================================================

TRACKING_PARAMS: set[str] = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "ref", "fbclid", "gclid", "zanpid", "msclkid", "_ga", "mc_eid"
}


class URLCanonicalizer:
    """Canonicalizes raw discovered web URLs to prevent duplicate crawling."""

    @staticmethod
    def canonicalize(raw_url: str) -> str:
        """Normalizes URL scheme, host, port, path, and cleans query parameters."""
        raw_url = raw_url.strip()
        parsed = urlparse(raw_url)

        # Enforce HTTP/HTTPS scheme
        scheme = parsed.scheme.lower()
        if scheme not in ("http", "https"):
            raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

        # Lowercase hostname and remove default ports
        netloc = parsed.netloc.lower()
        if ":" in netloc:
            host, port = netloc.split(":", 1)
            if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
                netloc = host

        # Path normalization: normalize consecutive slashes, strip trailing slash if not root
        path = re.sub(r"/+", "/", parsed.path)
        if not path:
            path = "/"
        elif len(path) > 1 and path.endswith("/"):
            path = path[:-1]

        # Filter out tracking query parameters and sort remaining keys alphabetically
        query_pairs = parse_qsl(parsed.query, keep_blank_values=False)
        cleaned_pairs = [
            (k, v) for k, v in query_pairs if k.lower() not in TRACKING_PARAMS
        ]
        cleaned_pairs.sort(key=lambda x: (x[0], x[1]))
        cleaned_query = urlencode(cleaned_pairs)

        # Strip fragment (#section) entirely as crawler operates at document level
        return urlunparse((scheme, netloc, path, "", cleaned_query, ""))

    @staticmethod
    def is_spider_trap(url: str, max_depth: int = 6, max_repeats: int = 2) -> bool:
        """Detects recursive spider traps such as repeated directory loops or excessive depth."""
        parsed = urlparse(url)
        segments = [s for s in parsed.path.split("/") if s]

        # Exceeds maximum folder traversal depth
        if len(segments) > max_depth:
            return True

        # Check for repeating path segments (e.g., /dir/dir/dir)
        counts: dict[str, int] = defaultdict(int)
        for seg in segments:
            counts[seg] += 1
            if counts[seg] > max_repeats:
                return True

        return False


# ============================================================================
# 2. Robots.txt Compliance Evaluator
# ============================================================================

@dataclass
class RobotsRule:
    path_prefix: str
    allow: bool


class RobotsTxtParser:
    """Parses and evaluates robots.txt directives for web crawlers."""

    def __init__(self, raw_content: str, user_agent: str = "*") -> None:
        self.user_agent = user_agent.lower()
        self.rules: list[RobotsRule] = []
        self.crawl_delay_sec: float = 0.5
        self._parse(raw_content)

    def _parse(self, content: str) -> None:
        current_agents: list[str] = []
        is_target_agent = False

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ":" not in line:
                continue

            field, val = [part.strip() for part in line.split(":", 1)]
            field = field.lower()

            if field == "user-agent":
                agent = val.lower()
                current_agents.append(agent)
                is_target_agent = (agent == "*" or agent == self.user_agent)
            elif is_target_agent:
                if field == "disallow":
                    if val:
                        self.rules.append(RobotsRule(path_prefix=val, allow=False))
                    else:
                        # Empty Disallow means everything is allowed
                        self.rules.append(RobotsRule(path_prefix="/", allow=True))
                elif field == "allow":
                    if val:
                        self.rules.append(RobotsRule(path_prefix=val, allow=True))
                elif field == "crawl-delay":
                    with contextlib.suppress(ValueError):
                        self.crawl_delay_sec = max(0.1, float(val))

    def is_allowed(self, path: str) -> bool:
        """Determines if a URL path is crawlable according to longest prefix match."""
        if not path.startswith("/"):
            path = "/" + path

        best_match_len = -1
        allowed = True

        for rule in self.rules:
            prefix = rule.path_prefix
            if path.startswith(prefix):
                if len(prefix) > best_match_len:
                    best_match_len = len(prefix)
                    allowed = rule.allow
                elif len(prefix) == best_match_len and rule.allow:
                    # Allow takes precedence over Disallow on tie
                    allowed = True

        return allowed


# ============================================================================
# 3. 64-Bit SimHash Near-Duplicate Detection Engine
# ============================================================================

class SimHashEngine:
    """Computes 64-bit Locality Sensitive Hash fingerprints and measures Hamming distance."""

    BIT_LENGTH = 64

    @classmethod
    def compute_fingerprint(cls, text: str) -> int:
        """Generates a 64-bit integer fingerprint from document text."""
        # Simple tokenization: extract alphanumeric tokens
        tokens = re.findall(r"\b[a-zA-Z0-9_]{2,}\b", text.lower())
        if not tokens:
            return 0

        # Term frequency weighting
        tf: dict[str, int] = defaultdict(int)
        for token in tokens:
            tf[token] += 1

        vector = [0] * cls.BIT_LENGTH

        for token, weight in tf.items():
            # Generate deterministic 64-bit integer hash using MD5
            token_hash = int(hashlib.md5(token.encode("utf-8")).hexdigest()[:16], 16)
            for i in range(cls.BIT_LENGTH):
                bit = (token_hash >> i) & 1
                if bit == 1:
                    vector[i] += weight
                else:
                    vector[i] -= weight

        fingerprint = 0
        for i in range(cls.BIT_LENGTH):
            if vector[i] > 0:
                fingerprint |= (1 << i)

        return fingerprint

    @staticmethod
    def hamming_distance(fp1: int, fp2: int) -> int:
        """Calculates the number of differing bits between two 64-bit fingerprints."""
        xor_result = fp1 ^ fp2
        return bin(xor_result).count("1")


class ContentDeduplicator:
    """In-memory index that flags near-duplicate documents within a Hamming distance threshold."""

    def __init__(self, max_hamming_distance: int = 3) -> None:
        self.max_hamming_distance = max_hamming_distance
        self.fingerprints: list[tuple[str, int]] = []  # List of (doc_id, fingerprint)

    def is_duplicate(self, text: str) -> tuple[bool, str | None, int]:
        """Checks if document is a near-duplicate.

        Returns: (is_dup, matching_doc_id, min_distance)
        """
        new_fp = SimHashEngine.compute_fingerprint(text)
        min_dist = float("inf")
        matched_id: str | None = None

        for doc_id, existing_fp in self.fingerprints:
            dist = SimHashEngine.hamming_distance(new_fp, existing_fp)
            if dist < min_dist:
                min_dist = dist
                matched_id = doc_id
            if dist <= self.max_hamming_distance:
                return True, doc_id, dist

        return False, matched_id, int(min_dist) if min_dist != float("inf") else -1

    def add_document(self, doc_id: str, text: str) -> int:
        """Indexes a document fingerprint and returns its computed fingerprint."""
        fp = SimHashEngine.compute_fingerprint(text)
        self.fingerprints.append((doc_id, fp))
        return fp


# ============================================================================
# 4. Mercator Two-Tier URL Frontier
# ============================================================================

@dataclass(order=True)
class HostReadyEntry:
    ready_time: float
    host: str = field(compare=False)


class MercatorFrontier:
    """Reference Mercator URL Frontier decoupling priority from host politeness."""

    def __init__(self, default_politeness_delay: float = 1.0) -> None:
        self.default_politeness_delay = default_politeness_delay

        # Priority queues: priority 0 (highest) to N
        self.priority_queues: dict[int, deque[str]] = defaultdict(deque)

        # Host queues: FIFO queue of URLs per hostname
        self.host_queues: dict[str, deque[str]] = defaultdict(deque)

        # Host heap: Min-heap tracking (next_ready_timestamp, host)
        self.host_ready_heap: list[HostReadyEntry] = []
        self.active_hosts_in_heap: set[str] = set()

        # Tracking seen URLs to prevent duplicate enqueue
        self.seen_urls: set[str] = set()

        # Per-host politeness delay overrides (e.g. from robots.txt)
        self.host_delays: dict[str, float] = {}

    def set_host_delay(self, host: str, delay_sec: float) -> None:
        """Sets custom politeness crawl delay for a specific host."""
        self.host_delays[host] = delay_sec

    def enqueue(self, raw_url: str, priority: int = 1) -> bool:
        """Normalizes and enqueues a URL. Returns True if accepted, False if seen or trap."""
        try:
            canonical_url = URLCanonicalizer.canonicalize(raw_url)
        except Exception:
            return False

        if URLCanonicalizer.is_spider_trap(canonical_url):
            return False

        if canonical_url in self.seen_urls:
            return False

        self.seen_urls.add(canonical_url)

        # Place into priority front-queue
        self.priority_queues[priority].append(canonical_url)
        self._flush_front_to_back()
        return True

    def _flush_front_to_back(self) -> None:
        """Transfers URLs from priority queues into their respective host back queues."""
        for prio in sorted(self.priority_queues.keys()):
            q = self.priority_queues[prio]
            while q:
                url = q.popleft()
                parsed = urlparse(url)
                host = parsed.netloc
                self.host_queues[host].append(url)

                # If host is not currently scheduled in the ready heap, schedule it immediately
                if host not in self.active_hosts_in_heap:
                    heapq.heappush(self.host_ready_heap, HostReadyEntry(ready_time=0.0, host=host))
                    self.active_hosts_in_heap.add(host)

    def poll(self, current_time: float) -> str | None:
        """Fetches the next eligible URL respecting politeness intervals."""
        if not self.host_ready_heap:
            return None

        # Check if the earliest host is ready to crawl
        top = self.host_ready_heap[0]
        if top.ready_time > current_time:
            return None  # All candidate hosts are currently waiting for politeness cooldown

        entry = heapq.heappop(self.host_ready_heap)
        host = entry.host
        self.active_hosts_in_heap.remove(host)

        queue = self.host_queues.get(host)
        if not queue:
            return None

        url = queue.popleft()
        delay = self.host_delays.get(host, self.default_politeness_delay)
        next_ready = current_time + delay

        # If more URLs remain for this host, re-insert into heap with updated ready_time
        if queue:
            heapq.heappush(self.host_ready_heap, HostReadyEntry(ready_time=next_ready, host=host))
            self.active_hosts_in_heap.add(host)

        return url

    def size(self) -> int:
        """Returns total remaining URLs waiting across all host queues."""
        return sum(len(q) for q in self.host_queues.values())
