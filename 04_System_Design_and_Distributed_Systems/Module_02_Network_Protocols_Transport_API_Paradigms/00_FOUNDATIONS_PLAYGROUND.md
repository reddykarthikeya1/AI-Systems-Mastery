# Beginner Playground - Network Protocols, Transport and API Paradigms

> *"TCP is a phone call: you say hello, they say hello back, and you confirm everything you heard. UDP is a postcard: you write it, you post it, and you never hear again."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import json
```

---

## 1. The handshake you pay for before any data moves

TCP guarantees delivery and ordering, and charges a round trip up front to
establish the connection. Add TLS and you pay more. Only then does your request
start moving.

UDP skips all of it - no handshake, no retransmission, no ordering. You lose
reliability and gain the one thing TCP cannot give you: no setup cost. Which is
why voice and video use it. A re-sent packet of audio from 200 ms ago is worth
less than silence.

```python
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
```

---

## 2. Chatty beats slow, and chatty loses

Fifty sequential calls to Sydney is fifty round trips. The server work might be a
millisecond each; the network is 150 ms each. The code is not the problem.

```python
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
```

---

## 3. REST, gRPC and GraphQL are three answers to one question

The question is *who decides what comes back*.

| Style | Who decides | Costs you |
| :--- | :--- | :--- |
| REST | the server | over-fetching, and N+1 calls for related data |
| GraphQL | the client | server complexity; a client can ask for something ruinous |
| gRPC | a shared contract | binary, so not readable by a browser or `curl` |

REST returns the whole resource whether or not you wanted it. For a list screen
showing only names, that is most of your bandwidth wasted.

```python
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
```

---

## 4. When to reach for each one

There is no winner, only a fit:

- **REST** for public APIs. Everyone understands it, caches understand it, and it
  works from a browser address bar.
- **gRPC** for service-to-service inside your own network. Binary, fast, and the
  contract is generated rather than documented.
- **GraphQL** when many different clients need many different shapes of the same
  data - which is exactly the mobile-plus-web-plus-watch problem it was built for.
- **WebSocket** when the *server* needs to speak first. Polling for new messages
  is the thing it replaces.

```python
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
```

---

## 5. Predict before you run

Your server is in Dublin and your user is in Sydney - about 150 ms each way.
Your page makes 50 small API calls, one after another. How long does the user
wait? What if the calls were batched into one?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

The single most common cause of a slow page is not slow code - it is too many
round trips. You cannot make light faster, so the only lever is making fewer
trips.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
