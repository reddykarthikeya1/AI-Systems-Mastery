"""Example 3: a complete, dependency-free hybrid RAG retrieval pipeline with evaluation.

chunking -> BM25 (lexical) + hashed character n-gram vectors (typo-tolerant "dense" stand-in)
-> Reciprocal Rank Fusion -> recall@k on labelled queries.

Swap `embed()` for a real embedding model in production; everything else stays the same.
Run: python ex03_hybrid_rag.py
"""
import math
import re
import zlib
from collections import Counter

DOCS = {
    "d1": "Error ECONNRESET means the peer closed the TCP connection abruptly. Retry with exponential backoff.",
    "d2": "The refund policy allows returns within 30 days of delivery with the original receipt.",
    "d3": "To rotate the signing key run the kms-rotate job; the previous key stays valid for 24 hours.",
    "d4": "Kubernetes liveness probes restart a stuck container while readiness probes remove it from the load balancer.",
    "d5": "PostgreSQL MVCC keeps old row versions so readers never block writers; VACUUM reclaims dead tuples.",
    "d6": "Our SKU-48213 charger supports 65W USB-C power delivery and ships with a two meter cable.",
    "d7": "Use idempotency keys on payment requests so a retried charge is not applied twice.",
    "d8": "The HNSW index trades memory for fast approximate nearest neighbour search over embeddings.",
    "d9": "Raft elects a leader using randomized election timeouts and replicates a log to followers.",
    "d10": "Rate limiting with a token bucket allows short bursts while enforcing an average request rate.",
}

# (query, relevant doc). Identifier and error-code queries favour lexical match; typo queries favour n-grams.
QUERIES = [
    # identifiers / error codes: exact token match (BM25 strong, collision-blurred n-grams weak)
    ("ECONNRESET", "d1"), ("SKU-48213", "d6"), ("kms-rotate", "d3"), ("VACUUM", "d5"),
    # misspelled queries with no exact token overlap (BM25 returns nothing, n-grams still match)
    ("refnd polcy retrns", "d2"), ("kubernetis livness prob", "d4"), ("idempotncy payemnt", "d7"),
    ("approximte neighbour embedings", "d8"), ("raft electon timout", "d9"), ("toekn bukcet", "d10"),
]


def tokens(text: str) -> list:
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())


def chunk(text: str, size: int = 40, overlap: int = 8) -> list:
    words = text.split()
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(1, len(words) - overlap), step)]


class BM25:
    def __init__(self, corpus: dict, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.ids = list(corpus)
        self.tf = {i: Counter(tokens(t)) for i, t in corpus.items()}
        self.len = {i: sum(c.values()) for i, c in self.tf.items()}
        self.avg = sum(self.len.values()) / len(self.len)
        df = Counter(w for c in self.tf.values() for w in c)
        n = len(self.ids)
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}

    def rank(self, query: str) -> list:
        scores = {}
        for i in self.ids:
            s = 0.0
            for w in tokens(query):
                f = self.tf[i].get(w, 0)
                if f:
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
            scores[i] = s
        return [i for i, s in sorted(scores.items(), key=lambda kv: -kv[1]) if s > 0]


DIM = 48   # deliberately small: hash collisions make this "dense" side blur exact identifiers


def embed(text: str) -> list:
    """Hashed character 3-grams: robust to typos. A stand-in for a learned embedding."""
    vec = [0.0] * DIM
    for w in tokens(text):
        padded = f"^{w}$"
        for j in range(len(padded) - 2):
            vec[zlib.crc32(padded[j:j + 3].encode()) % DIM] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def dense_rank(corpus: dict, query: str) -> list:
    q = embed(query)
    scored = {i: sum(a * b for a, b in zip(q, embed(t))) for i, t in corpus.items()}
    return [i for i, _ in sorted(scored.items(), key=lambda kv: -kv[1])]


def rrf(rankings: list, k: int = 60) -> list:
    score = Counter()
    for r in rankings:
        for pos, doc in enumerate(r, start=1):
            score[doc] += 1.0 / (k + pos)
    return [d for d, _ in score.most_common()]


def recall_at(ranker, k: int) -> float:
    hits = sum(1 for q, rel in QUERIES if rel in ranker(q)[:k])
    return hits / len(QUERIES)


def evaluate(k: int = 1) -> dict:
    bm = BM25(DOCS)
    lex = lambda q: bm.rank(q)
    den = lambda q: dense_rank(DOCS, q)
    hyb = lambda q: rrf([lex(q), den(q)])
    return {"bm25": recall_at(lex, k), "dense": recall_at(den, k), "hybrid": recall_at(hyb, k)}


if __name__ == "__main__":
    assert len(chunk(" ".join(["w"] * 100), 40, 8)) == 3          # chunking sanity: 100 words, stride 32
    r = evaluate(k=1)
    print("recall@1:", r)
    assert r["hybrid"] >= max(r["bm25"], r["dense"]), r             # fusion should not be worse than the best single method
    assert r["hybrid"] > min(r["bm25"], r["dense"]), r              # and it must beat the weaker one on this set
    print("OK")
