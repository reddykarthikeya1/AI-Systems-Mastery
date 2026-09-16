"""STARTER - Module 25: AI Engineering LLM Integration

Module 25 - Embeddings: three backends, and one of them is a trap.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_embeddings.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/embeddings.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import hashlib
import math
import re
from abc import ABC, abstractmethod
from collections.abc import Sequence
import numpy as np
from numpy.typing import NDArray

def cosine_similarity(u: NDArray[np.float64], v: NDArray[np.float64]) -> float:
    """Cosine of the angle between two vectors, in [-1, 1].

    cos(theta) = (u . v) / (||u|| ||v||)

    Why cosine and not Euclidean distance? Cosine ignores magnitude and compares
    *direction* only. A one-sentence document and a ten-page document about the
    same topic point the same way but have very different lengths.

    """
    # [Tier 2] Algorithm: Implement cosine_similarity adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_cosine_similarity_identical_vectors_is_one
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 25: implement cosine_similarity()")


def cosine_similarity_matrix(
    query: NDArray[np.float64], matrix: NDArray[np.float64]
) -> NDArray[np.float64]:
    """Cosine similarity of one query against every row of `matrix` at once.

    This is the vectorised form: one BLAS call instead of a Python loop over
    documents. At 100k chunks that is the difference between 20 ms and 8 s.

    """
    # [Tier 2] Algorithm: Implement cosine_similarity_matrix adhering to the
    #   contract defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_cosine_matrix_matches_pairwise_loop
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 25: implement cosine_similarity_matrix()")


class Embedder(ABC):
    """Common interface for every embedding backend."""
    name: str = "abstract"
    dimensions: int = 0

    def fit(self, corpus: Sequence[str]) -> Embedder:
        """Learn any corpus statistics needed. Pre-trained backends no-op here."""
        # [Tier 2] Algorithm: Implement Embedder.fit adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_tfidf_embedder_requires_fit_before_encode
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement Embedder.fit()")


    @abstractmethod
    def encode_one(self, text: str) -> NDArray[np.float64]:
        """Embed a single string."""
        # [Tier 2] Algorithm: Implement Embedder.encode_one adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES:
        #   test_hash_embedder_gives_near_zero_similarity_to_near_identical_text
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement Embedder.encode_one()")


    def encode(self, texts: Sequence[str]) -> NDArray[np.float64]:
        """Embed a batch, returning shape (len(texts), dimensions)."""
        # [Tier 2] Algorithm: Implement Embedder.encode adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_tfidf_embedder_requires_fit_before_encode
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement Embedder.encode()")



class HashEmbedder(Embedder):
    """❌ **NOT A REAL EMBEDDER.** Kept only as a demonstrable negative example.

    SHA-256 is designed so that flipping one input bit changes ~half the output
    bits. Semantic similarity is therefore *impossible* by construction:
    "cat" and "cats" are as far apart as "cat" and "thermodynamics".

    Never use this for retrieval. See ``test_hash_embedder_cannot_do_semantics``.

    """
    name = "hash-BROKEN"

    def __init__(self, dimensions: int = 64) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_cosine_similarity_identical_vectors_is_one
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 25: implement HashEmbedder.__init__()")


    def encode_one(self, text: str) -> NDArray[np.float64]:
        # [Tier 2] Algorithm: Implement HashEmbedder.encode_one adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES:
        #   test_hash_embedder_gives_near_zero_similarity_to_near_identical_text
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement HashEmbedder.encode_one()")



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
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_cosine_similarity_identical_vectors_is_one
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 25: implement TfidfSvdEmbedder.__init__()")


    def fit(self, corpus: Sequence[str]) -> TfidfSvdEmbedder:
        # [Tier 2] Algorithm: Implement TfidfSvdEmbedder.fit adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_tfidf_embedder_requires_fit_before_encode
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement TfidfSvdEmbedder.fit()")


    def encode_one(self, text: str) -> NDArray[np.float64]:
        # [Tier 2] Algorithm: Implement TfidfSvdEmbedder.encode_one adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES:
        #   test_hash_embedder_gives_near_zero_similarity_to_near_identical_text
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement TfidfSvdEmbedder.encode_one()")


    def encode(self, texts: Sequence[str]) -> NDArray[np.float64]:
        # [Tier 2] Algorithm: Implement TfidfSvdEmbedder.encode adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_tfidf_embedder_requires_fit_before_encode
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement TfidfSvdEmbedder.encode()")



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
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_cosine_similarity_identical_vectors_is_one
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 25: implement SentenceTransformerEmbedder.__init__()")


    @staticmethod
    def is_available() -> bool:
        # [Tier 2] Algorithm: Implement SentenceTransformerEmbedder.is_available
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_cosine_similarity_identical_vectors_is_one
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement SentenceTransformerEmbedder.is_available()")


    def fit(self, corpus: Sequence[str]) -> SentenceTransformerEmbedder:
        # [Tier 2] Algorithm: Implement SentenceTransformerEmbedder.fit adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_tfidf_embedder_requires_fit_before_encode
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement SentenceTransformerEmbedder.fit()")


    def _load(self) -> object:
        # [Tier 1] Algorithm: Normalize raw input data structure into typed
        #   domain representation.
        # HINTS:
        #  - Handle missing optional keys with sensible defaults (.get()
        #   pattern).
        #  - Coerce primitive data types safely and strip surrounding
        #   whitespace.
        # GRADES: test_load_embedder_never_returns_broken_backend_implicitly
        # WARNING: Watch for unexpected null or None values in optional fields.
        raise NotImplementedError("Module 25: implement SentenceTransformerEmbedder._load()")


    def encode_one(self, text: str) -> NDArray[np.float64]:
        # [Tier 2] Algorithm: Implement SentenceTransformerEmbedder.encode_one
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES:
        #   test_hash_embedder_gives_near_zero_similarity_to_near_identical_text
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement SentenceTransformerEmbedder.encode_one()")


    def encode(self, texts: Sequence[str]) -> NDArray[np.float64]:
        # [Tier 2] Algorithm: Implement SentenceTransformerEmbedder.encode
        #   adhering to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_tfidf_embedder_requires_fit_before_encode
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement SentenceTransformerEmbedder.encode()")



def load_embedder(prefer: str = "auto", dimensions: int = 128) -> Embedder:
    """Return the best available *real* embedder.

    ``prefer``: "auto" | "tfidf" | "transformer" | "hash"

    Note that "hash" must be requested explicitly and by name. There is no code
    path in which a broken embedder is selected silently - which is exactly the
    bug this module used to contain.

    """
    # [Tier 1] Algorithm: Normalize raw input data structure into typed domain
    #   representation.
    # HINTS:
    #  - Handle missing optional keys with sensible defaults (.get() pattern).
    #  - Coerce primitive data types safely and strip surrounding whitespace.
    # GRADES: test_load_embedder_never_returns_broken_backend_implicitly
    # WARNING: Watch for unexpected null or None values in optional fields.
    raise NotImplementedError("Module 25: implement load_embedder()")

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
    # [Tier 2] Algorithm: Implement chunk_text adhering to the contract defined
    #   in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_chunking_never_splits_mid_sentence
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 25: implement chunk_text()")

_TOKEN = re.compile(r"[a-z0-9]+")

def tokenize(text: str) -> list[str]:
    # [Tier 2] Algorithm: Implement tokenize adhering to the contract defined in
    #   docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_chunking_produces_overlap
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 25: implement tokenize()")


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
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_cosine_similarity_identical_vectors_is_one
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 25: implement BM25.__init__()")


    def scores(self, query: str) -> NDArray[np.float64]:
        """BM25 score of `query` against every document."""
        # [Tier 2] Algorithm: Implement BM25.scores adhering to the contract
        #   defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_bm25_unknown_term_scores_zero_everywhere
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 25: implement BM25.scores()")



def min_max_normalise(scores: NDArray[np.float64]) -> NDArray[np.float64]:
    """Scale scores into [0, 1] so BM25 and cosine can be blended.

    BM25 is unbounded; cosine lives in [-1, 1]. Adding them raw lets BM25
    dominate purely because of its scale. Normalise first, always.

    """
    # [Tier 2] Algorithm: Implement min_max_normalise adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_min_max_normalise_maps_to_unit_range
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 25: implement min_max_normalise()")
