# Debug Lab 17 - Symptoms

> A logistics planner: container throughput, bottleneck identification and
> driver assignment. Each computation is almost right.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_flow_service.py
echo "exit=$?"
```

There are **3** distinct defects.

---

## Symptom 1 - Throughput matches the depot's total capacity exactly

```
    one-way links (from, to, capacity): [(0, 1, 3), (2, 1, 3), (2, 3, 3), (0, 4, 2), (4, 3, 2)]
    capacity leaving the depot : 5
    capacity entering the port : 5
    planner says throughput is : 5
```

Five out of the depot, five into the port, five moved. Tidy - suspiciously so.

Trace an actual container. It leaves the depot on link `(0, 1)` and arrives at
node 1. Now read the list again and find a link that *leaves* node 1.

**Ask yourself:** how many containers can genuinely reach the port, and what
would the planner have to be assuming to get 5?

---

## Symptom 2 - The bottleneck is reported as no links at all

```
    planner says max throughput is : 2
    planner says the bottleneck is : []
    capacity of those links     : 0
    links remaining after cutting them: 5 of 5
```

The two numbers cannot both be true. Max-flow min-cut says the throughput and
the capacity of the bottleneck set are *the same number*. Here one is 2 and the
other is 0.

An empty cut also means: cut nothing, and the depot is still disconnected from
the port. Obviously false.

**Ask yourself:** the cut is found by exploring outward from the depot and
seeing where you get stuck. Stuck according to *which* set of numbers - the
capacities the links started with, or what is left of them after the flow was
pushed?

---

## Symptom 3 - One driver is given every route

```
    3 drivers, 2 routes, qualifications: [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]
    planner assigned: [(0, 0), (0, 1)]
    routes per driver: {0: 2}
```

Two routes were covered, which is the maximum possible - so the *count* is
right. But driver 0 is doing both of them while drivers 1 and 2 sit idle, and
driver 1 is qualified for both.

A matching is supposed to enforce two limits at once: at most one route per
driver, and at most one driver per route. One of those two is being enforced
and the other is not.

**Ask yourself:** in the flow formulation, which specific number encodes "a
driver may take at most one route"?
