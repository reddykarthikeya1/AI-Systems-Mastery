#!/usr/bin/env python3
"""Product Catalog Microservice REST API.

Module 11 (FastAPI & ASGI Architecture) Turnkey Project Implementation.
Demonstrates FastAPI CRUD routing, query filtering, and Pydantic validation.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Product Catalog Microservice",
    description="High-performance catalog microservice built with FastAPI & Pydantic",
    version="1.0.0",
)


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0.0)
    in_stock: bool = True


class ProductResponse(ProductCreate):
    id: int


# In-memory database repository
products_db: dict[int, ProductResponse] = {
    1: ProductResponse(id=1, name="Mechanical Keyboard", category="electronics", price=129.99, in_stock=True),
    2: ProductResponse(id=2, name="Ergonomic Mouse", category="electronics", price=69.50, in_stock=True),
    3: ProductResponse(id=3, name="Coffee Mug", category="kitchen", price=14.99, in_stock=False),
}
id_counter = 3


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, str]:
    return {"status": "HEALTHY", "service": "product-catalog"}


@app.get("/products", response_model=list[ProductResponse])
def list_products(
    category: str | None = None,
    min_price: float | None = Query(None, ge=0.0),
    max_price: float | None = Query(None, ge=0.0),
) -> list[ProductResponse]:
    results = list(products_db.values())

    if category:
        results = [p for p in results if p.category.lower() == category.lower()]
    if min_price is not None:
        results = [p for p in results if p.price >= min_price]
    if max_price is not None:
        results = [p for p in results if p.price <= max_price]

    return results


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int) -> ProductResponse:
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    return products_db[product_id]


@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate) -> ProductResponse:
    global id_counter
    id_counter += 1
    new_product = ProductResponse(id=id_counter, **payload.model_dump())
    products_db[id_counter] = new_product
    return new_product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int) -> None:
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    del products_db[product_id]
