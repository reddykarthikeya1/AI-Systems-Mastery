"""STARTER - Module 13: FastAPI ASGI Architecture

Product Catalog Microservice REST API.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_catalog_api.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/catalog_api.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
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

products_db: dict[int, ProductResponse] = {
    1: ProductResponse(id=1, name="Mechanical Keyboard", category="electronics", price=129.99, in_stock=True),
    2: ProductResponse(id=2, name="Ergonomic Mouse", category="electronics", price=69.50, in_stock=True),
    3: ProductResponse(id=3, name="Coffee Mug", category="kitchen", price=14.99, in_stock=False),
}
id_counter = 3

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, str]:
    # [Tier 2] Algorithm: Validate input arguments against constraints and raise
    #   specific exception.
    # HINTS:
    #  - Check boundary conditions (e.g. non-empty string, positive integer,
    #   range).
    #  - Raise ValueError or TypeError with actionable descriptive messages.
    # GRADES: test_health_check
    # WARNING: Never swallow validation errors or return None instead of
    #   raising.
    raise NotImplementedError("Module 13: implement health_check()")


@app.get("/products", response_model=list[ProductResponse])
def list_products(
    category: str | None = None,
    min_price: float | None = Query(None, ge=0.0),
    max_price: float | None = Query(None, ge=0.0),
) -> list[ProductResponse]:
    # [Tier 2] Algorithm: Implement list_products adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_list_products_and_filter
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 13: implement list_products()")


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int) -> ProductResponse:
    # [Tier 1] Algorithm: Implement get_product adhering to the contract defined
    #   in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_get_product_by_id_and_404
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 13: implement get_product()")


@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate) -> ProductResponse:
    # [Tier 2] Algorithm: Implement create_product adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_create_product_missing_required_field
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 13: implement create_product()")


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int) -> None:
    # [Tier 2] Algorithm: Implement delete_product adhering to the contract
    #   defined in docstring.
    # HINTS:
    #  - Check preconditions on input arguments before mutating internal state.
    #  - Return expected data shape matching the type annotations.
    # GRADES: test_create_and_delete_product
    # WARNING: Do not alter the function signature or return incompatible types.
    raise NotImplementedError("Module 13: implement delete_product()")
