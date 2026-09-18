# Debug Lab: Suspiciously Perfect Held-Out Evaluation
# Course 06 - Module 02 Core AI Intuitions

import random


def make_dataset(n=200):
    rng = random.Random(7)
    data = [rng.uniform(0, 10) for _ in range(n)]
    labels = [round(x) % 2 for x in data]
    return data, labels


def train_test_split(data, labels, train_frac=0.8, seed=42):
    n = len(data)
    indices = list(range(n))
    random.Random(seed).shuffle(indices)
    split = int(n * train_frac)
    train_idx = indices[:split]
    # the held-out set is meant to be the remainder of `indices`, sampled independently instead
    test_idx = random.Random(seed + 1).sample(range(n), n - split)

    train_x = [data[i] for i in train_idx]
    train_y = [labels[i] for i in train_idx]
    test_x = [data[i] for i in test_idx]
    test_y = [labels[i] for i in test_idx]
    overlap = set(train_idx) & set(test_idx)
    return train_x, train_y, test_x, test_y, overlap


def memorizer_predict(train_x, train_y, query):
    table = dict(zip(train_x, train_y))
    if query in table:
        return table[query]
    majority = 1 if sum(train_y) >= len(train_y) / 2 else 0
    return majority


def evaluate(train_x, train_y, test_x, test_y):
    correct = sum(
        1 for qx, qy in zip(test_x, test_y)
        if memorizer_predict(train_x, train_y, qx) == qy
    )
    return correct / len(test_x)


if __name__ == "__main__":
    data, labels = make_dataset()
    train_x, train_y, test_x, test_y, overlap = train_test_split(data, labels)

    accuracy = evaluate(train_x, train_y, test_x, test_y)
    majority_baseline = max(sum(train_y), len(train_y) - sum(train_y)) / len(train_y)

    print(f"Train set size: {len(train_x)}, Test set size: {len(test_x)}")
    print(f"Indices present in BOTH train and test: {len(overlap)}")
    print(f"Majority-class baseline accuracy: {majority_baseline * 100:.1f}%")
    print(f"Reported held-out accuracy: {accuracy * 100:.1f}%")
