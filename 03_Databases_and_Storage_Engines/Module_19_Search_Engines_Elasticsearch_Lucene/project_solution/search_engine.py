"""Module 19: Inverted Index & Okapi BM25 Search Engine (Solution).

Implements:
1. TextAnalyzer: Tokenization, stopword removal, and morphological suffix stemming.
2. InvertedIndex: Term dictionary and postings list with positions and frequencies.
3. BM25Ranker: Exact Lucene/Okapi BM25 relevance scoring.
4. DistributedSearchCluster: Two-Phase Query-Then-Fetch distributed search simulation.
5. CompletionTrie / EdgeNGramIndex: the two typeahead mechanisms, with the
   index-size vs lookup-cost trade-off between them measured, not asserted.
6. FuzzySuggester: typo tolerance via a bounded Levenshtein distance, which is
   the tractable form of Lucene's Levenshtein-automaton intersection.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Any


class TextAnalyzer:
    """Text processing pipeline executing tokenization, stopword filtering, and stemming."""

    def __init__(self, stopwords: set[str] | None = None) -> None:
        self.stopwords = stopwords if stopwords is not None else {
            "the", "a", "an", "is", "are", "was", "were", "in", "and", "or", "for", "to",
            "of", "with", "at", "by", "from", "on", "towards", "toward",
        }

    def tokenize(self, text: str) -> list[str]:
        return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9]+\b", text)]

    def stem(self, token: str) -> str:
        t = token
        if t.endswith("ing") and len(t) > 5:
            t = t[:-3]
            if len(t) > 2 and t[-1] == t[-2] and t[-1] in "bdfgmnprtz":
                t = t[:-1]
        elif t.endswith("ed") and len(t) > 4:
            t = t[:-2]
            if len(t) > 2 and t[-1] == t[-2] and t[-1] in "bdfgmnprtz":
                t = t[:-1]
        elif t.endswith("es") and len(t) > 4:
            t = t[:-2]
        elif t.endswith("s") and not t.endswith("ss") and len(t) > 3:
            t = t[:-1]
        return t

    def analyze(self, text: str) -> list[str]:
        tokens = self.tokenize(text)
        filtered = [t for t in tokens if t not in self.stopwords]
        return [self.stem(t) for t in filtered]


class Posting:
    """Represents a term's occurrence in a specific document."""

    def __init__(self, doc_id: str, term_freq: int, positions: list[int]) -> None:
        self.doc_id = doc_id
        self.term_freq = term_freq
        self.positions = positions


class InvertedIndex:
    """Core inverted index mapping terms to postings lists."""

    def __init__(self, analyzer: TextAnalyzer | None = None) -> None:
        self.analyzer = analyzer if analyzer is not None else TextAnalyzer()
        self.postings: dict[str, list[Posting]] = {}
        self.doc_lengths: dict[str, int] = {}
        self.doc_sources: dict[str, dict[str, Any]] = {}

    def add_document(self, doc_id: str, text: str, source: dict[str, Any] | None = None) -> None:
        tokens = self.analyzer.analyze(text)
        self.doc_lengths[doc_id] = len(tokens)
        self.doc_sources[doc_id] = dict(source or {"text": text})

        term_positions: dict[str, list[int]] = {}
        for pos, term in enumerate(tokens):
            if term not in term_positions:
                term_positions[term] = []
            term_positions[term].append(pos)

        for term, positions in term_positions.items():
            if term not in self.postings:
                self.postings[term] = []
            self.postings[term].append(
                Posting(doc_id=doc_id, term_freq=len(positions), positions=positions)
            )

    def get_postings(self, term: str) -> list[Posting]:
        stemmed_term = self.analyzer.stem(term.lower())
        return self.postings.get(stemmed_term, [])

    def boolean_and(self, query: str) -> list[str]:
        terms = self.analyzer.analyze(query)
        if not terms:
            return []

        doc_sets: list[set[str]] = []
        for t in terms:
            doc_sets.append({p.doc_id for p in self.get_postings(t)})

        if not doc_sets:
            return []
        return sorted(list(set.intersection(*doc_sets)))

    def boolean_or(self, query: str) -> list[str]:
        terms = self.analyzer.analyze(query)
        if not terms:
            return []

        union_set: set[str] = set()
        for t in terms:
            union_set.update(p.doc_id for p in self.get_postings(t))
        return sorted(list(union_set))


class BM25Ranker:
    """Calculates Okapi BM25 relevance scores."""

    def __init__(self, k1: float = 1.2, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b

    def score(self, index: InvertedIndex, query: str) -> list[tuple[str, float]]:
        query_terms = index.analyzer.analyze(query)
        total_docs = len(index.doc_lengths)
        if total_docs == 0 or not query_terms:
            return []

        avgdl = sum(index.doc_lengths.values()) / total_docs
        doc_scores: dict[str, float] = {}

        for term in set(query_terms):
            postings = index.get_postings(term)
            n_q = len(postings)
            if n_q == 0:
                continue

            # Lucene BM25 IDF
            idf = math.log(1.0 + (total_docs - n_q + 0.5) / (n_q + 0.5))

            for p in postings:
                doc_len = index.doc_lengths[p.doc_id]
                tf = p.term_freq
                num = tf * (self.k1 + 1.0)
                den = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / avgdl))
                term_score = idf * (num / den)
                doc_scores[p.doc_id] = doc_scores.get(p.doc_id, 0.0) + term_score

        return sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)


class DistributedSearchCluster:
    """Simulates an Elasticsearch cluster distributing documents across shards with Query-Then-Fetch."""

    def __init__(self, num_shards: int = 3) -> None:
        self.num_shards = num_shards
        self.shards = [InvertedIndex() for _ in range(num_shards)]
        self.ranker = BM25Ranker()

    def _route(self, doc_id: str) -> int:
        digest = hashlib.md5(doc_id.encode("utf-8")).hexdigest()
        return int(digest, 16) % self.num_shards

    def index(self, doc_id: str, text: str, source: dict[str, Any]) -> None:
        shard_idx = self._route(doc_id)
        self.shards[shard_idx].add_document(doc_id=doc_id, text=text, source=source)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        # Phase 1: Query phase (gather top scores and IDs from each shard)
        candidates: list[tuple[str, float, int]] = []
        for s_idx, shard in enumerate(self.shards):
            results = self.ranker.score(shard, query)
            for doc_id, score in results[:top_k]:
                candidates.append((doc_id, score, s_idx))

        candidates.sort(key=lambda x: x[1], reverse=True)
        winners = candidates[:top_k]

        # Phase 2: Fetch phase (retrieve full _source only for top_k winners)
        hits: list[dict[str, Any]] = []
        for doc_id, score, s_idx in winners:
            source = self.shards[s_idx].doc_sources[doc_id]
            hits.append({
                "_id": doc_id,
                "_score": round(score, 4),
                "_shard": s_idx,
                "_source": source,
            })

        return hits


# ---------------------------------------------------------------------------
# Typeahead / autocomplete
# ---------------------------------------------------------------------------
# Search-as-you-type is a different problem from search, and treating it as
# "search with a wildcard" is the usual mistake. Three reasons:
#
#   1. The latency budget is a keystroke, not a query - roughly 50 ms end to
#      end, because the user types the next character before a slower response
#      lands and the result is discarded anyway.
#   2. The input is a *prefix*, not a term. An inverted index is keyed on whole
#      analyzed terms, so it cannot answer "starts with" without scanning the
#      term dictionary.
#   3. Ranking is by popularity, not relevance. There is no document to be
#      relevant to yet.
#
# `LIKE 'prefix%'` on a relational table gets you a demo; it also gets you a
# full index scan per keystroke. What follows are the two mechanisms real
# engines use, with the trade-off between them measured rather than asserted.


class CompletionTrie:
    """Prefix trie with per-node top-k cached completions.

    This is the teachable form of Lucene's ``FSTCompletionLookup`` - the real
    thing stores an FST (a minimised, shared-suffix automaton) to shrink the
    node count, but the lookup shape is identical: walk the prefix, then read
    the answers cached at the node you land on.

    The important design decision is *where the ranking happens*. A naive trie
    walks the prefix and then enumerates the whole subtree to sort candidates by
    weight, which makes a one-character prefix like "a" the slowest possible
    query - exactly the query users type most. Caching the top-k at every node
    on insert moves that cost to write time, where there is budget for it, and
    makes lookup O(len(prefix) + k) regardless of subtree size.

    ``test_trie_lookup_cost_is_independent_of_subtree_size`` measures that.
    """

    __slots__ = ("children", "top", "weight", "is_terminal")

    def __init__(self) -> None:
        self.children: dict[str, CompletionTrie] = {}
        self.top: list[tuple[int, str]] = []
        self.weight: int = 0
        self.is_terminal: bool = False

    def insert(self, phrase: str, weight: int = 1, top_k: int = 10) -> None:
        """Add a suggestion with a popularity weight.

        Re-inserting an existing phrase replaces its weight rather than adding
        to it, so a nightly rebuild from a query log is idempotent.
        """
        if not phrase:
            raise ValueError("cannot insert an empty suggestion")
        phrase = phrase.lower().strip()

        node = self
        path = [self]
        for ch in phrase:
            node = node.children.setdefault(ch, CompletionTrie())
            path.append(node)
        node.is_terminal = True
        node.weight = weight

        # Refresh the cached top-k on every node along the path. Sorting by
        # (-weight, phrase) makes ties alphabetical, which makes the output
        # deterministic - otherwise the tests are asserting dict ordering.
        for n in path:
            n.top = [t for t in n.top if t[1] != phrase]
            n.top.append((weight, phrase))
            n.top.sort(key=lambda t: (-t[0], t[1]))
            del n.top[top_k:]

    def suggest(self, prefix: str, limit: int = 5) -> list[tuple[str, int]]:
        """Top suggestions for ``prefix``, most popular first.

        Returns ``[]`` for an unknown prefix rather than raising - a user typing
        a novel string is the normal case, not an error.
        """
        node = self
        for ch in prefix.lower().strip():
            node = node.children.get(ch)
            if node is None:
                return []
        return [(phrase, weight) for weight, phrase in node.top[:limit]]

    def node_count(self) -> int:
        """Total nodes, for comparing memory against the edge n-gram approach."""
        return 1 + sum(child.node_count() for child in self.children.values())


class EdgeNGramIndex:
    """The other way: index every prefix as a term at write time.

    This is what Elasticsearch's ``edge_ngram`` tokenizer does. "laptop" is
    indexed as l, la, lap, lapt, lapto, laptop - so a prefix query becomes an
    ordinary exact-term lookup and needs no special traversal at all. It reuses
    the inverted index you already have, which is the whole appeal.

    The cost is write amplification: a term of length L produces L index
    entries. ``test_edge_ngram_write_amplification`` measures it, and the
    trade-off is the point of having both classes here:

    ================  ==========================  ==========================
    .                 CompletionTrie              EdgeNGramIndex
    ================  ==========================  ==========================
    Lookup            O(len(prefix) + k)          O(1) hash lookup
    Index size        one node per shared char    one entry per prefix
    Infix matching    no (prefix only)            no (prefix only)
    Reuses the index  no, separate structure      yes
    Rebuild cost      cheap                       proportional to total chars
    ================  ==========================  ==========================

    Neither handles "matching a word in the *middle*" - for that you need a
    full n-gram tokenizer, and its index grows quadratically in term length,
    which is why nobody enables it on a large corpus without measuring first.
    """

    def __init__(self, min_gram: int = 1, max_gram: int = 20) -> None:
        if min_gram < 1:
            raise ValueError("min_gram must be at least 1")
        if max_gram < min_gram:
            raise ValueError("max_gram must not be below min_gram")
        self.min_gram = min_gram
        self.max_gram = max_gram
        self._index: dict[str, list[tuple[int, str]]] = {}
        self.terms_indexed = 0

    def index(self, phrase: str, weight: int = 1) -> int:
        """Index every prefix of ``phrase``. Returns the number of entries written."""
        phrase = phrase.lower().strip()
        written = 0
        upper = min(len(phrase), self.max_gram)
        for length in range(self.min_gram, upper + 1):
            gram = phrase[:length]
            bucket = self._index.setdefault(gram, [])
            bucket[:] = [b for b in bucket if b[1] != phrase]
            bucket.append((weight, phrase))
            bucket.sort(key=lambda t: (-t[0], t[1]))
            written += 1
        self.terms_indexed += 1
        return written

    def suggest(self, prefix: str, limit: int = 5) -> list[tuple[str, int]]:
        bucket = self._index.get(prefix.lower().strip(), [])
        return [(phrase, weight) for weight, phrase in bucket[:limit]]

    @property
    def entry_count(self) -> int:
        return len(self._index)

    @property
    def write_amplification(self) -> float:
        """Index entries per term indexed. 1.0 would mean no amplification."""
        if not self.terms_indexed:
            return 0.0
        return self.entry_count / self.terms_indexed


def bounded_edit_distance(a: str, b: str, max_distance: int = 2) -> int | None:
    """Levenshtein distance, abandoned once it provably exceeds ``max_distance``.

    Returns ``None`` when the distance is greater than the bound. The bound is
    not an optimisation detail - it is what makes fuzzy suggestion tractable.
    Lucene compiles the query term into a *Levenshtein automaton* and intersects
    it with the term dictionary, which is the same idea done properly: never
    consider a candidate that cannot be within the bound.

    Two cheap early exits do most of the work here:

    * a length difference above the bound rules the pair out with no DP at all;
    * if the best value in a completed row already exceeds the bound, no later
      row can come back down, because each row's minimum is non-decreasing.
    """
    if abs(len(a) - len(b)) > max_distance:
        return None
    if a == b:
        return 0

    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            current.append(
                min(
                    previous[j] + 1,          # deletion
                    current[j - 1] + 1,       # insertion
                    previous[j - 1] + (ca != cb),  # substitution
                )
            )
        if min(current) > max_distance:
            return None
        previous = current

    return previous[-1] if previous[-1] <= max_distance else None


class FuzzySuggester:
    """Typo-tolerant suggestion over a fixed vocabulary.

    Ranks by ``(edit_distance, -weight, phrase)`` - correctness first, then
    popularity. Ranking by popularity first lets a very common term outrank an
    exact match, which users read as the search box ignoring what they typed.

    ``max_distance`` should scale with term length. Lucene's default is 2 for
    terms of 6+ characters, 1 for 3-5, and 0 below that, because at three
    characters an edit distance of 2 matches most of the dictionary. ``for_term``
    applies that rule.
    """

    def __init__(self, vocabulary: dict[str, int] | None = None) -> None:
        self.vocabulary: dict[str, int] = dict(vocabulary or {})

    def add(self, phrase: str, weight: int = 1) -> None:
        self.vocabulary[phrase.lower().strip()] = weight

    @staticmethod
    def for_term(term: str) -> int:
        """Lucene's length-scaled fuzziness (the ``AUTO`` setting)."""
        if len(term) < 3:
            return 0
        return 1 if len(term) < 6 else 2

    def suggest(
        self, term: str, limit: int = 5, max_distance: int | None = None
    ) -> list[tuple[str, int, int]]:
        """Return ``(phrase, weight, distance)`` triples, closest match first."""
        term = term.lower().strip()
        bound = self.for_term(term) if max_distance is None else max_distance

        scored: list[tuple[int, int, str]] = []
        for phrase, weight in self.vocabulary.items():
            distance = bounded_edit_distance(term, phrase, bound)
            if distance is not None:
                scored.append((distance, -weight, phrase))

        scored.sort()
        return [(phrase, -neg_weight, dist) for dist, neg_weight, phrase in scored[:limit]]
