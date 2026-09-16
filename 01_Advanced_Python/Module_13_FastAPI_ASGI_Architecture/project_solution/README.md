# Design Rationale: Product Catalog Microservice with FastAPI & ASGI

## Architectural Overview
A production-ready e-commerce catalog API demonstrating raw ASGI packet interception, FastAPI router modularity, automated Pydantic validation, and OpenAPI documentation.

## Key Design Decisions
1. **Asynchronous Non-Blocking Handlers:** Endpoints use `async def` paired with non-blocking I/O, allowing thousands of concurrent client connections per Uvicorn worker process.
2. **Pydantic V2 Request-Response Contracts:** Rust-accelerated schema validation enforces input boundaries and automatically strips internal entity fields from outgoing HTTP responses.
3. **Lifespan Context Management:** Database connection pools and shared HTTP clients are managed using the `@asynccontextmanager` lifespan protocol, guaranteeing clean startup and shutdown.

## Rejected Alternatives
1. **Synchronous WSGI Architecture (Flask/Django Sync):**
   - *Reason for Rejection:* Standard WSGI requires a dedicated OS thread or worker per connection, consuming tens of gigabytes of RAM under concurrent traffic loads.
2. **Parsing Raw Request JSON Manually (`request.json()`):**
   - *Reason for Rejection:* Manual parsing bypasses Pydantic schema validation, loses automatic OpenAPI documentation generation, and introduces boilerplate type conversion.

## Invariants & Guarantees
- All request parameters validated before reaching business logic handlers.
- Lifespan resources are cleanly closed on SIGINT / SIGTERM signals.

## Verification
```bash
pytest test_catalog_api.py -v
```
