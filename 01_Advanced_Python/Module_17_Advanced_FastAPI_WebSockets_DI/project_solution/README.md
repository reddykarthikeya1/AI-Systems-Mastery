# Design Rationale: Real-Time Financial Ticker & WebSocket Broadcast Hub

## Architectural Overview
A high-concurrency real-time WebSocket hub implementing hierarchical dependency injection, correlation ID tracing middleware, and resilient client broadcast managers.

## Key Design Decisions
1. **Hierarchical Dependency Injection (`Depends`):** Resolves request dependencies in a composable DAG, caching shared sub-dependencies per request and guaranteeing cleanup after response completion.
2. **Distributed Tracing Middleware:** An ASGI middleware intercepts every incoming request and attaches a unique `X-Correlation-ID`, propagating tracing headers across log entries.
3. **Defensive WebSocket Connection Management:** The `ConnectionManager` isolates dead client sockets upon `WebSocketDisconnect`, preventing broadcast stalls to active listeners.

## Rejected Alternatives
1. **Consuming Full Request Bodies in Custom Middleware:**
   - *Reason for Rejection:* Reading `await request.body()` inside ASGI middleware exhausts the receive stream, causing downstream FastAPI endpoints to receive empty payloads.
2. **Long-Polling HTTP Requests for Real-Time Feeds:**
   - *Reason for Rejection:* Long-polling incurs repeated HTTP header overhead and TLS renegotiation latency compared to persistent full-duplex WebSocket frames.

## Invariants & Guarantees
- Disconnected WebSocket clients are removed immediately without blocking broadcasts.
- Dependency overrides in tests provide 100% test isolation.

## Verification
```bash
pytest test_chat_api.py -v
```
