# LLD Case Study 16: Kafka Consumer Group Partition Rebalancing

> **The Bridge: How Do Consumers Share Work at Scale?**
> In Chapter 16 of Track 1, we learned that Apache Kafka scales horizontally by splitting a topic into **Partitions** (e.g. 12 partitions).
> 
> But what happens inside a **Consumer Group** when you have 4 worker applications reading those 12 partitions, and suddenly:
> 1. Worker 3 crashes!
> 2. Or you deploy 2 new servers to handle a traffic surge!
> 
> How do the surviving workers detect the crash, renegotiate ownership of the 12 partitions, and resume reading without duplicating or dropping messages?
> 
> This process is called **Consumer Group Partition Rebalancing**.
> In this case study, we will design the industrial **Cooperative Sticky Assignor** protocol and examine how modern streaming brokers avoid catastrophic "Stop-The-World" rebalance storms.

---

## 1. Zero-Prerequisite Intuition: The "Airport Baggage Carousel Shift"

```mermaid
flowchart TD
    subgraph Topic["Kafka Topic: 'orders' (6 Partitions)"]
        P0["Partition 0"]
        P1["Partition 1"]
        P2["Partition 2"]
        P3["Partition 3"]
        P4["Partition 4"]
        P5["Partition 5"]
    end

    subgraph GroupBefore["Consumer Group (2 Workers: Balanced)"]
        W1["Worker 1: Reading P0, P1, P2"]
        W2["Worker 2: Reading P3, P4, P5"]
    end

    subgraph Crash["Worker 1 Sudden Power Outage!"]
        Dead["Worker 1 stops sending Heartbeats!"]
    end

    subgraph GroupAfter["Rebalanced Group (Worker 2 Takes All)"]
        W2_After["Worker 2: Reading P0, P1, P2, P3, P4, P5"]
    end

    Topic --> GroupBefore
    GroupBefore -.-> Crash
    Crash --> GroupAfter
```

### The Eager vs Cooperative Rebalance Revolution
* **The Legacy Eager Way ("Evasive Stop-The-World"):** When Worker 1 died, Kafka forced ALL surviving workers to drop ALL their assigned partitions. The entire message processing pipeline stopped cold for 30 seconds while everyone renegotiated from zero!
* **The Modern Cooperative Sticky Way (Incremental Handover):** 
  - Surviving workers keep processing their existing partitions without interruption.
  - Only the orphaned partitions (from the dead worker) are reassigned to the surviving workers.
  - Downtime drops from 30 seconds to **$0$ seconds**!

---

## 2. Requirements & Architecture

### Functional Requirements:
1. **Group Membership & Heartbeats:** Workers periodically send heartbeats to the Group Coordinator. If no heartbeat arrives within `session_timeout_ms`, the worker is marked dead.
2. **Deterministic Partition Assignment:** Distribute $M$ partitions across $N$ active consumers fairly and evenly.
3. **Sticky Allocation:** When rebalancing occurs, minimize partition movement (keep partitions on their previous consumers if still alive).
4. **Generation ID (Epoch Fencing):** Every rebalance increments a `generation_id` to reject stale commits from zombie workers.

---

## 3. Production-Grade Python Implementation

```python
# kafka_rebalance_engine.py
import time
from typing import Dict, List, Set, Optional

class Partition:
    def __init__(self, topic: str, partition_id: int):
        self.topic = topic
        self.partition_id = partition_id

    def __repr__(self):
        return f"{self.topic}-{self.partition_id}"


class ConsumerMember:
    def __init__(self, member_id: str):
        self.member_id = member_id
        self.assigned_partitions: Set[Partition] = set()
        self.last_heartbeat = time.monotonic()


class CooperativeStickyAssignor:
    """
    Distributes partitions evenly while preserving existing assignments (Stickiness).
    Minimizes partition migration during rebalances.
    """
    @staticmethod
    def assign(
        all_partitions: List[Partition], 
        active_members: List[ConsumerMember]
    ) -> Dict[str, Set[Partition]]:
        if not active_members:
            return {}

        target_per_consumer = len(all_partitions) // len(active_members)
        remainder = len(all_partitions) % len(active_members)
        
        new_assignments: Dict[str, Set[Partition]] = {m.member_id: set() for m in active_members}
        unassigned_partitions: Set[Partition] = set(all_partitions)

        # Step 1: Retain sticky partitions if still valid
        for member in active_members:
            retained = member.assigned_partitions.intersection(unassigned_partitions)
            # Cap retention to fair share
            while len(retained) > target_per_consumer + (1 if remainder > 0 else 0):
                retained.pop()
            
            new_assignments[member.member_id] = retained
            unassigned_partitions.difference_update(retained)

        # Step 2: Distribute remaining unassigned partitions evenly
        member_idx = 0
        for partition in sorted(unassigned_partitions, key=lambda p: p.partition_id):
            # Find member with fewest partitions
            least_loaded = min(active_members, key=lambda m: len(new_assignments[m.member_id]))
            new_assignments[least_loaded.member_id].add(partition)

        return new_assignments


class GroupCoordinator:
    """Manages group heartbeats, failure detection, and incremental rebalance triggers."""
    def __init__(self, group_id: str, partitions: List[Partition], session_timeout_sec: float = 3.0):
        self.group_id = group_id
        self.partitions = partitions
        self.session_timeout_sec = session_timeout_sec
        self.members: Dict[str, ConsumerMember] = {}
        self.generation_id = 0

    def register_member(self, member_id: str):
        self.members[member_id] = ConsumerMember(member_id)
        self.trigger_rebalance("Member joined")

    def heartbeat(self, member_id: str):
        if member_id in self.members:
            self.members[member_id].last_heartbeat = time.monotonic()

    def check_failures_and_rebalance(self):
        now = time.monotonic()
        dead_members = [
            m_id for m_id, m in self.members.items() 
            if now - m.last_heartbeat > self.session_timeout_sec
        ]
        
        if dead_members:
            for d in dead_members:
                print(f"[COORDINATOR] Worker '{d}' missed heartbeats! Marking DEAD.")
                del self.members[d]
            self.trigger_rebalance("Worker failure detected")

    def trigger_rebalance(self, reason: str):
        self.generation_id += 1
        print(f"\n[REBALANCE Triggered: {reason}] Generation: {self.generation_id}")
        
        assignments = CooperativeStickyAssignor.assign(
            self.partitions, 
            list(self.members.values())
        )
        
        for m_id, parts in assignments.items():
            self.members[m_id].assigned_partitions = parts
            print(f"  -> {m_id}: {[str(p) for p in parts]}")


# --- Simulation Demonstration ---
if __name__ == "__main__":
    # Create 6 topic partitions
    partitions = [Partition("orders", i) for i in range(6)]
    coordinator = GroupCoordinator("order_consumers", partitions, session_timeout_sec=1.0)

    print("--- [STAGE 1] Workers A and B Join the Group ---")
    coordinator.register_member("worker_A")
    coordinator.register_member("worker_B")

    print("\n--- [STAGE 2] Worker C Joins to Share Load ---")
    coordinator.register_member("worker_C")

    print("\n--- [STAGE 3] Normal Heartbeats Keep Group Stable ---")
    coordinator.heartbeat("worker_A")
    coordinator.heartbeat("worker_B")
    coordinator.heartbeat("worker_C")
    print("Heartbeats acknowledged. Zero rebalances needed.")

    print("\n--- [STAGE 4] Worker B Crashes (Misses Heartbeats) ---")
    # Simulate time passing without Worker B sending heartbeats
    time.sleep(1.2)
    coordinator.heartbeat("worker_A")
    coordinator.heartbeat("worker_C")
    # Coordinator detects Worker B timeout and rebalances stickily!
    coordinator.check_failures_and_rebalance()
```

---

## 4. Milestone Check: What You Just Mastered!

You now understand:
1. How Kafka divides topic partitions among consumer group members.
2. Why **Stop-The-World** rebalances caused multi-minute production outages in legacy systems.
3. How the **Cooperative Sticky Assignor** preserves live partition assignments while transferring only orphaned partitions.
4. How **Generation IDs** prevent stale writes from zombie workers that temporarily disconnected.


---

## 4. Edge Cases, Tests and Extensions

### What the assignor guarantees and where it falls short

| Property | Status | Detail |
| :--- | :--- | :--- |
| Even spread when members join or leave | Mostly | Shares differ by at most one in the common cases |
| Stickiness | Good | Members keep partitions they already hold, so only the necessary ones move |
| Balance when the partition count is not divisible | **Bug** | The retention cap is `target + 1` for every member whenever there is a remainder, so several members can keep the extra partition: 7 partitions split 3, 3, 1 instead of 3, 2, 2 |
| Which partition is dropped when trimming | Arbitrary | `set.pop()` order is not deterministic across runs; sort for reproducibility |
| Failure detection | Good | A missed `session_timeout_sec` removes the member and triggers a rebalance |
| "Cooperative" in the class name | Overstated | A truly cooperative protocol revokes in a first round and assigns in a second, so unaffected consumers never stop; this simulation does one assignment step |

### Tests, including the imbalance bug

This block extends the implementation above. The last section replaces the retention cap with proper per-member quotas and checks the result on randomised scenarios.

```python
# continues: rebalance implementation above
import io, contextlib, random
from unittest import mock

def counts(assignments):
    return sorted(len(v) for v in assignments.values())

def members(*held):
    out = []
    for i, parts in enumerate(held):
        m = ConsumerMember(f"m{i}"); m.assigned_partitions = set(parts); out.append(m)
    return out

P = [Partition("orders", i) for i in range(6)]

# Fresh join: 6 partitions over 2 members is 3 / 3, and every partition is assigned once
a = CooperativeStickyAssignor.assign(P, members([], []))
assert counts(a) == [3, 3] and set().union(*a.values()) == set(P)

# A third member joins: shares become 2 / 2 / 2 and only two partitions move
before = members(P[:3], P[3:], [])
a = CooperativeStickyAssignor.assign(P, before)
assert counts(a) == [2, 2, 2]
moved = sum(len(m.assigned_partitions - a[m.member_id]) for m in before)
assert moved == 2

# A member dies: survivors keep everything they had
survivors = members(P[:2], P[4:])                       # m1 (P2, P3) is gone
a = CooperativeStickyAssignor.assign(P, survivors)
assert set(P[:2]) <= a["m0"] and set(P[4:]) <= a["m1"] and counts(a) == [3, 3]

# Bug: 7 partitions, holders 4 / 3 / 0, end up 3 / 3 / 1
P7 = [Partition("t", i) for i in range(7)]
a = CooperativeStickyAssignor.assign(P7, members(P7[:4], P7[4:], []))
assert counts(a) == [1, 3, 3]

# Fix: quota per member. The first `extra` members (largest current holders first) may keep base + 1
def balanced_sticky_assign(all_partitions, active):
    base, extra = divmod(len(all_partitions), len(active))
    everything = set(all_partitions)
    order = sorted(active, key=lambda m: (-len(m.assigned_partitions & everything), m.member_id))
    quota = {m.member_id: base + (1 if i < extra else 0) for i, m in enumerate(order)}
    out, free = {}, set(everything)
    for m in order:
        keep = sorted(m.assigned_partitions & free, key=lambda p: p.partition_id)[:quota[m.member_id]]
        out[m.member_id] = set(keep); free -= set(keep)
    for p in sorted(free, key=lambda p: p.partition_id):
        m = min(order, key=lambda m: (len(out[m.member_id]) - quota[m.member_id], m.member_id))
        out[m.member_id].add(p)
    return out

a = balanced_sticky_assign(P7, members(P7[:4], P7[4:], []))
assert counts(a) == [2, 2, 3]

rng = random.Random(7)
for _ in range(300):
    n_parts, n_members = rng.randint(1, 30), rng.randint(1, 8)
    parts = [Partition("x", i) for i in range(n_parts)]
    held = [set() for _ in range(n_members)]
    for p in parts:
        if rng.random() < 0.8:
            held[rng.randrange(n_members)].add(p)
    ms = members(*held)
    out = balanced_sticky_assign(parts, ms)
    sizes = [len(v) for v in out.values()]
    assert max(sizes) - min(sizes) <= 1                                   # balanced
    assert sorted(p.partition_id for v in out.values() for p in v) == list(range(n_parts))   # every partition exactly once
    base, extra = divmod(n_parts, n_members)
    for m in ms:                                                          # sticky: keeps min(held, quota)
        assert len(out[m.member_id] & m.assigned_partitions) >= min(len(m.assigned_partitions), base)

# Failure detection with a fake clock
clock = [0.0]
with mock.patch("time.monotonic", lambda: clock[0]), contextlib.redirect_stdout(io.StringIO()):
    gc = GroupCoordinator("g", P, session_timeout_sec=1.0)
    gc.register_member("A"); gc.register_member("B")
    gen = gc.generation_id
    clock[0] = 0.5
    gc.heartbeat("A"); gc.heartbeat("B"); gc.check_failures_and_rebalance()
    assert gc.generation_id == gen                                        # healthy group: no rebalance
    clock[0] = 1.7
    gc.heartbeat("A")                                                     # B stays silent for 1.2 s
    gc.check_failures_and_rebalance()
    assert "B" not in gc.members and gc.generation_id == gen + 1
    assert gc.members["A"].assigned_partitions == set(P)                 # A inherits everything
print("rebalance tests passed")
```

### Extensions interviewers ask for

1. **True cooperative rebalancing:** in round one the coordinator tells owners which partitions to revoke; in round two, after owners release them, the new owners receive them. Consumers that keep their partitions never pause.
2. **Static membership:** a restarting consumer with the same `group.instance.id` gets its old partitions back within the session timeout, avoiding a rebalance for a rolling restart.
3. **Generation fencing:** every commit carries the generation id; a commit from an older generation is rejected, which stops a zombie consumer from overwriting offsets after it was replaced.
4. **Rack awareness and weights:** extend the quota so heavier consumers receive proportionally more partitions, and prefer partitions in the consumer's zone.
5. **Rebalance storms:** flapping members cause repeated reassignments; add a minimum interval and a longer `session_timeout` than the longest GC or processing pause.

### Follow-up questions

- *Why is stickiness valuable?* Moving a partition means committing offsets, closing readers and rebuilding local caches or state stores; keeping assignments stable keeps lag low during a rebalance.
- *What triggers a rebalance?* A member joining, leaving, or timing out, a change in the subscribed topics, or a change in partition count.
- *Heartbeat timeout versus processing time?* Heartbeats come from a separate thread, so a long batch does not by itself look like a failure; a separate `max.poll.interval` bounds how long processing may take between polls.
