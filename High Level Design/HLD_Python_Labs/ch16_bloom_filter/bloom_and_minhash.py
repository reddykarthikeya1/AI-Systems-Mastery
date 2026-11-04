"""Probabilistic Data Structures: Bloom Filter vs. MinHash & LSH.

CRITICAL ARCHITECTURAL DISTINCTION:
===================================
1. Bloom Filter:
   - Purpose: Probabilistic SET MEMBERSHIP testing ("Is element x in set S?").
   - Guarantees: ZERO false negatives. Small, bounded false positive probability p.
   - Mechanism: A bit array of size m and k independent hash functions.
   - Use Cases: Checking if username exists, caching negative disk lookups, web crawlers.

2. MinHash & Locality-Sensitive Hashing (LSH):
   - Purpose: SET SIMILARITY estimation ("What is the Jaccard similarity |A & B| / |A | B|?").
   - Guarantees: Unbiased estimator of Jaccard similarity. Sub-quadratic nearest neighbor search.
   - Mechanism: k random hash permutations over shingled tokens, partitioned into b bands of r rows.
   - Use Cases: Near-duplicate document detection, deduplication in LLM pre-training datasets, plagiarism check.
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
    if n <= 0 or p <= 0 or p >= 1.0:
        raise ValueError("Capacity n must be > 0 and error rate p must be in (0, 1)")
    m = - (n * math.log(p)) / (math.log(2) ** 2)
    k = (m / n) * math.log(2)
    return max(1, int(math.ceil(m))), max(1, int(round(k)))


class BloomFilter:
    """Probabilistic Set Membership Filter.

    Zero false negatives; bounded false positive rate p ~= (1 - e^(-kn/m))^k.
    """

    def __init__(self, size_m: int, hash_count_k: int) -> None:
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


class MinHash:
    """MinHash Signature for Jaccard Similarity Estimation.

    Estimates: J(A, B) = |A & B| / |A | B|
    By property: P(min_hash(A) == min_hash(B)) = J(A, B)
    """

    _PRIME = (1 << 61) - 1  # Mersenne prime for hashing

    def __init__(self, num_hashes: int = 128, seed: int = 42) -> None:
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
        words = text.lower().split()
        if len(words) < n_gram:
            return {" ".join(words)}
        return {" ".join(words[i : i + n_gram]) for i in range(len(words) - n_gram + 1)}

    def update(self, tokens: Set[str]) -> None:
        """Update the signature with a set of shingle tokens."""
        for token in tokens:
            # 64-bit token hash
            raw_hash = int(hashlib.md5(token.encode("utf-8")).hexdigest()[:16], 16)
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


class LSHIndex:
    """Locality-Sensitive Hashing (LSH) Banding Index for Sub-Quadratic Candidate Search.

    Partitions signature of length K into B bands of R rows each (K = B * R).
    Two items become candidate matches if they collide in AT LEAST ONE band.
    Probability of collision: P = 1 - (1 - s^r)^b where s is Jaccard similarity.
    """

    def __init__(self, bands: int = 16, rows_per_band: int = 8) -> None:
        self.bands = bands
        self.rows_per_band = rows_per_band
        self.num_hashes = bands * rows_per_band
        # (band_idx, bucket_hash) -> set of doc_ids
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
            bucket_hash = hash(band_tuple)
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
            bucket_hash = hash(band_tuple)
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
