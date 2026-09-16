"""Module 02: Asynchronous Binary Framed RPC Protocol Engine.

Implements a production-style multiplexed RPC engine featuring:
- Custom binary framing with magic bytes and fixed-size headers.
- Request/response correlation via unique Correlation IDs.
- Method registration and asynchronous remote procedure invocation.
- Out-of-order multiplexed response handling over a single transport stream.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import asyncio
import json
import struct
import uuid
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from enum import IntEnum
from typing import Any

MAGIC_BYTE = 0xAB
HEADER_FORMAT = ">BB16sI"  # Magic(1B), FrameType(1B), CorrelationID(16B), PayloadLen(4B)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


class FrameType(IntEnum):
    REQUEST = 0x01
    RESPONSE = 0x02
    HEARTBEAT = 0x03
    ERROR = 0x04


@dataclass(frozen=True)
class RPCFrame:
    frame_type: FrameType
    correlation_id: bytes
    payload: bytes


class RPCFrameCodec:
    """Encodes and decodes binary frames with network byte order header packing."""

    @staticmethod
    def encode(frame: RPCFrame) -> bytes:
        header = struct.pack(
            HEADER_FORMAT,
            MAGIC_BYTE,
            int(frame.frame_type),
            frame.correlation_id,
            len(frame.payload),
        )
        return header + frame.payload

    @staticmethod
    def decode_header(header_bytes: bytes) -> tuple[FrameType, bytes, int]:
        if len(header_bytes) != HEADER_SIZE:
            raise ValueError(f"Header must be exactly {HEADER_SIZE} bytes, got {len(header_bytes)}")

        magic, frame_type_raw, correlation_id, payload_len = struct.unpack(
            HEADER_FORMAT, header_bytes
        )
        if magic != MAGIC_BYTE:
            raise ValueError(f"Invalid protocol magic byte: {hex(magic)} (expected {hex(MAGIC_BYTE)})")

        try:
            frame_type = FrameType(frame_type_raw)
        except ValueError as exc:
            raise ValueError(f"Unknown frame type: {frame_type_raw}") from exc

        return frame_type, correlation_id, payload_len


class RPCServer:
    """Multiplexed RPC Server that dispatches requests to registered procedures."""

    def __init__(self) -> None:
        self._handlers: dict[str, Callable[..., Coroutine[Any, Any, Any]]] = {}

    def register(self, method_name: str, handler: Callable[..., Coroutine[Any, Any, Any]]) -> None:
        self._handlers[method_name] = handler

    async def handle_request_frame(self, frame: RPCFrame) -> RPCFrame:
        if frame.frame_type != FrameType.REQUEST:
            return RPCFrame(
                frame_type=FrameType.ERROR,
                correlation_id=frame.correlation_id,
                payload=b"Invalid frame type for server request",
            )

        try:
            request_data = json.loads(frame.payload.decode("utf-8"))
            method = request_data.get("method")
            params = request_data.get("params", {})

            if method not in self._handlers:
                error_resp = {"error": f"Method '{method}' not found"}
                return RPCFrame(
                    frame_type=FrameType.ERROR,
                    correlation_id=frame.correlation_id,
                    payload=json.dumps(error_resp).encode("utf-8"),
                )

            # Invoke registered handler
            handler = self._handlers[method]
            result = await handler(**params)
            response_payload = json.dumps({"result": result}).encode("utf-8")

            return RPCFrame(
                frame_type=FrameType.RESPONSE,
                correlation_id=frame.correlation_id,
                payload=response_payload,
            )
        except Exception as exc:
            error_payload = json.dumps({"error": str(exc)}).encode("utf-8")
            return RPCFrame(
                frame_type=FrameType.ERROR,
                correlation_id=frame.correlation_id,
                payload=error_payload,
            )


class RPCClient:
    """Multiplexed RPC Client that correlates out-of-order responses using Correlation IDs."""

    def __init__(self, server: RPCServer) -> None:
        self._server = server
        self._background_tasks: set[asyncio.Task] = set()
        self._pending_futures: dict[bytes, asyncio.Future[RPCFrame]] = {}

    async def invoke(self, method: str, params: dict[str, Any], timeout_sec: float = 3.0) -> Any:
        correlation_id = uuid.uuid4().bytes
        loop = asyncio.get_running_loop()
        future: asyncio.Future[RPCFrame] = loop.create_future()
        self._pending_futures[correlation_id] = future

        # Prepare request frame
        request_payload = json.dumps({"method": method, "params": params}).encode("utf-8")
        request_frame = RPCFrame(
            frame_type=FrameType.REQUEST,
            correlation_id=correlation_id,
            payload=request_payload,
        )

        # Encode and send over simulated transport channel
        encoded_bytes = RPCFrameCodec.encode(request_frame)

        # Dispatch async execution (simulates network transmission).
        #
        # The reference matters: asyncio holds only a WEAK reference to a task,
        # so a fire-and-forget `create_task(...)` whose handle is discarded can
        # be garbage-collected mid-execution. The symptom is a transmission that
        # silently never happens, under load, non-deterministically. Keep the
        # handle in a set and discard it on completion.
        _send_task = asyncio.create_task(self._simulate_transport_send(encoded_bytes))
        self._background_tasks.add(_send_task)
        _send_task.add_done_callback(self._background_tasks.discard)

        # Await response with correlation timeout
        try:
            response_frame = await asyncio.wait_for(future, timeout=timeout_sec)
        finally:
            self._pending_futures.pop(correlation_id, None)

        response_dict = json.loads(response_frame.payload.decode("utf-8"))
        if response_frame.frame_type == FrameType.ERROR or "error" in response_dict:
            raise RuntimeError(response_dict.get("error", "Unknown RPC Error"))

        return response_dict.get("result")

    async def _simulate_transport_send(self, raw_bytes: bytes) -> None:
        # Simulate packet parsing at server
        header = raw_bytes[:HEADER_SIZE]
        frame_type, correlation_id, payload_len = RPCFrameCodec.decode_header(header)
        payload = raw_bytes[HEADER_SIZE : HEADER_SIZE + payload_len]

        incoming_frame = RPCFrame(frame_type, correlation_id, payload)
        response_frame = await self._server.handle_request_frame(incoming_frame)

        # Response arrives back at client socket
        encoded_response = RPCFrameCodec.encode(response_frame)
        self._on_incoming_wire_response(encoded_response)

    def _on_incoming_wire_response(self, raw_bytes: bytes) -> None:
        header = raw_bytes[:HEADER_SIZE]
        frame_type, correlation_id, payload_len = RPCFrameCodec.decode_header(header)
        payload = raw_bytes[HEADER_SIZE : HEADER_SIZE + payload_len]

        response_frame = RPCFrame(frame_type, correlation_id, payload)
        if correlation_id in self._pending_futures:
            fut = self._pending_futures[correlation_id]
            if not fut.done():
                fut.set_result(response_frame)
