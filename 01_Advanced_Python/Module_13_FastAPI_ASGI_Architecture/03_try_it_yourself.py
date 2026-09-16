"""
Module 13: Lightweight In-Memory HTTP/API Router Simulator
Run: python try_it_yourself.py
"""

import json


class MiniRouter:
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self.routes[("GET", path)] = func
            return func
        return decorator

    def handle_request(self, method, path):
        handler = self.routes.get((method, path))
        if handler:
            data = handler()
            return 200, json.dumps(data)
        return 404, json.dumps({"error": "Route Not Found"})


app = MiniRouter()


@app.get("/")
def read_root():
    return {"status": "online", "version": "1.0"}


@app.get("/api/products")
def list_products():
    return [{"id": 1, "name": "Keyboard"}, {"id": 2, "name": "Mouse"}]


def main():
    print("=" * 60)
    print("  MODULE 13: MINI API ROUTER PLAYGROUND [*]")
    print("=" * 60)

    for path in ["/", "/api/products", "/unknown"]:
        status, body = app.handle_request("GET", path)
        print(f"\n--> GET {path}")
        print(f"    Status: {status}")
        print(f"    Body:   {body}")

    print("\n[OK] Mini ASGI router simulated without external dependencies!")


if __name__ == "__main__":
    main()
