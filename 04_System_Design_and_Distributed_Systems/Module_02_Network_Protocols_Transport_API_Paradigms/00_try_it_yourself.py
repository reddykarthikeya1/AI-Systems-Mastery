"""Beginner playground for Module 02 - Network Protocols, Transport and API Paradigms.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import json

# ------------------------- 1. The handshake you pay for before any data moves
RTT_MS = 150            # Dublin to Sydney, one way and back

costs = {
    "UDP (no handshake)": 0,
    "TCP handshake": 1,
    "TCP + TLS 1.3": 2,
    "TCP + TLS 1.2": 3,
}
for label, round_trips in costs.items():
    print(f"  {label:<22} {round_trips} RTT = {round_trips * RTT_MS:>3} ms before any data")

assert costs["TCP + TLS 1.3"] * RTT_MS == 300
print("300 ms spent on introductions before the request is even sent.")


# ------------------------------------- 2. Chatty beats slow, and chatty loses
calls = 50
server_work_ms = 1

sequential = calls * (RTT_MS + server_work_ms)
batched = RTT_MS + calls * server_work_ms
parallel_10 = (calls / 10) * (RTT_MS + server_work_ms)

print(f"50 calls, one after another: {sequential:>6,.0f} ms")
print(f"10 at a time, in parallel:   {parallel_10:>6,.0f} ms")
print(f"1 batched call:              {batched:>6,.0f} ms")
assert sequential == 7_550
assert batched == 200
assert sequential / batched > 35
print("Same server, same code, same data. 37x, purely from trip count.")


# ---------------- 3. REST, gRPC and GraphQL are three answers to one question
full_user = {"id": 1, "name": "ana", "email": "ana@example.com",
             "bio": "x" * 500, "preferences": {"theme": "dark"}, "avatar_url": "..."}


def rest_response(user):
    return user                                      # the whole resource, always


def graphql_response(user, fields):
    return {k: user[k] for k in fields}              # exactly what was asked for


rest_bytes = len(json.dumps(rest_response(full_user)))
graphql_bytes = len(json.dumps(graphql_response(full_user, ["id", "name"])))

print(f"REST:    {rest_bytes:>4} bytes")
print(f"GraphQL: {graphql_bytes:>4} bytes for the same list screen")
assert graphql_bytes < rest_bytes / 10
print("Multiply by 50 rows and a page, and it is the whole page weight.")


# ---------------------------------------------- 4. When to reach for each one
def recommend(caller, needs_push, many_client_shapes):
    if needs_push:
        return "websocket"
    if caller == "internal_service":
        return "grpc"
    if many_client_shapes:
        return "graphql"
    return "rest"


cases = [
    ("public API for third parties", "third_party", False, False),
    ("payment service calling ledger", "internal_service", False, False),
    ("chat app receiving messages", "browser", True, False),
    ("one backend, web + iOS + watch", "browser", False, True),
]
for label, caller, push, shapes in cases:
    print(f"  {label:<32} -> {recommend(caller, push, shapes)}")

assert recommend("internal_service", False, False) == "grpc"
assert recommend("browser", True, False) == "websocket"


print()
print("All checks passed.")
