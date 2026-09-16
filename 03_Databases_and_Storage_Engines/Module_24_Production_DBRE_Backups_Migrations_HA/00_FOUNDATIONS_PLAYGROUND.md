# Beginner Playground - Production DBRE - Backups, Migrations and HA

> *"An untested backup is not a backup. It is a file you have feelings about."*


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
import hashlib
```

---

## 1. RPO and RTO, in one worked example

- **RPO** - Recovery Point Objective. How much data you may lose, measured in time.
  Set by how often you back up.
- **RTO** - Recovery Time Objective. How long you may be down. Set by how fast you
  can restore.

They are bought separately, and more frequent backups do nothing for RTO.

```python
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
```

---

## 2. The backup you never restored

A backup job that exits 0 has proved one thing: the job exited 0. It has not
proved the file is complete, that it is readable, that the encryption key still
exists, or that anyone knows the restore procedure.

The only test that means anything is a restore into a scratch environment with a
row count and a checksum at the end. Schedule it like any other job.

```python
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
```

---

## 3. Zero-downtime schema change: expand, migrate, contract

Renaming a column in one step breaks every running instance of the old code the
moment it is applied. The safe version is three deploys:

1. **Expand** - add the new column. Old code ignores it; nothing breaks.
2. **Migrate** - write to both, backfill the old rows, then read from the new one.
3. **Contract** - once no code reads the old column, drop it.

Slower, and every intermediate state is one that both old and new code survive.

```python
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
```

---

## 4. High availability is not backup

Replication protects you from a server dying. It does not protect you from a
`DELETE` with a bad `WHERE` clause - that replicates too, faithfully, in
milliseconds.

You need both, and they answer different questions.

```python
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
```

---

## 5. Predict before you run

You take a full backup nightly at 02:00 and incrementals hourly. The
database is destroyed at 14:30. How much data have you lost? Now answer it
again for the case where last night's full backup is silently corrupt.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

The two questions an incident commander asks are "how much did we lose" and
"how long until we are back". Those are RPO and RTO, and if you have not
rehearsed a restore you do not know either number - you have guesses.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
