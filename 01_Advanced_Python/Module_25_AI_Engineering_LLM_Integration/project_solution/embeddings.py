#!/usr/bin/env python3
"""Module 25 - Embeddings: three backends, and one of them is a trap.

An embedding must place *semantically similar* text close together in vector
space. That property is the entire foundation of RAG. If it does not hold, the
retrieval step returns noise and no amount of prompt engineering rescues it.

This file ships three backends so you can measure the difference yourself:

+---------------------------+----------------+---------------------------------+
| Backend                   | Semantic?      | Use for                         |
+===========================+================+=================================+
| ``HashEmbedder``          | **NO - never** | Teaching what NOT to do         |
| ``TfidfSvdEmbedder``      | Yes (lexical/  | Default here: real, offline,    |
|                           | distributional)| deterministic, no downloads     |
| ``SentenceTransformer...``| Yes (learned)  | Production; needs a model file  |
+---------------------------+----------------+---------------------------------+

Why ``HashEmbedder`` exists
---------------------------
An earlier version of this project used it *as the real embedder*::

    h = hashlib.sha256(f"{text}:{i}".encode()).hexdigest()

A cryptographic hash is engineered so that similar inputs produce **maximally
dissimilar** outputs - that is its design goal (the avalanche property). Using
one as an embedding gives you a pipeline that runs, produces plausible-looking
cosine scores, and retrieves essentially at random.

It is kept here, clearly labelled, because ``test_hash_embedder_cannot_do_semantics``
*proves* it fails while the real embedder succeeds. Seeing that contrast is
worth more than being told.
"""

from __future__ import annotations

import hashlib
import math
import re
from abc import ABC, abstractmethod
from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

# ---------------------------------------------------------------------------
# Vector maths (numpy, not hand-rolled Python loops)
# ---------------------------------------------------------------------------


def cosine_similarity(u: NDArray[np.float64], v: NDArray[np.float64]) -> float:
    """Cosine of the angle between two vectors, in [-1, 1].

    cos(theta) = (u . v) / (||u|| ||v||)

    Why cosine and not Euclidean distance? Cosine ignores magnitude and compares
    *direction* only. A one-sentence document and a ten-page document about the
    same topic point the same way but have very different lengths.
    """
    nu = float(np.linalg.norm(u))
    nv = float(np.linalg.norm(v))
    if nu == 0.0 or nv == 0.0:
        return 0.0
    return float(np.dot(u, v) / (nu * nv))


def cosine_similarity_matrix(
    query: NDArray[np.float64], matrix: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Cosine similarity of one query against every row of `matrix` at once.

    This is the vectorised form: one BLAS call instead of a Python loop over
    documents. At 100k chunks that is the difference between 20 ms and 8 s.
    """
    if matrix.size == 0:
        return np.empty(0, dtype=np.float64)
    qn = float(np.linalg.norm(query))
    if qn == 0.0:
        return np.zeros(matrix.shape[0], dtype=np.float64)
    row_norms = np.linalg.norm(matrix, axis=1)
    row_norms[row_norms == 0.0] = 1.0  # avoid divide-by-zero on empty rows
    return (matrix @ query) / (row_norms * qn)


# ---------------------------------------------------------------------------
# Backend interface
# ---------------------------------------------------------------------------


class Embedder(ABC):
    """Common interface for every embedding backend."""

    name: str = "abstract"
    dimensions: int = 0

    def fit(self, corpus: Sequence[str]) -> Embedder:
        """Learn any corpus statistics needed. Pre-trained backends no-op here."""
        return self

    @abstractmethod
    def encode_one(self, text: str) -> NDArray[np.float64]:
        """Embed a single string."""

    def encode(self, texts: Sequence[str]) -> NDArray[np.float64]:
        """Embed a batch, returning shape (len(texts), dimensions)."""
        if not texts:
            return np.empty((0, self.dimensions), dtype=np.float64)
        return np.vstack([self.encode_one(t) for t in texts])


# ---------------------------------------------------------------------------
# 1. THE TRAP - a hash is not an embedding
# ---------------------------------------------------------------------------


class HashEmbedder(Embedder):
    """❌ **NOT A REAL EMBEDDER.** Kept only as a demonstrable negative example.

    SHA-256 is designed so that flipping one input bit changes ~half the output
    bits. Semantic similarity is therefore *impossible* by construction:
    "cat" and "cats" are as far apart as "cat" and "thermodynamics".

    Never use this for retrieval. See ``test_hash_embedder_cannot_do_semantics``.
    """

    name = "hash-BROKEN"

    def __init__(self, dimensions: int = 64) -> None:
        self.dimensions = dimensions

    def encode_one(self, text: str) -> NDArray[np.float64]:
        vec = np.empty(self.dimensions, dtype=np.float64)
        for i in range(self.dimensions):
            digest = hashlib.sha256(f"{text}:{i}".encode()).hexdigest()
            vec[i] = (int(digest[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec


# ---------------------------------------------------------------------------
# 2. THE DEFAULT - real distributional semantics, offline
# ---------------------------------------------------------------------------


class TfidfSvdEmbedder(Embedder):
    """✅ Latent Semantic Analysis: TF-IDF followed by truncated SVD.

    Two steps, each doing real work:

    1. **TF-IDF** turns each document into a sparse term-weight vector. Terms
       that are frequent *here* but rare *across the corpus* score highest, so
       "vacuum" outweighs "the".
    2. **Truncated SVD** projects that sparse space down to `dimensions` dense
       axes. This is the step that creates *semantics*: words that co-occur in
       similar contexts collapse onto the same latent axis, so a query using
       "refund" can match a document that says "money back".

    This is a genuine embedding - it satisfies the similarity property, needs no
    network access, and is fully deterministic. Its limit is that it only knows
    what is in the corpus you fit it on; it cannot generalise beyond that the
    way a pre-trained neural model can.

    Requires ``fit(corpus)`` before ``encode()``.
    """

    name = "tfidf-svd"

    def __init__(self, dimensions: int = 128, random_state: int = 42) -> None:
        self.dimensions = dimensions
        self.random_state = random_state
        self._pipeline: object | None = None
        self._fitted = False

    def fit(self, corpus: Sequence[str]) -> TfidfSvdEmbedder:
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import Normalizer

        if not corpus:
            raise ValueError("cannot fit an embedder on an empty corpus")

        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            sublinear_tf=True,      # damp runaway term counts
            ngram_range=(1, 2),     # unigrams + bigrams ("data base" ~ "database")
            min_df=1,
        )
        sparse = vectorizer.fit_transform(corpus)

        # SVD cannot request more components than the sparse rank allows.
        n_components = min(self.dimensions, max(1, min(sparse.shape) - 1))
        svd = TruncatedSVD(n_components=n_components, random_state=self.random_state)

        # Normalizer makes every output unit-length, so a dot product IS cosine.
        self._pipeline = make_pipeline(vectorizer, svd, Normalizer(copy=False))
        self._pipeline.fit(corpus)  # type: ignore[attr-defined]
        self.dimensions = n_components
        self._fitted = True
        return self

    def encode_one(self, text: str) -> NDArray[np.float64]:
        return self.encode([text])[0]

    def encode(self, texts: Sequence[str]) -> NDArray[np.float64]:
        if not self._fitted or self._pipeline is None:
            raise RuntimeError(
                "TfidfSvdEmbedder.fit(corpus) must be called before encode(). "
                "LSA learns its axes from the corpus - unlike a pre-trained model."
            )
        if not texts:
            return np.empty((0, self.dimensions), dtype=np.float64)
        return np.asarray(
            self._pipeline.transform(list(texts)), dtype=np.float64  # type: ignore[attr-defined]
        )


# ---------------------------------------------------------------------------
# 3. PRODUCTION - a pre-trained neural encoder, when available
# ---------------------------------------------------------------------------


class SentenceTransformerEmbedder(Embedder):
    """✅ A real pre-trained transformer encoder (optional dependency).

    ``all-MiniLM-L6-v2`` is 384-dimensional, ~80 MB, runs on CPU, and is the
    standard baseline for production RAG. Unlike LSA it generalises to text it
    has never seen, because the semantics live in the pre-trained weights rather
    than in your corpus.

    Install::

        pip install sentence-transformers
    """

    name = "sentence-transformer"

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self._model: object | None = None
        self.dimensions = 384

    @staticmethod
    def is_available() -> bool:
        import importlib.util

        return importlib.util.find_spec("sentence_transformers") is not None

    def fit(self, corpus: Sequence[str]) -> SentenceTransformerEmbedder:
        return self  # pre-trained: nothing to learn

    def _load(self) -> object:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            self.dimensions = int(self._model.get_sentence_embedding_dimension())  # type: ignore
        return self._model

    def encode_one(self, text: str) -> NDArray[np.float64]:
        return self.encode([text])[0]

    def encode(self, texts: Sequence[str]) -> NDArray[np.float64]:
        model = self._load()
        arr = model.encode(list(texts), normalize_embeddings=True)  # type: ignore[attr-defined]
        return np.asarray(arr, dtype=np.float64)


# ---------------------------------------------------------------------------
# Backend selection
# ---------------------------------------------------------------------------


def load_embedder(prefer: str = "auto", dimensions: int = 128) -> Embedder:
    """Return the best available *real* embedder.

    ``prefer``: "auto" | "tfidf" | "transformer" | "hash"

    Note that "hash" must be requested explicitly and by name. There is no code
    path in which a broken embedder is selected silently - which is exactly the
    bug this module used to contain.
    """
    if prefer == "hash":
        return HashEmbedder(dimensions=dimensions)
    if prefer in {"auto", "transformer"} and SentenceTransformerEmbedder.is_available():
        return SentenceTransformerEmbedder()
    if prefer == "transformer":
        raise RuntimeError("sentence-transformers is not installed")
    return TfidfSvdEmbedder(dimensions=dimensions)


# ---------------------------------------------------------------------------
# Chunking - the step before embedding, and where most RAG quality is lost
# ---------------------------------------------------------------------------

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def chunk_text(text: str, chunk_size: int = 320, overlap_ratio: float = 0.15) -> list[str]:
    """Split text into overlapping, sentence-aligned chunks.

    Two rules that matter more than the exact sizes:

    1. **Never split mid-sentence.** A chunk that ends "the refund window is 30"
       is worse than useless - it will retrieve confidently and answer wrongly.
    2. **Overlap by 10-20%.** A fact spanning a boundary would otherwise be
       invisible to both neighbouring chunks.

    Args:
        text: the document.
        chunk_size: target characters per chunk.
        overlap_ratio: fraction of each chunk repeated from the previous one.

    Raises:
        ValueError: if chunk_size < 1 or overlap_ratio is outside [0, 0.9].
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be >= 1")
    if not 0.0 <= overlap_ratio <= 0.9:
        raise ValueError("overlap_ratio must be between 0.0 and 0.9")

    text = text.strip()
    if not text:
        return []

    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(text) if s.strip()]
    if not sentences:
        return []

    overlap_chars = int(chunk_size * overlap_ratio)
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for sentence in sentences:
        # A single sentence longer than the budget becomes its own chunk rather
        # than being truncated - losing text is worse than an oversized chunk.
        if current and current_len + len(sentence) + 1 > chunk_size:
            chunks.append(" ".join(current))
            if overlap_chars > 0:
                tail: list[str] = []
                tail_len = 0
                for prev in reversed(current):
                    if tail_len + len(prev) > overlap_chars:
                        break
                    tail.insert(0, prev)
                    tail_len += len(prev) + 1
                current = tail
                current_len = tail_len
            else:
                current, current_len = [], 0
        current.append(sentence)
        current_len += len(sentence) + 1

    if current:
        chunks.append(" ".join(current))
    return chunks


# ---------------------------------------------------------------------------
# BM25 - the lexical half of hybrid search
# ---------------------------------------------------------------------------

_TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


class BM25:
    """Okapi BM25 keyword ranking.

    Vector search is weak at exact tokens: part numbers, SKUs, error codes,
    surnames. BM25 is excellent at exactly those and hopeless at paraphrase.
    Combining the two (see ``rag_agent.HybridRetriever``) beats either alone -
    which is why production RAG systems are almost always hybrid.

    k1 controls term-frequency saturation; b controls length normalisation.
    The values below are the standard defaults.
    """

    def __init__(self, corpus: Sequence[str], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.docs: list[list[str]] = [tokenize(d) for d in corpus]
        self.doc_count = len(self.docs)
        self.doc_lengths = [len(d) for d in self.docs]
        self.avg_doc_length = (
            sum(self.doc_lengths) / self.doc_count if self.doc_count else 0.0
        )

        self.term_frequencies: list[dict[str, int]] = []
        document_frequency: dict[str, int] = {}
        for doc in self.docs:
            freqs: dict[str, int] = {}
            for token in doc:
                freqs[token] = freqs.get(token, 0) + 1
            self.term_frequencies.append(freqs)
            for token in freqs:
                document_frequency[token] = document_frequency.get(token, 0) + 1

        # Smoothed IDF (Robertson): stays positive for very common terms.
        self.idf: dict[str, float] = {
            term: math.log(1 + (self.doc_count - df + 0.5) / (df + 0.5))
            for term, df in document_frequency.items()
        }

    def scores(self, query: str) -> NDArray[np.float64]:
        """BM25 score of `query` against every document."""
        out = np.zeros(self.doc_count, dtype=np.float64)
        if self.doc_count == 0 or self.avg_doc_length == 0:
            return out
        for term in tokenize(query):
            idf = self.idf.get(term)
            if idf is None:
                continue
            for i, freqs in enumerate(self.term_frequencies):
                tf = freqs.get(term, 0)
                if tf == 0:
                    continue
                denom = tf + self.k1 * (
                    1 - self.b + self.b * self.doc_lengths[i] / self.avg_doc_length
                )
                out[i] += idf * (tf * (self.k1 + 1)) / denom
        return out


def min_max_normalise(scores: NDArray[np.float64]) -> NDArray[np.float64]:
    """Scale scores into [0, 1] so BM25 and cosine can be blended.

    BM25 is unbounded; cosine lives in [-1, 1]. Adding them raw lets BM25
    dominate purely because of its scale. Normalise first, always.
    """
    if scores.size == 0:
        return scores
    lo, hi = float(scores.min()), float(scores.max())
    if math.isclose(hi, lo):
        return np.zeros_like(scores)
    return (scores - lo) / (hi - lo)
