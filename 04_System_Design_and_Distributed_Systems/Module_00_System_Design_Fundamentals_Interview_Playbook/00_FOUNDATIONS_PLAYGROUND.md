# Beginner Playground - System Design Fundamentals and the Interview Playbook

> *"Nobody orders dinner by shouting 'food!'. You ask what is on the menu, how many are eating and what nobody will touch - and only then decide."*


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

## 1. Four steps, always in this order

1. **Clarify.** What does it do, for whom, at what scale? Write the numbers down.
2. **Estimate.** Requests per second, storage, bandwidth. Rough is fine; absent is not.
3. **Design.** Draw the boxes. Start with the simplest thing that could work.
4. **Trade off.** Say what breaks first, and what you would do about it.

Step 1 is where the interview is won. "Design Twitter" could mean 100 users or
500 million, read-heavy or write-heavy, with or without search. Those are four
different systems.

```python
def clarify(spec):
    required = ["users", "actions_per_user_per_day", "read_write_ratio", "consistency"]
    missing = [q for q in required if q not in spec]
    return missing


half_a_brief = {"users": 10_000_000, "actions_per_user_per_day": 20}
print("still unanswered:", clarify(half_a_brief))
assert clarify(half_a_brief) == ["read_write_ratio", "consistency"]
print("Designing now would be guessing. Ask first.")
```

---

## 2. Back-of-the-envelope, done out loud

You are not trying to be right. You are trying to land within a factor of ten,
because that is what decides whether this runs on one machine or three hundred.

Round everything. 86,400 seconds in a day is 100,000. Keep the arithmetic in your
head and say it out loud.

```python
daily_users = 10_000_000
actions_each = 20
SECONDS_PER_DAY = 100_000            # 86,400, rounded to something you can divide by

daily_actions = daily_users * actions_each
average_qps = daily_actions // SECONDS_PER_DAY
peak_qps = average_qps * 3           # traffic is never flat; 2-5x is the usual range

print(f"{daily_actions:,} actions/day")
print(f"average: {average_qps:,} QPS")
print(f"peak:    {peak_qps:,} QPS")
assert average_qps == 2_000
assert peak_qps == 6_000
print("2,000 QPS is a handful of servers. Knowing that shapes everything after.")
```

---

## 3. Storage, and the number people forget

Bytes per item times items per day times how long you keep them. The part people
skip is *replication* - three copies is standard, so multiply by three at the end.

```python
bytes_per_action = 1_000
days_retained = 365
replicas = 3

raw_per_day = daily_actions * bytes_per_action
total_bytes = raw_per_day * days_retained * replicas

print(f"raw per day: {raw_per_day / 1e9:.1f} GB")
print(f"one year, {replicas} replicas: {total_bytes / 1e12:.0f} TB")
assert 200 < total_bytes / 1e12 < 250
print("Hundreds of terabytes is a design constraint, not a detail.")
```

---

## 4. The ratio that decides the architecture

Ask "how many reads per write" before you draw anything. It is the single number
that most changes the answer.

- **Read-heavy** (a news feed, 100:1): caching and read replicas do the work.
- **Write-heavy** (metrics ingestion, 1:10): queues, batching, and a store built
  for writes such as an LSM tree.

Build a read-heavy design for a write-heavy workload and the cache is useless -
nothing is ever read twice.

```python
def architecture_for(reads, writes):
    ratio = reads / writes
    if ratio > 10:
        return "read-heavy: cache aggressively, add read replicas"
    if ratio < 1:
        return "write-heavy: buffer through a queue, batch, use an LSM store"
    return "balanced: no single trick; measure before optimising"


print("feed  (100 reads : 1 write):", architecture_for(100, 1))
print("metrics (1 read : 10 writes):", architecture_for(1, 10))
assert "cache" in architecture_for(100, 1)
assert "queue" in architecture_for(1, 10)
```

---

## 5. Predict before you run

A product has 10 million daily users who each open it 20 times a day. Before
reading the arithmetic: is the average load closer to 200 requests per second,
2,000, or 2 million? And how far off is the *peak*?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Candidates fail system design interviews by designing immediately. The people
who pass spend the first five minutes establishing what they are building,
because every later decision depends on numbers nobody has stated yet.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
