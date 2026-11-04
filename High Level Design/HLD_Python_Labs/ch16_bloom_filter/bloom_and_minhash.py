"""Probabilistic Data Structures: Bloom Filter, Counting Bloom Filter, MinHash & LSH.

CRITICAL ARCHITECTURAL DISTINCTIONS:
===================================
1. Bloom Filter (Set Membership):
   - Purpose: Fast, space-efficient testing of whether an element belongs to a set.
   - Guarantees: ZERO false negatives. Bounded false positive rate p ~= (1 - e^(-kn/m))^k.
   - Deletions: CANNOT delete elements (clearing a bit could delete other co-mapped elements).
   - Use Cases: Checking if username exists, caching negative disk lookups, web crawlers.

2. Counting Bloom Filter (Set Membership with Deletions):
   - Purpose: Set membership testing that supports dynamic removal of previously added items.
   - Mechanism: Replaces each bit in the array with an n-bit counter (e.g. 8-bit integer).
   - Invariant: Counters increment on add and decrement on remove (protected against underflow).

3. MinHash (Set Similarity Estimation):
   - Purpose: Estimating Jaccard similarity J(A, B) = |A & B| / |A | B| between high-dimensional sets.
   - Guarantees: P(min_hash(A) == min_hash(B)) = J(A, B). Unbiased similarity estimator.
   - Mechanism: k random hash permutations over shingled tokens.

4. Locality-Sensitive Hashing / LSH Index (Candidate Bucketing):
   - Purpose: Sub-quadratic approximate nearest-neighbor candidate pair retrieval.
   - Mechanism: Partitions K signature rows into B bands of R rows. Deterministic band hashing
     places colliding documents into candidate buckets without pairwise O(N^2) comparison.
   - Deterministic Hashing: Eliminates Python's built-in `hash()` which varies per process.
"""

from __future__ import annotations
import hashlib
import math
import random
from typing import Dict, List, Optional, Set, Tuple


def calculate_optimal_bloom_params(n: int, p: float) -> Tuple[int, int]:
    """Calculates optimal bit array size m and number of hash functions k.

    Formulas:
        m = - (n * ln(p)) / (ln(2)^2)
        k = (m / n) * ln(2)
    """
    if n <= 0:
        raise ValueError(f"Capacity n must be > 0, got {n}")
    if p <= 0 or p >= 1.0:
        raise ValueError(f"False positive rate p must be in (0, 1), got {p}")

    m = - (n * math.log(p)) / (math.log(2) ** 2)
    k = (m / n) * math.log(2)
    return max(1, int(math.ceil(m))), max(1, int(round(k)))


class BloomFilter:
    """Probabilistic Set Membership Filter (Zero False Negatives, No Deletions)."""

    def __init__(self, size_m: int, hash_count_k: int) -> None:
        if size_m <= 0:
            raise ValueError("size_m must be > 0")
        if hash_count_k <= 0:
            raise ValueError("hash_count_k must be > 0")

        self.m = size_m
        self.k = hash_count_k
        self.bit_array = bytearray(math.ceil(size_m / 8))
        self.items_count = 0

    @classmethod
    def from_capacity(cls, expected_items: int, false_positive_rate: float = 0.01) -> BloomFilter:
        m, k = calculate_optimal_bloom_params(expected_items, false_positive_rate)
        return cls(size_m=m, hash_count_k=k)

    def _get_hashes(self, item: str) -> List[int]:
        """Kirsch-Mitzenmacher optimization using two 64-bit hash digests to produce k hashes:

        g_i(x) = (h1(x) + i * h2(x)) mod m
        """
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        h1 = int.from_bytes(digest[:8], "little")
        h2 = int.from_bytes(digest[8:16], "little") | 1  # ensure odd

        hashes = []
        for i in range(self.k):
            hashes.append((h1 + i * h2) % self.m)
        return hashes

    def add(self, item: str) -> None:
        """Add an item to the Bloom filter."""
        for bit_index in self._get_hashes(item):
            byte_idx = bit_index // 8
            bit_offset = bit_index % 8
            self.bit_array[byte_idx] |= 1 << bit_offset
        self.items_count += 1

    def contains(self, item: str) -> bool:
        """Test set membership.

        Returns:
            False: Item is GUARANTEED not in the set (zero false negatives).
            True:  Item is likely in the set (subject to false positive rate).
        """
        for bit_index in self._get_hashes(item):
            byte_idx = bit_index // 8
            bit_offset = bit_index % 8
            if not (self.bit_array[byte_idx] & (1 << bit_offset)):
                return False
        return True

    def estimated_false_positive_rate(self) -> float:
        """Theoretical false positive rate given current item count:

        p ~= (1 - exp(-k * n / m))^k
        """
        if self.m == 0:
            return 1.0
        exponent = - (self.k * self.items_count) / self.m
        return math.pow(1.0 - math.exp(exponent), self.k)


class CountingBloomFilter:
    """Counting Bloom Filter supporting item removal/deletion via counter array."""

    def __init__(self, size_m: int, hash_count_k: int, counter_max: int = 255) -> None:
        if size_m <= 0:
            raise ValueError("size_m must be > 0")
        if hash_count_k <= 0:
            raise ValueError("hash_count_k must be > 0")
        if counter_max <= 0:
            raise ValueError("counter_max must be > 0")

        self.m = size_m
        self.k = hash_count_k
        self.counter_max = counter_max
        self.counters = [0] * size_m
        self.items_count = 0

    @classmethod
    def from_capacity(
        cls, expected_items: int, false_positive_rate: float = 0.01, counter_max: int = 255
    ) -> CountingBloomFilter:
        m, k = calculate_optimal_bloom_params(expected_items, false_positive_rate)
        return cls(size_m=m, hash_count_k=k, counter_max=counter_max)

    def _get_hashes(self, item: str) -> List[int]:
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        h1 = int.from_bytes(digest[:8], "little")
        h2 = int.from_bytes(digest[8:16], "little") | 1

        hashes = []
        for i in range(self.k):
            hashes.append((h1 + i * h2) % self.m)
        return hashes

    def add(self, item: str) -> None:
        """Increment counters for the item."""
        for idx in self._get_hashes(item):
            if self.counters[idx] < self.counter_max:
                self.counters[idx] += 1
        self.items_count += 1

    def contains(self, item: str) -> bool:
        """Check if all counters for the item are > 0."""
        for idx in self._get_hashes(item):
            if self.counters[idx] == 0:
                return False
        return True

    def remove(self, item: str) -> bool:
        """Decrement counters for the item if present.

        Returns:
            True if item was present and removed, False otherwise.
        """
        if not self.contains(item):
            return False

        for idx in self._get_hashes(item):
            if self.counters[idx] > 0:
                self.counters[idx] -= 1
        self.items_count = max(0, self.items_count - 1)
        return True


class MinHash:
    """MinHash Signature for Jaccard Similarity Estimation.

    Estimates: J(A, B) = |A & B| / |A | B|
    By property: P(min_hash(A) == min_hash(B)) = J(A, B)
    """

    _PRIME = (1 << 61) - 1  # Mersenne prime for hashing

    def __init__(self, num_hashes: int = 128, seed: int = 42) -> None:
        if num_hashes <= 0:
            raise ValueError("num_hashes must be > 0")

        self.num_hashes = num_hashes
        self.seed = seed
        self._a, self._b = self._generate_hash_coefficients(num_hashes, seed)
        self.signature: List[int] = [self._PRIME] * num_hashes

    @staticmethod
    def _generate_hash_coefficients(num_hashes: int, seed: int) -> Tuple[List[int], List[int]]:
        rng = random.Random(seed)
        a_coeffs = [rng.randint(1, MinHash._PRIME - 1) for _ in range(num_hashes)]
        b_coeffs = [rng.randint(0, MinHash._PRIME - 1) for _ in range(num_hashes)]
        return a_coeffs, b_coeffs

    @staticmethod
    def shingle_text(text: str, n_gram: int = 3) -> Set[str]:
        """Generate n-gram word or character shingles."""
        if n_gram <= 0:
            raise ValueError("n_gram must be > 0")
        words = text.lower().split()
        if not words:
            return set()
        if len(words) < n_gram:
            return {" ".join(words)}
        return {" ".join(words[i : i + n_gram]) for i in range(len(words) - n_gram + 1)}

    def update(self, tokens: Set[str]) -> None:
        """Update the signature with a set of shingle tokens."""
        for token in tokens:
            # Deterministic 64-bit token hash
            raw_hash = int(hashlib.sha256(token.encode("utf-8")).hexdigest()[:16], 16)
            for i in range(self.num_hashes):
                h_val = (self._a[i] * raw_hash + self._b[i]) % self._PRIME
                if h_val < self.signature[i]:
                    self.signature[i] = h_val

    def jaccard_similarity(self, other: MinHash) -> float:
        """Estimate Jaccard similarity as fraction of matching signature slots."""
        if self.num_hashes != other.num_hashes:
            raise ValueError("Signatures must have identical length")
        matches = sum(1 for i in range(self.num_hashes) if self.signature[i] == other.signature[i])
        return matches / float(self.num_hashes)


def _deterministic_band_hash(band_idx: int, band_tuple: Tuple[int, ...]) -> int:
    """Produces a deterministic 64-bit integer hash for LSH bucket indexing.

    Never uses Python's built-in hash() which has randomized per-process seeds.
    """
    raw = band_idx.to_bytes(4, "big") + b"".join(x.to_bytes(8, "big", signed=False) for x in band_tuple)
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")


class LSHIndex:
    """Locality-Sensitive Hashing (LSH) Banding Index for Sub-Quadratic Candidate Search.

    Partitions signature of length K into B bands of R rows each (K = B * R).
    Two items become candidate matches if they collide in AT LEAST ONE band.
    Probability of collision: P = 1 - (1 - s^r)^b where s is Jaccard similarity.
    """

    def __init__(self, bands: int = 16, rows_per_band: int = 8) -> None:
        if bands <= 0:
            raise ValueError("bands must be > 0")
        if rows_per_band <= 0:
            raise ValueError("rows_per_band must be > 0")

        self.bands = bands
        self.rows_per_band = rows_per_band
        self.num_hashes = bands * rows_per_band
        # (band_idx, deterministic_bucket_hash) -> set of doc_ids
        self.buckets: Dict[Tuple[int, int], Set[str]] = {}
        self.doc_signatures: Dict[str, MinHash] = {}

    def insert(self, doc_id: str, minhash: MinHash) -> None:
        """Index a document MinHash into the LSH bands."""
        if minhash.num_hashes != self.num_hashes:
            raise ValueError(
                f"MinHash length {minhash.num_hashes} must match bands*rows={self.num_hashes}"
            )
        self.doc_signatures[doc_id] = minhash

        for band_idx in range(self.bands):
            start = band_idx * self.rows_per_band
            end = start + self.rows_per_band
            band_tuple = tuple(minhash.signature[start:end])
            bucket_hash = _deterministic_band_hash(band_idx, band_tuple)
            bucket_key = (band_idx, bucket_hash)

            if bucket_key not in self.buckets:
                self.buckets[bucket_key] = set()
            self.buckets[bucket_key].add(doc_id)

    def query_candidates(self, minhash: MinHash) -> Set[str]:
        """Find all document IDs that collide in at least one band."""
        candidates: Set[str] = set()
        for band_idx in range(self.bands):
            start = band_idx * self.rows_per_band
            end = start + self.rows_per_band
            band_tuple = tuple(minhash.signature[start:end])
            bucket_hash = _deterministic_band_hash(band_idx, band_tuple)
            bucket_key = (band_idx, bucket_hash)

            if bucket_key in self.buckets:
                candidates.update(self.buckets[bucket_key])
        return candidates

    def query_similar(
        self, minhash: MinHash, threshold: float = 0.7
    ) -> List[Tuple[str, float]]:
        """Retrieve candidate matches and compute estimated Jaccard similarity."""
        candidates = self.query_candidates(minhash)
        results: List[Tuple[str, float]] = []
        for doc_id in candidates:
            other_sig = self.doc_signatures[doc_id]
            sim = minhash.jaccard_similarity(other_sig)
            if sim >= threshold:
                results.append((doc_id, sim))
        results.sort(key=lambda x: x[1], reverse=True)
        return results
