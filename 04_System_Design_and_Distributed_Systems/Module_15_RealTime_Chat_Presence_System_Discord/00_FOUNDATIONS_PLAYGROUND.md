# Beginner Playground - Real-Time Chat and Presence

> *"Polling is ringing the doorbell every ten seconds to ask if the post has arrived. A WebSocket is leaving the phone line open so they can tell you when it does."*


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

## 1. Count what polling actually costs

Polling is simple and it works. It is also almost entirely wasted work, and the
waste is proportional to how fresh you want the data.

```python
users = 100_000
poll_interval_seconds = 2
messages_per_user_per_hour = 10

poll_qps = users / poll_interval_seconds
useful_qps = users * messages_per_user_per_hour / 3_600
print(f"polling:  {poll_qps:>10,.0f} requests/second")
print(f"of which useful: {useful_qps:>5,.0f}/second ({useful_qps / poll_qps:.2%})")
assert poll_qps == 50_000
assert useful_qps / poll_qps < 0.01, "over 99% of requests find nothing"
```

---

## 2. A held-open connection inverts the cost

With a WebSocket the server pushes when there is something to push. Requests drop
to the number of actual messages, and latency drops from "up to the poll interval"
to "as fast as the network".

What you pay instead is *state*: an open connection per user, pinned to one
server. Which means load balancing, reconnection and server failure all become
your problem.

```python
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
```

---

## 3. Presence: how you know somebody left

A connection that drops cleanly tells you. A laptop lid closing, a train entering
a tunnel or a crashed process does not - the socket simply stops producing
traffic, and the server has no way to tell that from a quiet user.

So presence is always a **heartbeat with a timeout**: the client pings; if no ping
arrives within a window, the user is marked offline. Every presence system you
have used works this way, and the window is why someone can look online for a
minute after their phone died.

```python
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
```

---

## 4. Fan-out is the real problem

One message to a 10,000-member channel is one write and 10,000 deliveries. And the
recipients are spread across every server in your fleet, so each delivery is a
cross-server hop.

The fix is not to make the hop faster but to make fewer of them: a
publish/subscribe layer where each *server* subscribes once per channel, and then
delivers locally to whichever of its own connections care.

```python
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
```

---

## 5. Predict before you run

100,000 users poll for new messages every 2 seconds. What request rate is
that? How many of those requests find anything new, if the average user gets
10 messages an hour?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

The interesting problem in chat is never delivery - it is fan-out. A message
to a 10,000-person channel is one write and ten thousand deliveries, and how
you handle that decides whether the system works.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
