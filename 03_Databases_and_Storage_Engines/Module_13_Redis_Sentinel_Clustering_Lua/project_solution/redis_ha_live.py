"""Module 13: Real Redis HA, Lua Scripting, Streams & Consumer Groups (Track B).

Operates against live Redis to demonstrate:
1. Atomic multi-key transactional updates via Lua EVAL and EVALSHA with SHA1 caching.
2. Hash tags ensuring multi-key co-location on identical cluster hash slots.
3. Synchronous replication durability verification using WAIT.
4. Redis Streams event messaging: XADD append, XGROUP creation, and XREADGROUP consumption.
5. Pending Entries List (PEL) tracking via XPENDING and fault-tolerant message recovery via XAUTOCLAIM/XCLAIM.
"""

from __future__ import annotations

import os

from typing import Any

try:
    import redis
except ImportError:
    redis = None  # type: ignore


class RedisHALiveClient:
    """Production client for high-availability Redis patterns."""

    def __init__(self, host: str = os.environ.get("COURSE_DB_HOST", "localhost"), port: int = int(os.environ.get("COURSE_REDIS_PORT", "16379")), db: int = 0):
        if redis is None:
            raise RuntimeError("redis package is not installed. Install with: pip install redis")
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except Exception:
            return False

    def reserve_inventory_atomic(self, item_key: str, reservation_key: str, quantity: int) -> bool:
        """Executes an atomic check-and-decrement inventory reservation in Lua."""
        lua_script = """
        local stock = tonumber(redis.call("get", KEYS[1]) or "0")
        local req = tonumber(ARGV[1])
        if stock >= req then
            redis.call("decrby", KEYS[1], req)
            redis.call("set", KEYS[2], req, "EX", 60)
            return 1
        else
            return 0
        end
        """
        result = self.client.eval(lua_script, 2, item_key, reservation_key, str(quantity))
        return bool(result)

    def load_script_sha(self, script_body: str) -> str:
        """Loads a Lua script into the Redis script cache and returns its SHA1 digest."""
        return self.client.script_load(script_body)

    def execute_evalsha(self, sha: str, keys: list[str], args: list[str]) -> Any:
        return self.client.evalsha(sha, len(keys), *keys, *args)

    def write_with_replication_wait(self, key: str, value: str, num_replicas: int = 0, timeout_ms: int = 100) -> int:
        """Writes a key and blocks until acknowledged by the given number of replicas."""
        self.client.set(key, value)
        acks = self.client.wait(num_replicas, timeout_ms)
        return int(acks)

    def stream_append(self, stream_key: str, fields: dict[str, str]) -> str:
        """Appends an event to the stream (XADD)."""
        msg_id = self.client.xadd(stream_key, fields)
        return str(msg_id)

    def create_consumer_group(self, stream_key: str, group_name: str, id_offset: str = "0") -> bool:
        """Creates a consumer group for a stream (XGROUP CREATE)."""
        try:
            self.client.xgroup_create(stream_key, group_name, id=id_offset, mkstream=True)
            return True
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" in str(e):
                return True
            raise

    def consume_events(
        self, stream_key: str, group_name: str, consumer_name: str, count: int = 10, block_ms: int = 500
    ) -> list[tuple[str, dict[str, str]]]:
        """Reads unacknowledged events from a consumer group (XREADGROUP)."""
        resp = self.client.xreadgroup(
            groupname=group_name,
            consumername=consumer_name,
            streams={stream_key: ">"},
            count=count,
            block=block_ms,
        )
        if not resp:
            return []
        events = []
        for _stream, messages in resp:
            for msg_id, fields in messages:
                events.append((msg_id, fields))
        return events

    def ack_event(self, stream_key: str, group_name: str, msg_id: str) -> int:
        """Acknowledges successful processing of an event (XACK)."""
        return int(self.client.xack(stream_key, group_name, msg_id))

    def inspect_pel(self, stream_key: str, group_name: str) -> dict[str, Any]:
        """Inspects the Pending Entries List (PEL) via XPENDING."""
        pel = self.client.xpending(stream_key, group_name)
        return {
            "pending_count": pel.get("pending", 0),
            "min_id": pel.get("min"),
            "max_id": pel.get("max"),
            "consumers": pel.get("consumers", []),
        }

    def claim_stale_event(
        self, stream_key: str, group_name: str, new_consumer: str, min_idle_ms: int, msg_id: str
    ) -> list[Any]:
        """Recovers an unacknowledged event abandoned by a crashed worker (XCLAIM)."""
        return self.client.xclaim(
            name=stream_key,
            groupname=group_name,
            consumername=new_consumer,
            min_idle_time=min_idle_ms,
            message_ids=[msg_id],
        )
