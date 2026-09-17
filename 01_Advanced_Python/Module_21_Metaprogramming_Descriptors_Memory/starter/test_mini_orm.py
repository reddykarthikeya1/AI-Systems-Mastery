"""Unit tests for the Zero-Dependency Declarative Mini-ORM."""

from __future__ import annotations

import time

import pytest
from mini_orm import FloatField, IntegerField, Model, StringField


class Product(Model, table_name="store_products"):
    id = IntegerField(primary_key=True)
    title = StringField(max_length=40, nullable=False)
    price = FloatField(nullable=False)


class AutoTableItem(Model):
    id = IntegerField(primary_key=True)
    description = StringField(max_length=100, nullable=True)


def test_schema_generation() -> None:
    sql = Product.get_create_table_sql()
    assert "CREATE TABLE store_products" in sql
    assert "id INTEGER PRIMARY KEY" in sql
    assert "title VARCHAR(40) NOT NULL" in sql
    assert "price REAL NOT NULL" in sql


def test_instance_creation_and_insert_sql() -> None:
    prod = Product(id=10, title="Mechanical Keyboard", price=129.99)
    assert prod.title == "Mechanical Keyboard"
    assert prod.price == 129.99

    insert_sql = prod.as_insert_sql()
    assert "INSERT INTO store_products (id, title, price)" in insert_sql
    assert "10, 'Mechanical Keyboard', 129.99" in insert_sql


def test_validation_constraints() -> None:
    prod = Product(id=1, title="Valid", price=10.0)

    # Invalid type for IntegerField
    with pytest.raises(TypeError, match="must be an integer"):
        prod.id = "not-an-int"

    # String exceeding max_length
    with pytest.raises(TypeError, match="up to 40 characters"):
        prod.title = "A" * 50


def test_missing_required_field_raises_value_error() -> None:
    """Test initializing model missing a required non-nullable field raises ValueError."""
    with pytest.raises(ValueError, match="Missing required field: 'title'"):
        Product(id=1, price=50.0)


def test_nullable_field_assignment_none_allowed() -> None:
    """Test assigning None to a nullable field is permitted."""
    item = AutoTableItem(id=1, description=None)
    assert item.description is None


def test_non_nullable_assignment_none_raises_value_error() -> None:
    """Test setting None on a non-nullable field raises ValueError."""
    prod = Product(id=1, title="Widget", price=15.0)
    with pytest.raises(ValueError, match="cannot be NULL"):
        prod.title = None


def test_descriptor_class_access_returns_descriptor() -> None:
    """Test accessing descriptor on class returns descriptor object itself."""
    desc = Product.title
    assert isinstance(desc, StringField)
    assert desc.name == "title"


def test_model_to_dict_method() -> None:
    """Test to_dict produces key-value mapping of all defined fields."""
    prod = Product(id=5, title="Monitor", price=299.99)
    d = prod.to_dict()
    assert d == {"id": 5, "title": "Monitor", "price": 299.99}


def test_default_table_name_inference() -> None:
    """Test when table_name is omitted, class name plural is inferred."""
    assert AutoTableItem._table_name == "autotableitems"


def test_float_field_rejects_string_type() -> None:
    """Test assigning non-numeric string to FloatField raises TypeError."""
    prod = Product(id=1, title="Gadget", price=19.99)
    with pytest.raises(TypeError, match="must be a float"):
        prod.price = "free"


@pytest.mark.perf
def test_perf_model_instantiation_throughput() -> None:
    """Benchmark: 20,000 model instantiations with descriptor validation execute quickly."""
    start = time.perf_counter()
    for i in range(20_000):
        Product(id=i, title="Item", price=19.99)
    duration = time.perf_counter() - start
    assert duration < 1.5, f"Instantiation took too long: {duration:.3f}s"
