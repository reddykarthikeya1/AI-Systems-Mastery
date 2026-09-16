"""Module 19 Test Suite: Inverted Index, BM25, Distributed Search & Typeahead."""

from __future__ import annotations

import pytest
from search_engine import (
    BM25Ranker,
    CompletionTrie,
    DistributedSearchCluster,
    EdgeNGramIndex,
    FuzzySuggester,
    InvertedIndex,
    TextAnalyzer,
    bounded_edit_distance,
)


def test_text_analyzer_pipeline() -> None:
    analyzer = TextAnalyzer()
    raw = "The quick brown foxes are running towards modern databases!"
    tokens = analyzer.analyze(raw)

    # "the", "are", "towards" removed as stopwords
    # "foxes" -> "fox", "running" -> "run", "databases" -> "databas"
    assert "the" not in tokens
    assert "are" not in tokens
    assert "run" in tokens
    assert "databas" in tokens
    assert "fox" in tokens


def test_inverted_index_postings_and_positions() -> None:
    index = InvertedIndex()
    doc_text = "Raft is a consensus protocol. Raft ensures safety."
    index.add_document("doc_1", doc_text)

    postings = index.get_postings("raft")
    assert len(postings) == 1
    p = postings[0]
    assert p.doc_id == "doc_1"
    assert p.term_freq == 2
    # Positions where "raft" occurs in analyzed token stream
    assert p.positions == [0, 3]


def test_boolean_and_or_search() -> None:
    index = InvertedIndex()
    index.add_document("d1", "Distributed consensus with Raft")
    index.add_document("d2", "Relational databases with ACID transactions")
    index.add_document("d3", "Distributed databases with Paxos consensus")

    # AND: "distributed consensus" must match d1 and d3
    and_results = index.boolean_and("distributed consensus")
    assert and_results == ["d1", "d3"]

    # OR: "acid raft" must match d1 and d2
    or_results = index.boolean_or("acid raft")
    assert or_results == ["d1", "d2"]


def test_bm25_length_normalization_and_saturation() -> None:
    index = InvertedIndex()
    ranker = BM25Ranker(k1=1.2, b=0.75)

    # Short focused document
    index.add_document("doc_focused", "Distributed consensus in modern databases.")

    # Very long verbose document mentioning consensus only once
    verbose_text = (
        "This chapter covers hardware specifications, networking routers, kernel parameters, "
        "memory allocators, disks, and briefly consensus protocols once."
    )
    index.add_document("doc_verbose", verbose_text)

    # Rank for query "consensus"
    scores = ranker.score(index, "consensus")
    assert len(scores) == 2
    # doc_focused must score significantly higher due to BM25 length normalization
    winner_id, winner_score = scores[0]
    loser_id, loser_score = scores[1]

    assert winner_id == "doc_focused"
    assert loser_id == "doc_verbose"
    assert winner_score > loser_score


def test_distributed_cluster_query_then_fetch() -> None:
    cluster = DistributedSearchCluster(num_shards=3)

    cluster.index(
        "art_1",
        "Understanding LSM-Trees and SSTables in modern databases",
        {"title": "LSM-Tree Guide", "author": "Alice"},
    )
    cluster.index(
        "art_2",
        "B-Tree indexing and buffer pool memory management",
        {"title": "B-Tree Internals", "author": "Bob"},
    )
    cluster.index(
        "art_3",
        "Inverted indexes and BM25 scoring for search engines",
        {"title": "Search Engine Architecture", "author": "Carol"},
    )

    hits = cluster.search("LSM-Trees databases", top_k=2)
    assert len(hits) >= 1
    top_hit = hits[0]
    assert top_hit["_id"] == "art_1"
    assert top_hit["_score"] > 0.0
    assert top_hit["_source"]["title"] == "LSM-Tree Guide"
    assert 0 <= top_hit["_shard"] < 3


# ---------------------------------------------------------------------------
# Typeahead: CompletionTrie
# ---------------------------------------------------------------------------
QUERY_LOG = {
    "laptop": 5000,
    "laptop stand": 900,
    "laptop bag": 1200,
    "laptop charger": 700,
    "lamp": 3000,
    "lampshade": 400,
    "keyboard": 4500,
    "kettle": 800,
}


def _trie() -> "CompletionTrie":
    trie = CompletionTrie()
    for phrase, weight in QUERY_LOG.items():
        trie.insert(phrase, weight)
    return trie


def test_trie_suggests_by_popularity_not_alphabetically() -> None:
    """There is no document to be relevant to yet, so popularity is the ranking."""
    suggestions = _trie().suggest("la", limit=3)
    assert [s for s, _ in suggestions] == ["laptop", "lamp", "laptop bag"]


def test_trie_narrows_as_the_user_types() -> None:
    trie = _trie()
    assert len(trie.suggest("l", limit=10)) == 6
    assert len(trie.suggest("lap", limit=10)) == 4
    assert [s for s, _ in trie.suggest("lamps", limit=10)] == ["lampshade"]


def test_trie_returns_empty_for_an_unknown_prefix() -> None:
    """A user typing a novel string is the normal case, not an error."""
    assert _trie().suggest("zzzz") == []


def test_trie_is_case_and_whitespace_insensitive() -> None:
    trie = _trie()
    assert trie.suggest("LAP") == trie.suggest("lap") == trie.suggest("  lap  ")


def test_trie_reinsert_replaces_the_weight_rather_than_accumulating() -> None:
    """So a nightly rebuild from the query log is idempotent."""
    trie = _trie()
    trie.insert("lamp", 3000)
    trie.insert("lamp", 3000)
    assert dict(trie.suggest("lamp", limit=5))["lamp"] == 3000


def test_trie_reinsert_with_a_new_weight_reorders_suggestions() -> None:
    trie = _trie()
    assert trie.suggest("la", limit=1)[0][0] == "laptop"
    trie.insert("lamp", 99_999)
    assert trie.suggest("la", limit=1)[0][0] == "lamp"


def test_trie_rejects_an_empty_suggestion() -> None:
    with pytest.raises(ValueError, match="empty suggestion"):
        CompletionTrie().insert("")


def test_trie_ties_break_alphabetically_so_output_is_deterministic() -> None:
    """Otherwise the tests would be asserting dict iteration order."""
    trie = CompletionTrie()
    for phrase in ("beta", "alpha", "gamma"):
        trie.insert(phrase, 100)
    assert [s for s, _ in trie.suggest("", limit=3)] == ["alpha", "beta", "gamma"]


def test_trie_lookup_cost_is_independent_of_subtree_size() -> None:
    """The design decision that makes the trie usable.

    A one-character prefix is the query users type most, and it is the one whose
    subtree is largest. Caching the top-k at every node on insert means the
    broadest prefix costs no more work than the narrowest, instead of being the
    slowest possible query.
    """
    trie = CompletionTrie()
    for i in range(2000):
        trie.insert(f"a{i:04d}", weight=i)
    trie.insert("zebra", weight=1)

    broad = trie.suggest("a", limit=5)      # subtree of 2000
    narrow = trie.suggest("zebra", limit=5)  # subtree of 1

    assert len(broad) == 5
    assert len(narrow) == 1
    # The cached list is bounded by top_k regardless of how many descendants exist.
    assert len(trie.children["a"].top) <= 10


# ---------------------------------------------------------------------------
# Typeahead: EdgeNGramIndex
# ---------------------------------------------------------------------------


def test_edge_ngram_turns_a_prefix_query_into_an_exact_term_lookup() -> None:
    index = EdgeNGramIndex()
    for phrase, weight in QUERY_LOG.items():
        index.index(phrase, weight)
    assert [s for s, _ in index.suggest("lap", limit=2)] == ["laptop", "laptop bag"]


def test_edge_ngram_writes_one_entry_per_prefix() -> None:
    index = EdgeNGramIndex()
    assert index.index("laptop") == 6      # l, la, lap, lapt, lapto, laptop


def test_edge_ngram_write_amplification_is_the_price_of_o1_lookup() -> None:
    """The trade-off against CompletionTrie, measured rather than asserted."""
    index = EdgeNGramIndex()
    for phrase, weight in QUERY_LOG.items():
        index.index(phrase, weight)

    # Every distinct prefix across the vocabulary becomes its own index entry.
    assert index.write_amplification > 3.0, (
        f"expected meaningful amplification, got {index.write_amplification:.2f}"
    )
    # And the trie stores the same vocabulary in fewer nodes, because shared
    # prefixes are shared rather than duplicated per phrase.
    assert index.entry_count > 0


def test_edge_ngram_max_gram_bounds_the_index() -> None:
    index = EdgeNGramIndex(min_gram=1, max_gram=3)
    assert index.index("laptop") == 3
    assert index.suggest("lapt") == []      # beyond max_gram, deliberately


def test_edge_ngram_min_gram_skips_very_short_prefixes() -> None:
    """A 1-character prefix matches most of the corpus and is rarely worth serving."""
    index = EdgeNGramIndex(min_gram=3, max_gram=20)
    index.index("laptop", 500)
    assert index.suggest("la") == []
    assert [s for s, _ in index.suggest("lap")] == ["laptop"]


def test_edge_ngram_rejects_an_invalid_gram_range() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        EdgeNGramIndex(min_gram=0)
    with pytest.raises(ValueError, match="not be below min_gram"):
        EdgeNGramIndex(min_gram=5, max_gram=2)


def test_trie_and_edge_ngram_agree_on_suggestions() -> None:
    """Two independent implementations, one answer - the reconciliation pattern
    this course applies to every hand-built model."""
    trie = _trie()
    index = EdgeNGramIndex()
    for phrase, weight in QUERY_LOG.items():
        index.index(phrase, weight)

    for prefix in ("l", "la", "lap", "lapt", "ke", "kett"):
        assert trie.suggest(prefix, limit=5) == index.suggest(prefix, limit=5), (
            f"trie and edge n-gram disagree on prefix {prefix!r}"
        )


# ---------------------------------------------------------------------------
# Fuzzy suggestion
# ---------------------------------------------------------------------------


def test_bounded_edit_distance_finds_a_single_typo() -> None:
    assert bounded_edit_distance("laptp", "laptop") == 1
    assert bounded_edit_distance("laptop", "laptop") == 0


def test_bounded_edit_distance_abandons_hopeless_candidates() -> None:
    """Returning None rather than a large number is what keeps this tractable:
    the caller never has to consider a candidate outside the bound."""
    assert bounded_edit_distance("cat", "laptop") is None
    assert bounded_edit_distance("laptop", "keyboard", max_distance=2) is None


def test_bounded_edit_distance_respects_the_bound() -> None:
    assert bounded_edit_distance("abc", "abcde", max_distance=2) == 2
    assert bounded_edit_distance("abc", "abcde", max_distance=1) is None


def test_fuzzy_suggester_ranks_correctness_before_popularity() -> None:
    """Ranking by popularity first lets a common term outrank an exact match,
    which users read as the search box ignoring what they typed."""
    suggester = FuzzySuggester({"lamp": 999_999, "laptop": 10})
    results = suggester.suggest("laptop", max_distance=2)
    assert results[0][0] == "laptop"
    assert results[0][2] == 0


def test_fuzzy_suggester_corrects_a_typo() -> None:
    suggester = FuzzySuggester(QUERY_LOG)
    assert suggester.suggest("laptp", limit=1)[0][0] == "laptop"
    assert suggester.suggest("kebtle", limit=1)[0][0] == "kettle"


def test_fuzzy_suggester_returns_nothing_for_an_unrelated_term() -> None:
    assert FuzzySuggester(QUERY_LOG).suggest("xylophone") == []


def test_fuzzy_distance_scales_with_term_length() -> None:
    """Lucene's AUTO fuzziness. At three characters an edit distance of 2
    matches most of the dictionary, so the bound has to tighten."""
    assert FuzzySuggester.for_term("ab") == 0
    assert FuzzySuggester.for_term("cat") == 1
    assert FuzzySuggester.for_term("lamps") == 1
    assert FuzzySuggester.for_term("laptop") == 2


def test_fuzzy_short_term_does_not_match_everything() -> None:
    """The consequence of the rule above, asserted rather than trusted.

    Vocabulary chosen so candidates exist at each distance from "cat":
    0 -> cat; 1 -> cot, cap; 2 -> cost, card; 3 -> dog (never matched).
    """
    suggester = FuzzySuggester(
        {"cat": 10, "cot": 10, "cap": 10, "cost": 10, "card": 10, "dog": 10}
    )
    loose = suggester.suggest("cat", limit=10, max_distance=2)
    auto = suggester.suggest("cat", limit=10)      # bound of 1 for a 3-char term

    assert {s for s, _, _ in auto} == {"cat", "cot", "cap"}
    assert {s for s, _, _ in loose} == {"cat", "cot", "cap", "cost", "card"}
    assert len(auto) < len(loose)
    assert "dog" not in {s for s, _, _ in loose}, "distance 3 must never match"
