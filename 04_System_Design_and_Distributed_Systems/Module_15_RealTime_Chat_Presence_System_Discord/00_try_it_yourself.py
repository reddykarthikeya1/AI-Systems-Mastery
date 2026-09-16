"""Beginner playground for Module 15 - Real-Time Chat and Presence.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# --------------------------------------- 1. Count what polling actually costs
users = 100_000
poll_interval_seconds = 2
messages_per_user_per_hour = 10

poll_qps = users / poll_interval_seconds
useful_qps = users * messages_per_user_per_hour / 3_600
print(f"polling:  {poll_qps:>10,.0f} requests/second")
print(f"of which useful: {useful_qps:>5,.0f}/second ({useful_qps / poll_qps:.2%})")
assert poll_qps == 50_000
assert useful_qps / poll_qps < 0.01, "over 99% of requests find nothing"


# --------------------------------- 2. A held-open connection inverts the cost
websocket_qps = useful_qps
print(f"websocket: {websocket_qps:>10,.0f} messages/second, "
      f"{users:,} open connections")
print(f"reduction in requests: {poll_qps / websocket_qps:.0f}x")
assert poll_qps / websocket_qps > 150

worst_case_latency_polling = poll_interval_seconds * 1_000
worst_case_latency_socket = 50
print(f"worst-case delivery latency: polling {worst_case_latency_polling:,.0f} ms, "
      f"socket ~{worst_case_latency_socket} ms")
assert worst_case_latency_socket < worst_case_latency_polling / 10


# ------------------------------------ 3. Presence: how you know somebody left
HEARTBEAT_TIMEOUT = 30

last_seen = {"ana": 100, "bo": 100, "cy": 100}


def who_is_online(now):
    return sorted(u for u, t in last_seen.items() if now - t < HEARTBEAT_TIMEOUT)


last_seen["ana"] = 120                      # ana keeps pinging

print("at t=110, online:", who_is_online(110))
assert who_is_online(110) == ["ana", "bo", "cy"], "10s of silence is still inside 30s"

print("at t=135, online:", who_is_online(135))
assert who_is_online(135) == ["ana"], "bo and cy have been silent for 35s"
print("bo's laptop lid closed at t=100. We find out at t=130 at the earliest.")


# --------------------------------------------- 4. Fan-out is the real problem
channel_members = 10_000
servers = 50

naive_hops = channel_members
pubsub_hops = servers
print(f"direct delivery:  {naive_hops:,} cross-server messages")
print(f"via pub/sub:      {pubsub_hops:,} cross-server messages, "
      f"then local fan-out")
assert pubsub_hops == 50
assert naive_hops / pubsub_hops == 200, "200x fewer network hops"

connections_per_server = channel_members / servers
print(f"each server then delivers locally to {connections_per_server:.0f} sockets")
print("Local delivery is memory. Cross-server delivery is network. Prefer memory.")


print()
print("All checks passed.")
