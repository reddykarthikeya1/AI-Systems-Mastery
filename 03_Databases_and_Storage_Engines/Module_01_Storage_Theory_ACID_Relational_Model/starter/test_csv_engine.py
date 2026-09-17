"""Automated pytest test suite for Module 01 Transactional CSV Engine."""

import shutil
import pytest

from csv_engine import TransactionalCSVEngine, ValidationError, TransactionError


@pytest.fixture
def temp_db_dir(tmp_path):
    """Provides a temporary sandbox directory for database file testing."""
    yield tmp_path
    shutil.rmtree(tmp_path, ignore_errors=True)


def test_table_creation_and_empty_select(temp_db_dir):
    schema = {"id": int, "name": str, "balance": float}
    engine = TransactionalCSVEngine("accounts", schema, base_dir=temp_db_dir)
    rows = engine.select_all()
    assert rows == []


def test_transaction_commit_and_select(temp_db_dir):
    schema = {"id": int, "name": str, "balance": float}
    engine = TransactionalCSVEngine("accounts", schema, base_dir=temp_db_dir)

    engine.begin()
    engine.insert({"id": 1, "name": "Alice", "balance": 500.0})
    engine.insert({"id": 2, "name": "Bob", "balance": 750.50})
    engine.commit()

    rows = engine.select_all()
    assert len(rows) == 2
    assert rows[0] == {"id": 1, "name": "Alice", "balance": 500.0}
    assert rows[1] == {"id": 2, "name": "Bob", "balance": 750.50}


def test_transaction_rollback_preserves_atomicity(temp_db_dir):
    schema = {"id": int, "name": str, "balance": float}
    engine = TransactionalCSVEngine("accounts", schema, base_dir=temp_db_dir)

    # Committed first transaction
    engine.begin()
    engine.insert({"id": 1, "name": "Alice", "balance": 500.0})
    engine.commit()

    # Aborted second transaction
    engine.begin()
    engine.insert({"id": 2, "name": "Bob", "balance": 100.0})
    engine.rollback()

    rows = engine.select_all()
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"


def test_schema_validation_rejects_bad_data(temp_db_dir):
    schema = {"id": int, "name": str, "balance": float}
    engine = TransactionalCSVEngine("accounts", schema, base_dir=temp_db_dir)

    engine.begin()
    with pytest.raises(ValidationError):
        # Invalid float for balance
        engine.insert({"id": 1, "name": "Alice", "balance": "not-a-number"})

    with pytest.raises(ValidationError):
        # Missing column
        engine.insert({"id": 2, "name": "Bob"})


def test_insert_outside_transaction_raises_error(temp_db_dir):
    schema = {"id": int, "name": str, "balance": float}
    engine = TransactionalCSVEngine("accounts", schema, base_dir=temp_db_dir)

    with pytest.raises(TransactionError):
        engine.insert({"id": 1, "name": "Alice", "balance": 100.0})
