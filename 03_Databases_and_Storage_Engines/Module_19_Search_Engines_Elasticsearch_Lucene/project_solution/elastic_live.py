"""Module 19: Real Elasticsearch Lucene Indexing & BM25 Scoring (Track B).

Interacts directly with Elasticsearch via the official elasticsearch-py client to demonstrate:
1. Index creation with explicit mappings, analyzers, and stopword token filters.
2. BM25 scoring and term frequency / document length saturation.
3. Bool compound queries combining must, should, and filter clauses.
4. Fuzzy matching handling typo tolerance (Levenshtein edit distance).
5. Fast aggregation pipelines (terms bucket aggregations and stats metrics).
"""

from __future__ import annotations


import socket
from urllib.parse import urlparse
from typing import Any

try:
    from elasticsearch import Elasticsearch
except ImportError:
    Elasticsearch = None  # type: ignore


class ElasticLiveClient:
    """Production Elasticsearch client for full-text search and BM25 relevance."""

    def __init__(self, host: str = "http://localhost:19200"):
        if Elasticsearch is None:
            raise RuntimeError("elasticsearch is not installed. Install with: pip install elasticsearch")
        self.host = host
        self.es = Elasticsearch(hosts=[self.host], request_timeout=2.0)

    def ping(self) -> bool:
        try:
            p = urlparse(self.host)
            host = p.hostname or "localhost"
            port = p.port or 9200
            with socket.create_connection((host, port), timeout=0.2):
                pass
            return bool(self.es.ping())
        except Exception:
            return False

    def create_search_index(self, index_name: str = "kb_articles") -> None:
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)

        mappings = {
            "properties": {
                "title": {"type": "text", "analyzer": "standard"},
                "content": {"type": "text", "analyzer": "standard"},
                "category": {"type": "keyword"},
                "view_count": {"type": "integer"},
            }
        }
        self.es.indices.create(index=index_name, mappings=mappings)

    def index_document(self, index_name: str, doc_id: str, doc: dict[str, Any]) -> None:
        self.es.index(index=index_name, id=doc_id, document=doc, refresh=True)

    def search_bm25(self, index_name: str, query_text: str, category_filter: str | None = None) -> list[dict[str, Any]]:
        must_clauses: list[dict[str, Any]] = [
            {"multi_match": {"query": query_text, "fields": ["title^2", "content"]}}
        ]
        filter_clauses: list[dict[str, Any]] = []
        if category_filter:
            filter_clauses.append({"term": {"category": category_filter}})

        body = {
            "query": {
                "bool": {
                    "must": must_clauses,
                    "filter": filter_clauses,
                }
            }
        }
        resp = self.es.search(index=index_name, body=body)
        return [
            {"id": hit["_id"], "score": hit["_score"], "source": hit["_source"]}
            for hit in resp["hits"]["hits"]
        ]

    # -- typeahead against real Elasticsearch -------------------------------
    def create_suggest_index(self, index_name: str) -> None:
        """Create an index with a real ``completion`` field.

        ``completion`` is not a text field with a clever analyzer - Elasticsearch
        builds a separate in-memory FST for it, which is why it can answer a
        prefix query inside a keystroke budget and why it costs heap in
        proportion to the vocabulary. That is the same structure ``CompletionTrie``
        models, minus the suffix minimisation.

        ``edge_ngram`` is also configured here so both mechanisms can be compared
        against the same data - the trade-off the Track A tests measure.
        """
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)

        self.es.indices.create(
            index=index_name,
            settings={
                "analysis": {
                    "tokenizer": {
                        "edge_ngram_tok": {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 20,
                            "token_chars": ["letter", "digit"],
                        }
                    },
                    "analyzer": {
                        "edge_ngram_idx": {
                            "type": "custom",
                            "tokenizer": "edge_ngram_tok",
                            "filter": ["lowercase"],
                        }
                    },
                }
            },
            mappings={
                "properties": {
                    # The FST-backed suggester.
                    "suggest": {"type": "completion"},
                    # The edge n-gram alternative. `search_analyzer` is `standard`
                    # on purpose: analysing the QUERY with edge_ngram too would
                    # match every prefix of the query against every prefix of
                    # every term, which is the classic edge_ngram misconfiguration
                    # and produces wildly irrelevant hits.
                    "title": {
                        "type": "text",
                        "analyzer": "edge_ngram_idx",
                        "search_analyzer": "standard",
                    },
                    "popularity": {"type": "integer"},
                }
            },
        )

    def index_suggestion(self, index_name: str, doc_id: str, phrase: str, weight: int) -> None:
        self.es.index(
            index=index_name,
            id=doc_id,
            document={
                "suggest": {"input": [phrase], "weight": weight},
                "title": phrase,
                "popularity": weight,
            },
            refresh=True,
        )

    def suggest_completion(
        self, index_name: str, prefix: str, size: int = 5
    ) -> list[tuple[str, int]]:
        """Prefix suggestions from the FST, ranked by the indexed weight."""
        resp = self.es.search(
            index=index_name,
            suggest={
                "phrase_suggest": {
                    "prefix": prefix,
                    "completion": {"field": "suggest", "size": size},
                }
            },
        )
        options = resp["suggest"]["phrase_suggest"][0]["options"]
        return [(o["text"], o["_source"]["popularity"]) for o in options]

    def suggest_fuzzy_completion(
        self, index_name: str, prefix: str, fuzziness: int = 1, size: int = 5
    ) -> list[tuple[str, int]]:
        """Typo-tolerant prefix suggestions.

        Elasticsearch intersects a Levenshtein automaton with the FST, which is
        the production form of the bounded edit distance in ``search_engine.py``.
        """
        resp = self.es.search(
            index=index_name,
            suggest={
                "phrase_suggest": {
                    "prefix": prefix,
                    "completion": {
                        "field": "suggest",
                        "size": size,
                        "fuzzy": {"fuzziness": fuzziness},
                    },
                }
            },
        )
        options = resp["suggest"]["phrase_suggest"][0]["options"]
        return [(o["text"], o["_source"]["popularity"]) for o in options]

    def suggest_edge_ngram(
        self, index_name: str, prefix: str, size: int = 5
    ) -> list[tuple[str, int]]:
        """The same query answered by the edge n-gram field instead of the FST."""
        resp = self.es.search(
            index=index_name,
            query={"match": {"title": prefix}},
            sort=[{"popularity": "desc"}],
            size=size,
        )
        return [
            (hit["_source"]["title"], hit["_source"]["popularity"])
            for hit in resp["hits"]["hits"]
        ]
