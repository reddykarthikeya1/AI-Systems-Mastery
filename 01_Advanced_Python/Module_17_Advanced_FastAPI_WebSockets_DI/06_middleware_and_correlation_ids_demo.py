#!/usr/bin/env python3
"""Module 15: Custom ASGI Middleware & Correlation ID Demonstration.

This script demonstrates injecting correlation tracking IDs and processing time
headers via FastAPI HTTP middleware.
"""

from __future__ import annotations

import time
import uuid

from fastapi import FastAPI, Request, Response
from starlette.testclient import TestClient

app = FastAPI()


@app.middleware("http")
async def correlation_and_timing_middleware(request: Request, call_next) -> Response:
    # 1. Extract or generate unique correlation trace ID
    corr_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

    start = time.perf_counter()
    response: Response = await call_next(request)
    duration = time.perf_counter() - start

    # 2. Inject tracking headers into outbound response
    response.headers["X-Correlation-ID"] = corr_id
    response.headers["X-Process-Time"] = f"{duration * 1000:.2f}ms"
    return response


@app.get("/ping")
def ping():
    return {"message": "pong"}


def main() -> None:
    print("=" * 60)
    print("  FastAPI Middleware & Correlation Tracking Demo")
    print("=" * 60)

    client = TestClient(app)
    custom_trace_id = "trace-client-12345"

    res = client.get("/ping", headers={"X-Correlation-ID": custom_trace_id})
    print(f"Status Code        : {res.status_code}")
    print(f"X-Correlation-ID   : {res.headers.get('X-Correlation-ID')}")
    print(f"X-Process-Time     : {res.headers.get('X-Process-Time')}")


if __name__ == "__main__":
    main()
