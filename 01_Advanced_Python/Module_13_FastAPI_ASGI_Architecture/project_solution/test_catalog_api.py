"""Unit tests for the Product Catalog Microservice API."""

from __future__ import annotations

from catalog_api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "HEALTHY", "service": "product-catalog"}


def test_list_products_and_filter() -> None:
    # All products
    res = client.get("/products")
    assert res.status_code == 200
    assert len(res.json()) >= 3

    # Filter by category
    res_filtered = client.get("/products?category=kitchen")
    assert res_filtered.status_code == 200
    data = res_filtered.json()
    assert len(data) == 1
    assert data[0]["name"] == "Coffee Mug"


def test_get_product_by_id_and_404() -> None:
    res = client.get("/products/1")
    assert res.status_code == 200
    assert res.json()["name"] == "Mechanical Keyboard"

    res_404 = client.get("/products/9999")
    assert res_404.status_code == 404


def test_create_and_delete_product() -> None:
    payload = {
        "name": "Noise Cancelling Headphones",
        "category": "electronics",
        "price": 199.99,
        "in_stock": True,
    }
    res_create = client.post("/products", json=payload)
    assert res_create.status_code == 201
    created_id = res_create.json()["id"]

    # Verify created
    res_get = client.get(f"/products/{created_id}")
    assert res_get.status_code == 200
    assert res_get.json()["name"] == "Noise Cancelling Headphones"

    # Delete
    res_del = client.delete(f"/products/{created_id}")
    assert res_del.status_code == 204

    # Verify gone
    res_check = client.get(f"/products/{created_id}")
    assert res_check.status_code == 404


def test_create_product_missing_required_field() -> None:
    """Test creating product with missing price returns 422 Unprocessable Entity."""
    payload = {"name": "Incomplete Product", "category": "books"}
    res = client.post("/products", json=payload)
    assert res.status_code == 422


def test_create_product_negative_price() -> None:
    """Test creating product with negative price returns 422."""
    payload = {"name": "Negative Price Item", "category": "tools", "price": -15.0}
    res = client.post("/products", json=payload)
    assert res.status_code == 422


def test_create_product_empty_name() -> None:
    """Test creating product with empty string name returns 422."""
    payload = {"name": "", "category": "tools", "price": 10.0}
    res = client.post("/products", json=payload)
    assert res.status_code == 422


def test_delete_nonexistent_product_returns_404() -> None:
    """Test deleting non-existent product returns 404."""
    res = client.delete("/products/99999")
    assert res.status_code == 404


def test_filter_products_by_nonexistent_category() -> None:
    """Test filtering by category that matches no items returns empty list."""
    res = client.get("/products?category=spacecraft")
    assert res.status_code == 200
    assert res.json() == []


def test_filter_products_by_price_range() -> None:
    """Test filtering products using min_price and max_price query parameters."""
    res = client.get("/products?min_price=20.0&max_price=100.0")
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["name"] == "Ergonomic Mouse"


def test_openapi_schema_accessible() -> None:
    """Test OpenAPI schema endpoint returns valid OpenAPI JSON."""
    res = client.get("/openapi.json")
    assert res.status_code == 200
    schema = res.json()
    assert "openapi" in schema
    assert "/products" in schema["paths"]
