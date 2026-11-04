"""Distributed Hybrid Search: Okapi BM25 Lexical, Dense Vector Semantic & RRF.

Mathematical Formulation:
--------------------------
1. Okapi BM25 Lexical Ranking:
   For query Q with terms {q_1, q_2, ... q_n} and document D:
       BM25(D, Q) = sum_{q_i in Q} IDF(q_i) * [ f(q_i, D) * (k1 + 1) ] / [ f(q_i, D) + k1 * (1 - b + b * (|D| / avgdl)) ]
   where:
       IDF(q_i) = ln( (N - n(q_i) + 0.5) / (n(q_i) + 0.5) + 1 )
       f(q_i, D) = term frequency of q_i in document D
       |D| = document length (number of tokens in D)
       avgdl = average document length across all documents in corpus
       k1 = term saturation parameter (default 1.5)
       b = length normalization parameter (default 0.75)

2. Dense Vector Cosine Similarity:
   Cosine(u, v) = (u . v) / ( ||u||_2 * ||v||_2 )

3. Reciprocal Rank Fusion (RRF) (Cormack, Clarke, Buettcher):
   Combines disparate ranked result sets without score calibration:
       RRF_Score(d) = sum_{m in Models} [ 1.0 / (k + rank_m(d)) ]
   where k is a constant penalty parameter (default k = 60), rank_m(d) is 1-based rank.
"""

from __future__ import annotations
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class SearchResult:
    doc_id: str
    score: float
    rank: int = 1
    content: Optional[str] = None


def tokenize(text: str) -> List[str]:
    """Basic lowercased alphanumeric tokenizer."""
    return re.findall(r"\b[a-zA-Z0-9_-]+\b", text.lower())


def cosine_similarity(v1: Sequence[float], v2: Sequence[float]) -> float:
    """Compute cosine similarity between two dense vectors."""
    if len(v1) != len(v2):
        raise ValueError("Vector dimensions must match")
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot / (norm1 * norm2)


class BM25Index:
    """Production Inverted Index implementing Okapi BM25."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.doc_lengths: Dict[str, int] = {}
        self.doc_contents: Dict[str, str] = {}
        # term -> {doc_id: count}
        self.inverted_index: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.total_tokens = 0

    @property
    def total_docs(self) -> int:
        return len(self.doc_lengths)

    @property
    def avgdl(self) -> float:
        if not self.doc_lengths:
            return 0.0
        return self.total_tokens / float(len(self.doc_lengths))

    def add_document(self, doc_id: str, content: str) -> None:
        """Indexes a document into inverted index."""
        tokens = tokenize(content)
        doc_len = len(tokens)
        self.doc_lengths[doc_id] = doc_len
        self.doc_contents[doc_id] = content
        self.total_tokens += doc_len

        tf = Counter(tokens)
        for term, count in tf.items():
            self.inverted_index[term][doc_id] = count

    def _idf(self, term: str) -> float:
        """Compute Lucene/Robertson IDF:

        ln( (N - n + 0.5) / (n + 0.5) + 1 )
        """
        n = len(self.inverted_index.get(term, {}))
        total_docs = self.total_docs
        return math.log(((total_docs - n + 0.5) / (n + 0.5)) + 1.0)

    def search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """Search query tokens against BM25 index and return ranked results."""
        query_terms = tokenize(query)
        if not query_terms or self.total_docs == 0:
            return []

        avg_len = self.avgdl
        scores: Dict[str, float] = defaultdict(float)

        for term in query_terms:
            if term not in self.inverted_index:
                continue
            idf = self._idf(term)
            doc_counts = self.inverted_index[term]

            for doc_id, tf in doc_counts.items():
                doc_len = self.doc_lengths[doc_id]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / avg_len))
                scores[doc_id] += idf * (numerator / denominator)

        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [
            SearchResult(
                doc_id=doc_id,
                score=score,
                rank=i + 1,
                content=self.doc_contents.get(doc_id),
            )
            for i, (doc_id, score) in enumerate(sorted_results)
        ]


class DenseVectorIndex:
    """Dense vector cosine similarity search index."""

    def __init__(self) -> None:
        self.doc_vectors: Dict[str, List[float]] = {}
        self.doc_contents: Dict[str, str] = {}

    def add_document(self, doc_id: str, vector: List[float], content: Optional[str] = None) -> None:
        self.doc_vectors[doc_id] = list(vector)
        if content:
            self.doc_contents[doc_id] = content

    def search(self, query_vector: List[float], top_k: int = 10) -> List[SearchResult]:
        """Search nearest documents by cosine similarity."""
        scores: List[Tuple[str, float]] = []
        for doc_id, vec in self.doc_vectors.items():
            sim = cosine_similarity(query_vector, vec)
            scores.append((doc_id, sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        top_scores = scores[:top_k]
        return [
            SearchResult(
                doc_id=doc_id,
                score=score,
                rank=i + 1,
                content=self.doc_contents.get(doc_id),
            )
            for i, (doc_id, score) in enumerate(top_scores)
        ]


def reciprocal_rank_fusion(
    ranked_lists: List[List[SearchResult]],
    k: int = 60,
    top_k: int = 10,
) -> List[SearchResult]:
    """Combines multiple ranked lists using Reciprocal Rank Fusion (RRF).

    Formula:
        RRF_Score(d) = sum_{m in Lists} ( 1.0 / (k + rank_m(d)) )
    """
    rrf_scores: Dict[str, float] = defaultdict(float)
    doc_contents: Dict[str, Optional[str]] = {}

    for ranked_list in ranked_lists:
        for item in ranked_list:
            rrf_scores[item.doc_id] += 1.0 / (k + item.rank)
            if item.content and item.doc_id not in doc_contents:
                doc_contents[item.doc_id] = item.content

    sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [
        SearchResult(
            doc_id=doc_id,
            score=score,
            rank=i + 1,
            content=doc_contents.get(doc_id),
        )
        for i, (doc_id, score) in enumerate(sorted_docs)
    ]


class HybridSearchEngine:
    """Unified Lexical (BM25) and Semantic (Dense Vector) search engine with RRF."""

    def __init__(self, k_rrf: int = 60) -> None:
        self.bm25 = BM25Index()
        self.vector_index = DenseVectorIndex()
        self.k_rrf = k_rrf

    def add_document(self, doc_id: str, content: str, embedding: List[float]) -> None:
        self.bm25.add_document(doc_id, content)
        self.vector_index.add_document(doc_id, embedding, content=content)

    def search_hybrid(
        self,
        query_text: str,
        query_embedding: List[float],
        top_k: int = 10,
    ) -> List[SearchResult]:
        bm25_results = self.bm25.search(query_text, top_k=top_k * 2)
        dense_results = self.vector_index.search(query_embedding, top_k=top_k * 2)
        return reciprocal_rank_fusion([bm25_results, dense_results], k=self.k_rrf, top_k=top_k)
