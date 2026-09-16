"""Beginner playground for Module 00 - System Design Fundamentals and the Interview Playbook.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations


# ---------------------------------------- 1. Four steps, always in this order
def clarify(spec):
    required = ["users", "actions_per_user_per_day", "read_write_ratio", "consistency"]
    missing = [q for q in required if q not in spec]
    return missing


half_a_brief = {"users": 10_000_000, "actions_per_user_per_day": 20}
print("still unanswered:", clarify(half_a_brief))
assert clarify(half_a_brief) == ["read_write_ratio", "consistency"]
print("Designing now would be guessing. Ask first.")


# ------------------------------------- 2. Back-of-the-envelope, done out loud
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


# ----------------------------------- 3. Storage, and the number people forget
bytes_per_action = 1_000
days_retained = 365
replicas = 3

raw_per_day = daily_actions * bytes_per_action
total_bytes = raw_per_day * days_retained * replicas

print(f"raw per day: {raw_per_day / 1e9:.1f} GB")
print(f"one year, {replicas} replicas: {total_bytes / 1e12:.0f} TB")
assert 200 < total_bytes / 1e12 < 250
print("Hundreds of terabytes is a design constraint, not a detail.")


# --------------------------------- 4. The ratio that decides the architecture
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


print()
print("All checks passed.")
