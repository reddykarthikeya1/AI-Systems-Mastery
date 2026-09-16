# Module_13_FastAPI_ASGI_Architecture: Project Implementation Guide

**Deliverable:** a high-performance catalog microservice built with FastAPI, Pydantic, OpenAPI documentation, and query filtering.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_catalog_api.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — FastAPI Application & Health Endpoint
Initialize `FastAPI` instance and create `GET /health` returning service health status.

### Step 2 — Pydantic Schemas
Define `ProductCreate` with positive price validation and `ProductResponse` with auto-assigned IDs.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_catalog_api.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — CRUD Endpoints
Implement `POST /products`, `GET /products/{product_id}`, and `DELETE /products/{product_id}` returning proper status codes (201, 204, 404).

### Step 4 — Query Filtering
Implement `GET /products` with optional `category`, `min_price`, and `max_price` query parameter filtering.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/catalog_api.py`, change `DELETE /products/{id}` to return HTTP 200 instead of HTTP 204.
Run:
```bash
pytest ../project_solution/test_catalog_api.py -k test_create_and_delete_product -v
```
Watch the test fail on `assert res.status_code == 204`, then restore HTTP 204 No Content.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_catalog_api.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Pagination Response Envelope:** Implement `Page[ProductResponse]` with `total`, `page`, `size`, and `has_more`.
2. **ETag Caching:** Generate ETags based on product hash and return `304 Not Modified` on matching `If-None-Match`.
3. **Bulk Product Ingest:** Add `POST /products/bulk` validating batches of up to 1,000 items.
4. **Structured Error Logging:** Intercept unhandled exceptions in custom exception handlers.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_health_check` | Proves health check endpoint returns 200 OK |
| `test_list_products_and_filter` | Proves category and price range query parameter filtering |
| `test_get_product_by_id_and_404` | Proves single product retrieval and 404 on missing item |
| `test_create_and_delete_product` | Proves full product lifecycle from creation to deletion |
| `test_create_product_negative_price` | Proves Pydantic rejects negative product prices with 422 |

---

## 🎓 You have mastered this module when you can…

- [ ] Explain the ASGI specification and how FastAPI interfaces with Uvicorn
- [ ] Design clean RESTful APIs using standard HTTP verbs and status codes (200, 201, 204, 404, 422)
- [ ] Use Pydantic models for automatic request parsing and response serialization
- [ ] Implement query parameter filtering and validation using FastAPI Query()
- [ ] Raise HTTPException with structured error payloads
- [ ] Test FastAPI applications synchronously and asynchronously using TestClient
- [ ] Avoid blocking synchronous calls in async def route handlers
