# Debug Lab: Semantic Search Picks the Wrong Nearest Neighbor
# Course 06 - Module 12 Bonus Lessons

import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def similarity(query, candidate):
    return dot(query, candidate)


def most_similar(query, candidates):
    scored = [(name, similarity(query, vec)) for name, vec in candidates.items()]
    return sorted(scored, key=lambda t: t[1], reverse=True)


if __name__ == "__main__":
    query = [1.0, 0.0]  # points purely in the "cat" direction

    candidates = {
        "closely_related_short": [0.9, 0.1],    # nearly same direction, small magnitude
        "unrelated_long_document": [3.0, 5.0],   # very different direction, large magnitude
        "opposite_direction": [-1.0, 0.0],
    }

    ranking = most_similar(query, candidates)

    print(f"Query embedding: {query}")
    print("Ranked nearest neighbors (highest score first):")
    for name, score in ranking:
        print(f"  {name}: score={score:.3f}")
    print(f"Top match chosen: '{ranking[0][0]}'")
