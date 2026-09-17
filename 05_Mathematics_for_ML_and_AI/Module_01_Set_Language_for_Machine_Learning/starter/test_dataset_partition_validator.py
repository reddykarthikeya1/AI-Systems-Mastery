"""Unit tests for DatasetPartitionValidator."""
from __future__ import annotations

import pytest
from dataset_partition_validator import DatasetPartitionValidator


def test_valid_partition():
    full = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    train = {1, 2, 3, 4, 5, 6}
    val = {7, 8}
    test = {9, 10}
    assert DatasetPartitionValidator.is_valid_partition(train, val, test, full)


def test_data_leakage_detected():
    full = {1, 2, 3, 4, 5}
    train = {1, 2, 3}
    val = {4}
    test = {3, 5}  # 3 is leaked!
    assert not DatasetPartitionValidator.is_valid_partition(train, val, test, full)
    assert DatasetPartitionValidator.find_data_leakage(train, test) == {3}


def test_non_exhaustive_partition():
    full = {1, 2, 3, 4, 5}
    train = {1, 2}
    val = {3}
    test = {4}  # element 5 is missing!
    assert not DatasetPartitionValidator.is_valid_partition(train, val, test, full)


def test_jaccard_similarity():
    s1 = {"deep", "learning", "model"}
    s2 = {"deep", "neural", "network"}
    assert pytest.approx(DatasetPartitionValidator.jaccard_similarity(s1, s2)) == 0.2
    assert DatasetPartitionValidator.jaccard_similarity(set(), set()) == 1.0
