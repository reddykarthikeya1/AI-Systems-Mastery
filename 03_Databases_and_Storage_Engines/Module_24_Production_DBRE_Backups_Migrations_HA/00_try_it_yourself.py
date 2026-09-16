"""Beginner playground for Module 24 - Production DBRE - Backups, Migrations and HA.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import hashlib

# -------------------------------------- 1. RPO and RTO, in one worked example
full_backup_at = 2.0                    # 02:00
incrementals = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0]
disaster_at = 14.5                      # 14:30

last_good = max([full_backup_at] + [t for t in incrementals if t <= disaster_at])
rpo_hours = disaster_at - last_good
print(f"last usable backup: {last_good:.1f}, disaster: {disaster_at:.1f}")
print(f"data lost (RPO): {rpo_hours * 60:.0f} minutes")
assert rpo_hours == 0.5

restore_full = 40                       # minutes to load the full backup
restore_each_incremental = 3
rto_minutes = restore_full + restore_each_incremental * len(incrementals)
print(f"time to be back (RTO): {rto_minutes} minutes")
assert rto_minutes == 76
print("Hourly incrementals cut the RPO and INCREASED the RTO. Both are choices.")


# ------------------------------------------- 2. The backup you never restored
live_rows = [f"row-{i}" for i in range(1_000)]


def checksum(rows):
    return hashlib.sha256("|".join(rows).encode()).hexdigest()[:12]


good_backup = list(live_rows)
truncated_backup = live_rows[:700]      # the job still exited 0


def verify(backup):
    return len(backup) == len(live_rows) and checksum(backup) == checksum(live_rows)


print("good backup verifies:     ", verify(good_backup))
print("truncated backup verifies:", verify(truncated_backup))
assert verify(good_backup)
assert not verify(truncated_backup), "caught in a drill, not during an outage"


# ------------------ 3. Zero-downtime schema change: expand, migrate, contract
table = [{"id": 1, "name": "Ana Ruiz"}, {"id": 2, "name": "Bo Chen"}]


def old_code_reads(row):
    return row["name"]


def new_code_reads(row):
    return f"{row['first_name']} {row['last_name']}"


for row in table:                                   # 1. EXPAND
    row["first_name"] = None
    row["last_name"] = None
assert all(old_code_reads(r) for r in table), "old code is unaffected"

for row in table:                                   # 2. MIGRATE (backfill)
    first, last = row["name"].split(" ", 1)
    row["first_name"], row["last_name"] = first, last
assert all(old_code_reads(r) == new_code_reads(r) for r in table), "both work at once"
print("during the overlap both versions read correctly:",
      [new_code_reads(r) for r in table])

for row in table:                                   # 3. CONTRACT
    del row["name"]
assert all(new_code_reads(r) for r in table)
print("after contract:", [new_code_reads(r) for r in table])


# ----------------------------------------- 4. High availability is not backup
primary_table = {1: "alice", 2: "bob", 3: "cara"}
replica_table = dict(primary_table)
last_night_backup = dict(primary_table)

del primary_table[2]                    # DELETE FROM users WHERE id = 2  (oops)
replica_table = dict(primary_table)     # replicated instantly and correctly

print("primary:", primary_table)
print("replica:", replica_table)
print("backup: ", last_night_backup)
assert 2 not in replica_table, "the replica has the same mistake"
assert 2 in last_night_backup, "only the backup remembers row 2"
print("HA covers hardware failure. Backups cover human failure. Buy both.")


print()
print("All checks passed.")
