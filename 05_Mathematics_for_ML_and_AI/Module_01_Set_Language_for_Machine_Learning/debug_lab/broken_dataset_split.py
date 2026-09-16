"""A dataset splitter with three planted defects.

It runs to completion, raises nothing and exits 0. Every number it prints is
plausible. Three of them are wrong.
"""
from __future__ import annotations


def split(rows, train_frac=0.6, val_frac=0.2):
    n = len(rows)
    train_end = int(n * train_frac)
    val_end = int(n * (train_frac + val_frac))
    train = rows[:train_end]
    validation = rows[train_end:val_end]
    test = rows[val_end:]
    return train, validation, test


def deduplicate(rows):
    seen = []
    out = []
    for row in rows:
        if row not in seen:
            seen.append(row)
            out.append(row)
    return out


def group_split(rows, groups, train_frac=0.7):
    """Rows sharing a group (same patient, same user) must not be split apart."""
    cut = int(len(rows) * train_frac)
    return rows[:cut], rows[cut:]


def main():
    print("=" * 66)
    print("DATASET SPLITTER - integrity report")
    print("=" * 66)

    print()
    print("[1] Partition sizes and coverage")
    rows = list(range(100))
    train, validation, test = split(rows)
    print(f"    rows in: {len(rows)}")
    print(f"    train={len(train)}  validation={len(validation)}  test={len(test)}")
    print(f"    total out: {len(train) + len(validation) + len(test)}")
    covered = set(train) | set(validation) | set(test)
    print(f"    distinct rows covered: {len(covered)}")
    print(f"    overlap train&test: {len(set(train) & set(test))}")

    print()
    print("[2] Deduplicating before the split")
    raw = [i % 500 for i in range(4000)]
    unique = deduplicate(raw)
    print(f"    raw rows: {len(raw)}  distinct values present: {len(set(raw))}")
    print(f"    deduplicate() returned: {len(unique)}")

    print()
    print("[3] Grouped split - rows from one patient must stay together")
    patients = [f"p{i // 3}" for i in range(30)]
    records = list(range(30))
    tr, te = group_split(records, patients)
    train_patients = {patients[i] for i in tr}
    test_patients = {patients[i] for i in te}
    shared = train_patients & test_patients
    print(f"    patients: {len(set(patients))}")
    print(f"    patients appearing in BOTH train and test: {len(shared)} {sorted(shared)}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()
