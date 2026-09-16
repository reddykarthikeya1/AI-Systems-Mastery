"""Tests for Module 13: Real Redis HA, Lua Scripts & Streams (Track B)."""

from __future__ import annotations

import time
import pytest
from redis_ha_live import RedisHALiveClient
from sentinel_cluster_streams import RedisStreamEngine

def _redis_is_up() -> bool:
    try:
        client = RedisHALiveClient()
        return client.ping()
    except Exception:
        return False

requires_redis = pytest.mark.skipif(
    not _redis_is_up(),
    reason="Redis server is not reachable on localhost:16379 - start with: make up redis"
)

pytestmark = [pytest.mark.requires_redis, requires_redis]


def test_redis_ha_ping():
    client = RedisHALiveClient()
    assert client.ping() is True


def test_redis_lua_atomic_inventory_reservation():
    client = RedisHALiveClient()
    item_key = "inventory:item:laptop_99"
    res_key = "inventory:reserve:order_500"

    client.client.set(item_key, 10)
    client.client.delete(res_key)

    # 1. Successful reservation of 4 units
    assert client.reserve_inventory_atomic(item_key, res_key, quantity=4) is True
    assert int(client.client.get(item_key)) == 6
    assert int(client.client.get(res_key)) == 4

    # 2. Failed reservation when requesting more than available (requesting 7 when 6 remain)
    failed_res = "inventory:reserve:order_501"
    assert client.reserve_inventory_atomic(item_key, failed_res, quantity=7) is False
    assert int(client.client.get(item_key)) == 6

    # 3. Clean up
    client.client.delete(item_key, res_key, failed_res)


def test_redis_evalsha_script_caching():
    client = RedisHALiveClient()
    script = "return tonumber(ARGV[1]) * 2"
    sha = client.load_script_sha(script)
    assert len(sha) == 40

    res = client.execute_evalsha(sha, keys=[], args=["21"])
    assert int(res) == 42


def test_redis_replication_wait():
    client = RedisHALiveClient()
    # Testing wait with 0 expected replicas should return immediately with >= 0
    acks = client.write_with_replication_wait("test:wait:key", "val", num_replicas=0, timeout_ms=50)
    assert acks >= 0
    client.client.delete("test:wait:key")


def test_redis_streams_xadd_and_xgroup_lifecycle():
    client = RedisHALiveClient()
    stream = "stream:orders:m13"
    group = "order_processors"

    client.client.delete(stream)

    # Append events
    msg_id1 = client.stream_append(stream, {"order_id": "ord_1", "amount": "99.50"})
    msg_id2 = client.stream_append(stream, {"order_id": "ord_2", "amount": "149.00"})
    assert "-" in msg_id1 and "-" in msg_id2

    # Create consumer group
    assert client.create_consumer_group(stream, group, id_offset="0") is True

    # Read events
    events = client.consume_events(stream, group, consumer_name="worker_1", count=5)
    assert len(events) == 2
    assert events[0][1]["order_id"] == "ord_1"
    assert events[1][1]["order_id"] == "ord_2"

    # Verify PEL has 2 unacknowledged messages
    pel_before = client.inspect_pel(stream, group)
    assert pel_before["pending_count"] == 2

    # Acknowledge first event
    acked = client.ack_event(stream, group, events[0][0])
    assert acked == 1

    # PEL should now show 1 pending message
    pel_after = client.inspect_pel(stream, group)
    assert pel_after["pending_count"] == 1

    client.client.delete(stream)


def test_redis_streams_xclaim_dead_letter_recovery():
    client = RedisHALiveClient()
    stream = "stream:failover:m13"
    group = "failover_group"

    client.client.delete(stream)
    msg_id = client.stream_append(stream, {"task": "generate_invoice"})
    client.create_consumer_group(stream, group, id_offset="0")

    # Worker 1 reads the message but crashes before ACKing
    worker1_events = client.consume_events(stream, group, consumer_name="crashed_worker", count=1)
    assert len(worker1_events) == 1

    # Worker 2 claims the pending message using min_idle_time = 0
    claimed = client.claim_stale_event(stream, group, new_consumer="rescue_worker", min_idle_ms=0, msg_id=msg_id)
    assert len(claimed) >= 1
    # Successfully acked by rescue worker
    assert client.ack_event(stream, group, msg_id) == 1

    client.client.delete(stream)


@pytest.mark.perf
def test_redis_streams_throughput():
    client = RedisHALiveClient()
    stream = "stream:bench:m13"
    client.client.delete(stream)

    start = time.perf_counter()
    pipe = client.client.pipeline(transaction=False)
    n_events = 200
    for i in range(n_events):
        pipe.xadd(stream, {"event_idx": str(i), "payload": "sample_data"})
    pipe.execute()
    elapsed = time.perf_counter() - start

    rate = n_events / elapsed
    assert rate > 100  # Must achieve > 100 events/sec

    client.client.delete(stream)


def test_track_a_model_matches_real_redis_streams_reconciliation():
    """Track A <-> Track B: Handbuilt RedisStreamEngine vs real Redis Streams."""
    model_stream = RedisStreamEngine()
    live_client = RedisHALiveClient()
    stream_key = "stream:reconcile:m13"
    live_client.client.delete(stream_key)

    # 1. Append message to both
    model_id = model_stream.xadd("orders", {"order_id": "1001", "sku": "WIDGET"})
    live_id = live_client.stream_append(stream_key, {"order_id": "1001", "sku": "WIDGET"})

    # Assert message ID structure matches Redis timestamp format: <millisecondsTime>-<sequenceNumber>
    assert "-" in model_id and "-" in live_id
    m_ts, m_seq = model_id.split("-")
    l_ts, l_seq = live_id.split("-")
    assert int(m_ts) > 0 and int(l_ts) > 0

    # 2. Consumer Group creation & read
    model_stream.xgroup_create("orders", "billing_group")
    live_client.create_consumer_group(stream_key, "billing_group", id_offset="0")

    model_read = model_stream.xreadgroup("orders", "billing_group", "consumer_A", count=1)
    live_read = live_client.consume_events(stream_key, "billing_group", "consumer_A", count=1)

    assert len(model_read) == len(live_read) == 1
    # Model returns [{'id': id, 'data': {...}}], redis-py returns [(id, {...})]
    assert model_read[0]["data"]["order_id"] == live_read[0][1]["order_id"] == "1001"

    # 3. Acknowledgment
    assert model_stream.xack("orders", "billing_group", [model_id]) == 1
    assert live_client.ack_event(stream_key, "billing_group", live_id) == 1

    live_client.client.delete(stream_key)
