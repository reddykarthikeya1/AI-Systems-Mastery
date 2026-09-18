# Debug Lab Solution & Forensic Post-Mortem

## Incident: Multi-Agent Swarm Hands Off Forever in a Delegation Cycle and Never Reports "Done"

---

### 🔍 Forensic Root Cause Analysis
`run()`'s only way out of `while True:` is `target` being falsy, which triggers the `"Done"` return:

```python
while True:
    target = self.agents[curr].get_next()
    if not target:
        return "Done"
    curr = target
```

It never records which agents have already been visited during this run, so it has no way to distinguish forward progress toward `"Done"` from a cycle that revisits the same agents forever. When the topology hands control back to an agent already seen earlier in the same run (`planner -> researcher -> critic -> planner -> ...`), the loop keeps following the chain indefinitely, because every single `get_next()` call along the cycle keeps returning a truthy next-agent name -- there is simply no check comparing the current agent against the ones that came before it.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class FixedSwarm:
    def __init__(self, agents):
        self.agents = agents

    def run(self, start, msg):
        curr = start
        visited = []
        while True:
            if curr in visited:
                raise RuntimeError(f"Delegation cycle detected: {' -> '.join(visited + [curr])}")
            visited.append(curr)

            target = self.agents[curr].get_next()
            if not target:
                return "Done"
            curr = target
```

Tracking `visited` and checking membership before following each handoff means a returning agent is detected on the very next hop instead of silently looping forever, and the raised error names the exact cycle for fast debugging.

---

### 🛡️ Production Prevention Invariants
1. **Track Visited Nodes in Any Multi-Hop Delegation:** Any graph or swarm traversal must maintain a visited set and fail fast (or escalate to a human) on a repeat, rather than trusting the topology to be acyclic by construction.
2. **Cap Total Handoffs Per Run as a Backstop:** Even with cycle detection in place, enforce a maximum handoff count so a bug in the cycle-detection logic itself cannot still run away.
3. **Emit a Handoff-Count Metric Per Run:** Surface handoffs-per-run on production dashboards so a runaway swarm is caught by monitoring within minutes, not discovered after the API bill spikes.
