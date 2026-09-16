#!/usr/bin/env python3
"""Module 11: Raw ASGI (Asynchronous Server Gateway Interface) Specification Demo.

This script demonstrates building a raw ASGI application callable without
frameworks, showing how Uvicorn interacts with Python async web code.
"""

from __future__ import annotations

import json


async def raw_asgi_app(scope: dict, receive: callable, send: callable) -> None:
    """The fundamental 3-argument ASGI specification interface."""
    assert scope["type"] == "http"

    response_body = json.dumps({
        "engine": "Raw ASGI Interface",
        "path": scope["path"],
        "method": scope["method"],
    }).encode("utf-8")

    # Step 1: Send HTTP Response start frame
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"application/json"],
            [b"content-length", str(len(response_body)).encode("utf-8")],
        ],
    })

    # Step 2: Send HTTP Response body frame
    await send({
        "type": "http.response.body",
        "body": response_body,
    })


def main() -> None:
    print("=" * 60)
    print("  Raw ASGI Callable Specification Demonstration")
    print("=" * 60)
    print("ASGI applications are coroutines accepting (scope, receive, send).")
    print("FastAPI builds high-level routing and Pydantic validation on top of this interface!")


if __name__ == "__main__":
    main()
