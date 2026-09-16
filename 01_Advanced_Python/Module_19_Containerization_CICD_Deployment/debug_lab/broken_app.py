#!/usr/bin/env python3
"""Broken Microservice Deployment demonstrating localhost binding inside Docker."""

import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/healthz")
def health():
    return {"status": "ok"}

def start_server():
    # The container will listen ONLY on its private internal loopback interface,
    # making it unreachable from the host machine or Docker port forwarding!
    host = "127.0.0.1"
    print(f"Starting server on {host}:8000 (Unreachable outside container!)")
    # In production, must be "0.0.0.0"

if __name__ == "__main__":
    start_server()
