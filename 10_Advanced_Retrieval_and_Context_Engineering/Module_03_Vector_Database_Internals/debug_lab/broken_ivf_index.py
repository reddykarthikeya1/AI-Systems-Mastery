# Debug Lab: IVF-Style Vector Index Searches the Wrong Partition
# Course 10 - Module 03 Vector Database Internals

import math

CENTROIDS = {
    "bucket_a": (0.0, 0.0),
    "bucket_b": (10.0, 10.0),
}


def l2_distance(u, v):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(u, v)))


def nearest_centroid_for_insert(vector):
    # Insertion correctly routes each vector to the bucket of its CLOSEST
    # centroid, mirroring how an IVF index clusters vectors at build time.
    return min(CENTROIDS, key=lambda name: l2_distance(vector, CENTROIDS[name]))


def nearest_centroid_for_query(vector):
    # Query-time partition lookup should also pick the CLOSEST centroid, so
    # search only scans the partition that could actually contain the
    # nearest neighbor.
    return max(CENTROIDS, key=lambda name: l2_distance(vector, CENTROIDS[name]))


class IVFIndex:
    def __init__(self):
        self.buckets = {name: [] for name in CENTROIDS}

    def insert(self, vec_id, vector):
        bucket = nearest_centroid_for_insert(vector)
        self.buckets[bucket].append((vec_id, vector))

    def search(self, query_vector, top_k=1):
        bucket = nearest_centroid_for_query(query_vector)
        candidates = self.buckets[bucket]
        scored = [(vec_id, l2_distance(query_vector, v)) for vec_id, v in candidates]
        scored.sort(key=lambda pair: pair[1])
        return bucket, scored[:top_k]


if __name__ == "__main__":
    index = IVFIndex()
    # 3 vectors cluster tightly near (0, 0) -> bucket_a; 1 outlier sits near
    # (10, 10) -> bucket_b.
    index.insert("doc_1", (0.5, 0.2))
    index.insert("doc_2", (0.1, 0.4))
    index.insert("doc_3", (0.3, 0.1))
    index.insert("doc_4", (9.8, 10.1))

    # Query is also right next to (0, 0), so the true nearest neighbor
    # (doc_1/doc_2/doc_3, all within ~0.5 distance) lives in bucket_a.
    query = (0.2, 0.3)

    searched_bucket, results = index.search(query, top_k=1)

    print(f"Centroids: {CENTROIDS}")
    print(f"Stored vectors all cluster near (0, 0), so they were all inserted "
          f"into: {[nearest_centroid_for_insert(v) for v in [(0.5,0.2),(0.1,0.4),(0.3,0.1)]]}")
    print(f"Query vector {query} is also near (0, 0).")
    print(f"Expected: search should scan 'bucket_a' (closest centroid to the query) "
          f"and return a very close match (distance well under 1.0).")
    print(f"Actual bucket searched: {searched_bucket!r}")
    print(f"Actual top-1 result: {results}")
