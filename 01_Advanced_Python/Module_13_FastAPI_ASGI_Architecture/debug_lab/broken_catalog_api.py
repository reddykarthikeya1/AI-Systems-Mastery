#!/usr/bin/env python3
"""Broken FastAPI Catalog API demonstrating event loop blocking and route order traps."""

import time
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(item_id: str):
    return {"item_id": item_id, "type": "dynamic"}

@app.get("/items/special")
def get_special_item():
    return {"item_id": "special", "type": "special_offer"}

@app.get("/slow-calc")
async def slow_calculation():
    time.sleep(1.0)  # Blocks ASGI worker event loop!
    return {"status": "complete"}

if __name__ == "__main__":
    client = TestClient(app)
    res = client.get("/items/special")
    print(f"Request to /items/special returned type: {res.json()['type']} (Expected 'special_offer'!)")

    t0 = time.perf_counter()
    client.get("/slow-calc")
    print(f"Slow calc took: {time.perf_counter() - t0:.2f}s")
