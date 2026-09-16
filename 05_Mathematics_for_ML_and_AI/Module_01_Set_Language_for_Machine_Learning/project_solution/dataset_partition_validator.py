"""Production solution for DatasetPartitionValidator."""
from __future__ import annotations

from typing import Any


class DatasetPartitionValidator:
    """Mathematical set validator for machine learning dataset partitions."""

    @staticmethod
    def is_valid_partition(
        train: set[Any], val: set[Any], test: set[Any], full_dataset: set[Any]
    ) -> bool:
        # Check mutual disjointness
        if (train & val) or (train & test) or (val & test):
            return False
        # Check exhaustive union
        return (train | val | test) == full_dataset

    @staticmethod
    def find_data_leakage(train: set[Any], test: set[Any]) -> set[Any]:
        return train & test

    @staticmethod
    def jaccard_similarity(set_a: set[Any], set_b: set[Any]) -> float:
        if not set_a and not set_b:
            return 1.0
        union_len = len(set_a | set_b)
        if union_len == 0:
            return 1.0
        return len(set_a & set_b) / union_len
