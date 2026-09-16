"""Module 19: Inverted Index & Okapi BM25 Relevance Scoring Demo.

Demonstrates:
1. Text analysis pipeline (tokenization, stopword removal, stemming).
2. Inverted index postings list construction.
3. Okapi BM25 relevance score calculation.
"""

from __future__ import annotations

import math
import re


def analyze_text(text: str) -> list[str]:
    """Simple text analysis pipeline: lowercase, regex word extraction, basic stopword filter."""
    stopwords = {"the", "a", "an", "is", "in", "and", "or", "for", "to", "of", "with"}
    tokens = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    # Simple stemmer for common suffixes (s, ing, ed)
    stemmed = []
    for t in tokens:
        if t in stopwords:
            continue
        if t.endswith("ing") and len(t) > 5:
            t = t[:-3]
        elif t.endswith("ed") and len(t) > 4:
            t = t[:-2]
        elif t.endswith("s") and not t.endswith("ss") and len(t) > 3:
            t = t[:-1]
        stemmed.append(t)
    return stemmed


def demo_inverted_index() -> None:
    print("=" * 75)
    print("    1. INVERTED INDEX & POSTINGS LIST CONSTRUCTION")
    print("=" * 75)

    docs = {
        "doc_1": "Distributed databases use consensus algorithms like Raft and Paxos.",
        "doc_2": "Relational databases enforce ACID transactions with write-ahead logs.",
        "doc_3": "Distributed consensus in databases requires leader election.",
    }

    inverted_index: dict[str, list[str]] = {}
    for doc_id, text in docs.items():
        tokens = analyze_text(text)
        for token in set(tokens):
            if token not in inverted_index:
                inverted_index[token] = []
            inverted_index[token].append(doc_id)

    print("Corpus Documents:")
    for d_id, text in docs.items():
        print(f"  [{d_id}] {text}")

    print("\nInverted Index (Term -> Postings):")
    sample_terms = ["databas", "distribut", "consensu", "acid", "raft"]
    for t in sample_terms:
        print(f"  '{t:<12}' -> {inverted_index.get(t, [])}")


def demo_bm25_scoring() -> None:
    print("\n" + "=" * 75)
    print("    2. OKAPI BM25 RELEVANCE SCORING")
    print("=" * 75)

    docs = {
        "doc_short": "Raft is a distributed consensus algorithm for replicated logs.",
        "doc_long": "This very long textbook chapter covers databases, storage engines, distributed network nodes, hardware fault tolerance, and briefly mentions consensus once at the end.",
    }

    query = "distributed consensus"
    query_tokens = analyze_text(query)

    corpus_tokens = {doc_id: analyze_text(text) for doc_id, text in docs.items()}
    total_docs = len(docs)
    avgdl = sum(len(toks) for toks in corpus_tokens.values()) / total_docs

    # Parameters
    k1 = 1.2
    b = 0.75

    print(f"Query : '{query}' -> Tokens: {query_tokens}")
    print(f"Corpus Average Document Length (avgdl): {avgdl:.1f} terms\n")

    for doc_id, tokens in corpus_tokens.items():
        doc_len = len(tokens)
        score = 0.0

        for q in query_tokens:
            # Count docs containing term q
            n_q = sum(1 for d_toks in corpus_tokens.values() if q in d_toks)
            # Lucene BM25 IDF
            idf = math.log(1.0 + (total_docs - n_q + 0.5) / (n_q + 0.5))

            # Term frequency in this document
            tf = tokens.count(q)

            # BM25 term score
            numerator = tf * (k1 + 1.0)
            denominator = tf + k1 * (1.0 - b + b * (doc_len / avgdl))
            term_score = idf * (numerator / denominator)
            score += term_score

        print(f"  [{doc_id:<10}] Length: {doc_len:>2} terms | BM25 Score: {score:.4f}")

    print("\nAnalysis: 'doc_short' receives a far higher score than 'doc_long' because BM25")
    print("normalizes for document length (b=0.75) and rewards high term density!")


def main() -> None:
    demo_inverted_index()
    demo_bm25_scoring()


if __name__ == "__main__":
    main()
