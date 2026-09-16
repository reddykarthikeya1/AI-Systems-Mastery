"""Tests for Module 19: Real Elasticsearch Lucene Indexing & BM25 Scoring (Track B).

Validates:
1. ElasticLiveClient connection & health ping
2. Explicit mappings with text and keyword types
3. Bool compound search with BM25 score calculation
4. Term bucket aggregation
5. RECONCILIATION: Handbuilt TextAnalyzer tokenization, stopword removal, and stemming
6. RECONCILIATION: Handbuilt BM25Ranker monotonicity with term frequency
"""

from __future__ import annotations

import os
import pytest

from Module_19_Search_Engines_Elasticsearch_Lucene.project_solution.elastic_live import ElasticLiveClient
from Module_19_Search_Engines_Elasticsearch_Lucene.project_solution.search_engine import (
    TextAnalyzer as HandbuiltAnalyzer,
    InvertedIndex as HandbuiltIndex,
    BM25Ranker as HandbuiltBM25,
    CompletionTrie as HandbuiltTrie,
)

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "http://localhost:19200")
_elastic_available: bool | None = None


def elastic_is_available() -> bool:
    global _elastic_available
    if _elastic_available is None:
        try:
            client = ElasticLiveClient(host=ELASTIC_HOST)
            _elastic_available = client.ping()
        except Exception:
            _elastic_available = False
    return _elastic_available


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_text_analyzer_tokenization():
    """Verify handbuilt TextAnalyzer lowercases, strips punctuation, and removes stopwords via analyze()."""
    analyzer = HandbuiltAnalyzer()
    tokens = analyzer.analyze("The quick BROWN fox is jumping over the lazy dog!")

    # 'the' and 'is' are standard stopwords and must be stripped
    assert "brown" in tokens
    assert "fox" in tokens
    assert "the" not in tokens
    assert "is" not in tokens


def test_reconciliation_bm25_monotonicity():
    """Verify handbuilt BM25 relevance score strictly increases with higher term frequency in document."""
    index = HandbuiltIndex()
    # Doc 1 has 1 mention of 'database'
    index.add_document("doc1", "database storage model")
    # Doc 2 has 3 mentions of 'database'
    index.add_document("doc2", "database database database internals")

    ranker = HandbuiltBM25(k1=1.2, b=0.75)
    scores = dict(ranker.score(index, "database"))

    assert scores["doc1"] > 0
    assert scores["doc2"] > scores["doc1"]


# --- LIVE INTEGRATION TESTS (Skip if Elasticsearch service is offline) ---

@pytest.mark.requires_elastic
def test_elastic_ping():
    if not elastic_is_available():
        pytest.skip("Elasticsearch cluster is not running at http://localhost:19200")
    client = ElasticLiveClient(host=ELASTIC_HOST)
    assert client.ping() is True


@pytest.mark.requires_elastic
def test_elastic_indexing_and_search():
    if not elastic_is_available():
        pytest.skip("Elasticsearch cluster is not running at http://localhost:19200")
    client = ElasticLiveClient(host=ELASTIC_HOST)
    client.create_search_index("test_live_docs")
    client.index_document("test_live_docs", "doc1", {
        "title": "PostgreSQL MVCC Internals",
        "content": "Deep dive into PostgreSQL multi-version concurrency control and vacuuming.",
        "category": "Databases",
        "view_count": 120,
    })

    results = client.search_bm25("test_live_docs", "PostgreSQL concurrency", category_filter="Databases")
    assert len(results) >= 1
    assert results[0]["id"] == "doc1"
    assert results[0]["score"] > 0


# --- TYPEAHEAD AGAINST REAL ELASTICSEARCH ---

SUGGEST_INDEX = "course_m19_suggest"
SUGGEST_LOG = {
    "laptop": 5000,
    "laptop bag": 1200,
    "laptop stand": 900,
    "laptop charger": 700,
    "lamp": 3000,
    "keyboard": 4500,
}


@pytest.mark.skipif(not elastic_is_available(), reason="Elasticsearch is not reachable")
def test_completion_suggester_ranks_by_indexed_weight():
    """A real FST-backed `completion` field, not a text field with an analyzer.

    Elasticsearch builds a separate in-memory FST for this field type, which is
    what lets it answer inside a keystroke budget - and what makes it cost heap
    proportional to the vocabulary.
    """
    client = ElasticLiveClient(host=ELASTIC_HOST)
    client.create_suggest_index(SUGGEST_INDEX)
    for i, (phrase, weight) in enumerate(SUGGEST_LOG.items()):
        client.index_suggestion(SUGGEST_INDEX, f"s{i}", phrase, weight)

    results = client.suggest_completion(SUGGEST_INDEX, "la", size=3)
    assert [phrase for phrase, _ in results] == ["laptop", "lamp", "laptop bag"]


@pytest.mark.skipif(not elastic_is_available(), reason="Elasticsearch is not reachable")
def test_completion_suggester_narrows_as_the_user_types():
    client = ElasticLiveClient(host=ELASTIC_HOST)
    client.create_suggest_index(SUGGEST_INDEX)
    for i, (phrase, weight) in enumerate(SUGGEST_LOG.items()):
        client.index_suggestion(SUGGEST_INDEX, f"s{i}", phrase, weight)

    assert len(client.suggest_completion(SUGGEST_INDEX, "l", size=10)) == 5
    assert len(client.suggest_completion(SUGGEST_INDEX, "lapt", size=10)) == 4
    assert client.suggest_completion(SUGGEST_INDEX, "zzz", size=10) == []


@pytest.mark.skipif(not elastic_is_available(), reason="Elasticsearch is not reachable")
def test_fuzzy_completion_tolerates_a_typo():
    """Elasticsearch intersects a Levenshtein automaton with the FST - the
    production form of `bounded_edit_distance`."""
    client = ElasticLiveClient(host=ELASTIC_HOST)
    client.create_suggest_index(SUGGEST_INDEX)
    for i, (phrase, weight) in enumerate(SUGGEST_LOG.items()):
        client.index_suggestion(SUGGEST_INDEX, f"s{i}", phrase, weight)

    strict = client.suggest_completion(SUGGEST_INDEX, "laptp", size=5)
    fuzzy = client.suggest_fuzzy_completion(SUGGEST_INDEX, "laptp", fuzziness=1, size=5)

    assert strict == [], "a strict prefix query must not match a misspelling"
    assert "laptop" in [phrase for phrase, _ in fuzzy]


@pytest.mark.skipif(not elastic_is_available(), reason="Elasticsearch is not reachable")
def test_reconciliation_completion_suggester_matches_handbuilt_trie():
    """The reconciliation that matters for typeahead.

    The hand-built `CompletionTrie` and Elasticsearch's FST-backed completion
    field must agree on ranked suggestions for the same vocabulary. Where they
    disagree, the model in `search_engine.py` is lying about how a real
    suggester behaves.
    """
    client = ElasticLiveClient(host=ELASTIC_HOST)
    client.create_suggest_index(SUGGEST_INDEX)
    for i, (phrase, weight) in enumerate(SUGGEST_LOG.items()):
        client.index_suggestion(SUGGEST_INDEX, f"s{i}", phrase, weight)

    trie = HandbuiltTrie()
    for phrase, weight in SUGGEST_LOG.items():
        trie.insert(phrase, weight)

    for prefix in ("l", "la", "lap", "lapt", "ke"):
        live = client.suggest_completion(SUGGEST_INDEX, prefix, size=10)
        model = trie.suggest(prefix, limit=10)
        assert live == model, (
            f"prefix {prefix!r}: Elasticsearch returned {live}, model returned {model}"
        )


@pytest.mark.skipif(not elastic_is_available(), reason="Elasticsearch is not reachable")
def test_edge_ngram_field_answers_the_same_prefix_query():
    """The other mechanism, on the same data.

    Note the mapping: `search_analyzer` is `standard`, not the edge_ngram
    analyzer. Analysing the query with edge_ngram as well would match every
    prefix of the query against every prefix of every term - the classic
    edge_ngram misconfiguration, and it produces wildly irrelevant hits.
    """
    client = ElasticLiveClient(host=ELASTIC_HOST)
    client.create_suggest_index(SUGGEST_INDEX)
    for i, (phrase, weight) in enumerate(SUGGEST_LOG.items()):
        client.index_suggestion(SUGGEST_INDEX, f"s{i}", phrase, weight)

    results = client.suggest_edge_ngram(SUGGEST_INDEX, "lap", size=5)
    phrases = [phrase for phrase, _ in results]
    assert phrases[0] == "laptop", f"most popular 'lap' prefix should lead, got {phrases}"
    assert all(p.startswith("laptop") for p in phrases), phrases
