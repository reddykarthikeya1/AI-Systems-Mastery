"""Unit tests for Module 02 Asynchronous RPC Protocol Engine."""

import asyncio

import pytest
import pytest_asyncio
from rpc_protocol_engine import (
    HEADER_SIZE,
    FrameType,
    RPCClient,
    RPCFrame,
    RPCFrameCodec,
    RPCServer,
)


@pytest.fixture
def frame_codec() -> type[RPCFrameCodec]:
    return RPCFrameCodec


@pytest_asyncio.fixture
async def rpc_system() -> tuple[RPCServer, RPCClient]:
    server = RPCServer()

    # Register demo procedures
    async def add(a: int, b: int) -> int:
        return a + b

    async def slow_fetch(item_id: str, delay_sec: float = 0.05) -> dict:
        await asyncio.sleep(delay_sec)
        return {"id": item_id, "status": "ACTIVE"}

    async def fail_op() -> None:
        raise ValueError("Database unavailable")

    server.register("add", add)
    server.register("slow_fetch", slow_fetch)
    server.register("fail_op", fail_op)

    client = RPCClient(server)
    return server, client


def test_frame_encoding_and_header_decoding(frame_codec: type[RPCFrameCodec]) -> None:
    correlation_id = b"0123456789abcdef"
    payload = b"Hello Distributed Systems!"
    frame = RPCFrame(
        frame_type=FrameType.REQUEST,
        correlation_id=correlation_id,
        payload=payload,
    )

    encoded = frame_codec.encode(frame)
    assert len(encoded) == HEADER_SIZE + len(payload)

    frame_type, decoded_corr_id, payload_len = frame_codec.decode_header(
        encoded[:HEADER_SIZE]
    )
    assert frame_type == FrameType.REQUEST
    assert decoded_corr_id == correlation_id
    assert payload_len == len(payload)


def test_invalid_magic_byte_raises_error(frame_codec: type[RPCFrameCodec]) -> None:
    bad_header = b"\xFF" + b"\x00" * (HEADER_SIZE - 1)
    with pytest.raises(ValueError, match="Invalid protocol magic byte"):
        frame_codec.decode_header(bad_header)


@pytest.mark.asyncio
async def test_rpc_successful_method_invocation(rpc_system: tuple[RPCServer, RPCClient]) -> None:
    _, client = rpc_system
    result = await client.invoke("add", {"a": 15, "b": 27})
    assert result == 42


@pytest.mark.asyncio
async def test_rpc_multiplexed_concurrent_calls(rpc_system: tuple[RPCServer, RPCClient]) -> None:
    _, client = rpc_system

    # Send 5 concurrent requests over the same client channel
    tasks = [
        client.invoke("slow_fetch", {"item_id": f"ITEM_{i}", "delay_sec": 0.02})
        for i in range(5)
    ]
    results = await asyncio.gather(*tasks)

    assert len(results) == 5
    for i, res in enumerate(results):
        assert res["id"] == f"ITEM_{i}"
        assert res["status"] == "ACTIVE"


@pytest.mark.asyncio
async def test_rpc_method_not_found_raises_runtime_error(rpc_system: tuple[RPCServer, RPCClient]) -> None:
    _, client = rpc_system
    with pytest.raises(RuntimeError, match="Method 'non_existent' not found"):
        await client.invoke("non_existent", {})


@pytest.mark.asyncio
async def test_rpc_server_exception_propagates_to_client(rpc_system: tuple[RPCServer, RPCClient]) -> None:
    _, client = rpc_system
    with pytest.raises(RuntimeError, match="Database unavailable"):
        await client.invoke("fail_op", {})
