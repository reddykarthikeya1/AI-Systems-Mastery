"""Starter template for DatasetPartitionValidator."""
from __future__ import annotations

from typing import Any


class DatasetPartitionValidator:
    """Mathematical set validator for machine learning dataset partitions."""

    @staticmethod
    def is_valid_partition(
        train: set[Any], val: set[Any], test: set[Any], full_dataset: set[Any]
    ) -> bool:
        """Return True if train, val, test form a strict pairwise-disjoint partition."""
        raise NotImplementedError

    @staticmethod
    def find_data_leakage(train: set[Any], test: set[Any]) -> set[Any]:
        """Return overlapping IDs that represent data contamination between train and test."""
        raise NotImplementedError

    @staticmethod
    def jaccard_similarity(set_a: set[Any], set_b: set[Any]) -> float:
        """Compute Jaccard similarity coefficient: |A intersect B| / |A union B|."""
        raise NotImplementedError
