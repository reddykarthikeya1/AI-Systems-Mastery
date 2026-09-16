"""Unit tests for Module 03 Layer 7 API Gateway & Reverse Proxy."""

import pytest
import pytest_asyncio
from api_gateway_proxy import APIGateway, ServiceCluster, TokenBucketRateLimiter, UpstreamServer


@pytest_asyncio.fixture
async def gateway_env() -> APIGateway:
    gateway = APIGateway(default_rate_limit_capacity=5, default_refill_per_sec=2.0)

    # 1. User Cluster with 2 servers
    async def user_handler_1(req: dict) -> dict:
        return {"service": "user", "node": "user-1", "user_id": req.get("id")}

    async def user_handler_2(req: dict) -> dict:
        return {"service": "user", "node": "user-2", "user_id": req.get("id")}

    user_cluster = ServiceCluster(
        name="user-service",
        servers=[
            UpstreamServer(server_id="usr-1", url="http://10.0.1.1:8080", handler=user_handler_1),
            UpstreamServer(server_id="usr-2", url="http://10.0.1.2:8080", handler=user_handler_2),
        ],
    )

    # 2. Orders Cluster with 1 flaky server
    async def flaky_handler(req: dict) -> dict:
        raise ConnectionResetError("Connection refused by upstream db")

    order_cluster = ServiceCluster(
        name="order-service",
        servers=[
            UpstreamServer(server_id="ord-1", url="http://10.0.2.1:8080", handler=flaky_handler),
        ],
    )

    gateway.register_cluster("/api/v1/users", user_cluster)
    gateway.register_cluster("/api/v1/orders", order_cluster)

    return gateway


@pytest.mark.asyncio
async def test_token_bucket_rate_limiter() -> None:
    limiter = TokenBucketRateLimiter(capacity=3, refill_rate_per_sec=10.0)

    # 3 bursts allowed
    assert await limiter.allow_request() is True
    assert await limiter.allow_request() is True
    assert await limiter.allow_request() is True

    # 4th burst rejected
    assert await limiter.allow_request() is False


@pytest.mark.asyncio
async def test_path_routing_and_round_robin(gateway_env: APIGateway) -> None:
    # Request 1 -> usr-1
    resp1 = await gateway_env.route_request("/api/v1/users/123", client_ip="192.168.1.10", payload={"id": 123})
    assert resp1["status_code"] == 200
    assert resp1["upstream"] == "usr-1"
    assert resp1["response"]["node"] == "user-1"
    assert "trace_id" in resp1

    # Request 2 -> usr-2 (Round Robin)
    resp2 = await gateway_env.route_request("/api/v1/users/124", client_ip="192.168.1.10", payload={"id": 124})
    assert resp2["status_code"] == 200
    assert resp2["upstream"] == "usr-2"
    assert resp2["response"]["node"] == "user-2"

    # Request 3 -> usr-1 again
    resp3 = await gateway_env.route_request("/api/v1/users/125", client_ip="192.168.1.10", payload={"id": 125})
    assert resp3["status_code"] == 200
    assert resp3["upstream"] == "usr-1"


@pytest.mark.asyncio
async def test_unmatched_route_returns_404(gateway_env: APIGateway) -> None:
    resp = await gateway_env.route_request("/api/v1/unknown", client_ip="192.168.1.10")
    assert resp["status_code"] == 404
    assert "No upstream cluster found" in resp["error"]


@pytest.mark.asyncio
async def test_rate_limiting_triggers_429(gateway_env: APIGateway) -> None:
    client_ip = "10.50.0.1"

    # Exhaust capacity of 5
    for _ in range(5):
        resp = await gateway_env.route_request("/api/v1/users/1", client_ip=client_ip)
        assert resp["status_code"] == 200

    # 6th request should trigger 429
    rate_limited_resp = await gateway_env.route_request("/api/v1/users/1", client_ip=client_ip)
    assert rate_limited_resp["status_code"] == 429
    assert "Rate Limit Exceeded" in rate_limited_resp["error"]


@pytest.mark.asyncio
async def test_upstream_failure_ejection_and_503(gateway_env: APIGateway) -> None:
    client_ip = "10.60.0.1"

    # 3 consecutive failures will eject ord-1
    for _ in range(3):
        resp = await gateway_env.route_request("/api/v1/orders/create", client_ip=client_ip)
        assert resp["status_code"] == 502

    # 4th request: All instances in order-service are now unhealthy -> 503
    resp_503 = await gateway_env.route_request("/api/v1/orders/create", client_ip=client_ip)
    assert resp_503["status_code"] == 503
    assert "Service Unavailable" in resp_503["error"]
