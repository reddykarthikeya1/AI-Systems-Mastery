# Python Exercises: Chapters 16 to 22

> Each chapter has graded exercises with hidden tests: two coding exercises and one debugging exercise. Create your files with `python 01-Python-Mastery/exercises/run.py --init`, edit `exercises/chNN.py`, then run `python 01-Python-Mastery/exercises/run.py NN`. Hints are also available in the terminal with `--hints NN` and walkthroughs with `--explain NN`.

---

## Chapter 16: Event-driven systems: partitioning and consumer offsets (in-memory model of Kafka semantics)

**The three exercises**

- partition_for: stable key -> partition mapping (must not use Python's randomised hash()).
- Consumer: poll/commit with at-least-once delivery and a dedupe helper.
- group_by_partition (debugging): per-key ordering is lost.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 16 - Event-driven systems: partitioning and consumer offsets (in-memory model of Kafka semantics).

1. partition_for: stable key -> partition mapping (must not use Python's randomised hash()).
2. Consumer: poll/commit with at-least-once delivery and a dedupe helper.
3. group_by_partition (debugging): per-key ordering is lost."""

import zlib

def partition_for(key, n):
    """Return a partition in range(n) for a str key. The result must be identical across processes and runs (use zlib.crc32
of the UTF-8 bytes). n < 1 raises ValueError. Same key -> same partition."""
    raise NotImplementedError()

class Consumer:
    """Reads a log (list). poll(max_n) returns up to max_n (offset, record) pairs from the current position and advances it.
    commit() makes the current position durable. restart() resets the position to the last commit (simulating a crash),
    so uncommitted records are delivered again (at-least-once)."""

    def __init__(self, log):
        raise NotImplementedError()

    def poll(self, max_n):
        raise NotImplementedError()

    def commit(self):
        raise NotImplementedError()

    def restart(self):
        raise NotImplementedError()

def dedupe(batches, key=lambda x: x):
    """Given an iterable of records (possibly redelivered), yield each record whose key has not been seen before, in order."""
    raise NotImplementedError()

def group_by_partition(events, n_partitions):
    """events: list of (key, value). Return {partition: [values...]} where each partition keeps events in arrival order
    and all events with the same key land in the same partition."""
    out = {}
    for key, value in events:
        out.setdefault(hash(key) % n_partitions, []).append(value)
    return out
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Consistent partition assignment for event streaming.
2. hash(key) % num_partitions to route keys to deterministic partitions.
3. Ensure records with the same partition key preserve strictly ordered processing.

**Exercise 2**

1. Idempotent consumer deduplication.
2. Track processed message IDs in a bounded window or Redis set.
3. Skip processing if message ID was already committed in the deduplication store.

**Exercise 3**

1. At-least-once delivery with manual offset commit.
2. Process the batch completely before committing offsets to the broker.
3. Guarantees no data loss if worker crashes during processing.

</details>

<details>
<summary>What the hidden tests check</summary>

- `consumer_at_least_once`
- `consumer_dedupe_makes_processing_idempotent`
- `dedupe_order_and_key`
- `group_by_partition_keeps_key_order`
- `partition_is_stable`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import zlib

def partition_for(key, n):
    """Return a partition in range(n) for a str key. The result must be identical across processes and runs (use zlib.crc32
    of the UTF-8 bytes). n < 1 raises ValueError. Same key -> same partition."""
    if n < 1:
        raise ValueError("n must be >= 1")
    return zlib.crc32(key.encode("utf-8")) % n

class Consumer:
    """Reads a log (list). poll(max_n) returns up to max_n (offset, record) pairs from the current position and advances it.
    commit() makes the current position durable. restart() resets the position to the last commit (simulating a crash),
    so uncommitted records are delivered again (at-least-once)."""

    def __init__(self, log):
        self.log = log
        self.position = 0
        self.committed = 0

    def poll(self, max_n):
        batch = [(i, self.log[i]) for i in range(self.position, min(len(self.log), self.position + max_n))]
        self.position += len(batch)
        return batch

    def commit(self):
        self.committed = self.position

    def restart(self):
        self.position = self.committed

def dedupe(batches, key=lambda x: x):
    """Given an iterable of records (possibly redelivered), yield each record whose key has not been seen before, in order."""
    seen = set()
    for r in batches:
        k = key(r)
        if k not in seen:
            seen.add(k)
            yield r

def group_by_partition(events, n_partitions):
    """events: list of (key, value). Return {partition: [values...]} where each partition keeps events in arrival order
    and all events with the same key land in the same partition."""
    out = {}
    for key, value in events:
        out.setdefault(partition_for(key, n_partitions), []).append(value)
    return out
```

**1. partition_for**

*Approach.* zlib.crc32 of the UTF-8 key modulo n is identical in every process. Python's str hash is randomised per process.

*Complexity.* O(len).

*Common wrong answers.*

- hash(key) % n changes between runs, breaking per-key ordering after a restart.
- n must be validated; modulo by zero is an error.

**2. Consumer**

*Approach.* Track a read position and a committed offset. poll advances the position, commit copies it, restart resets to the committed offset, so uncommitted records are redelivered.

*Complexity.* O(batch).

*Common wrong answers.*

- Committing before processing risks loss (at-most-once).
- Redelivery means handlers must dedupe or be idempotent.

**3. group_by_partition (debug)**

*Approach.* Use the stable partition function so all events with a key land in one partition, appended in arrival order.

*Complexity.* O(events).

*Common wrong answers.*

- Using hash() looks correct inside one process and fails across restarts.
- Sorting events by value destroys arrival order.

</details>

---

## Chapter 17: Columnar data engineering (pure Python models of what Polars/DuckDB/Arrow do)

**The three exercises**

- group_sum: aggregate column-wise, without building row dictionaries.
- dictionary_encode / dictionary_decode / run_length_encode: the encodings behind columnar compression.
- column_mean (debugging): the average of a column with NULLs is wrong.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 17 - Columnar data engineering (pure Python models of what Polars/DuckDB/Arrow do).

1. group_sum: aggregate column-wise, without building row dictionaries.
2. dictionary_encode / dictionary_decode / run_length_encode: the encodings behind columnar compression.
3. column_mean (debugging): the average of a column with NULLs is wrong."""

def group_sum(columns, key, value):
    """`columns` is {name: list}. Return {key_value: sum of `value` column} computed by zipping the two columns.
Rows whose value is None are skipped (but the key still appears with 0 if all its values are None)."""
    raise NotImplementedError()

def dictionary_encode(values):
    """Return (dictionary, codes): dictionary lists distinct values in first-seen order, codes[i] is the dictionary index of values[i]."""
    raise NotImplementedError()

def dictionary_decode(dictionary, codes):
    """Inverse of dictionary_encode."""
    raise NotImplementedError()

def run_length_encode(values):
    """[a, a, b, a] -> [(a, 2), (b, 1), (a, 1)]. Empty input gives []."""
    raise NotImplementedError()

def column_mean(values):
    """Mean of the non-None values (zeros count as values). Returns None when there are no non-None values."""
    return sum(v for v in values if v) / len(values)
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Columnar array operations and null handling.
2. Separate valid values array from null bitmask / boolean validity mask.
3. Calculate mean or sum ignoring masked null positions.

**Exercise 2**

1. Run-length encoding (RLE) for repeated categorical data compression.
2. Compress consecutive duplicate values into (value, count) pairs.
3. Decompress by repeating elements into flat array.

**Exercise 3**

1. Dictionary encoding for string columns.
2. Store unique string values in a dictionary array, store indices in integer array.
3. Significantly reduces memory footprint for low-cardinality string columns.

</details>

<details>
<summary>What the hidden tests check</summary>

- `column_mean_nulls_and_zeros`
- `dictionary_roundtrip`
- `group_sum_with_nulls`
- `run_length`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
def group_sum(columns, key, value):
    """`columns` is {name: list}. Return {key_value: sum of `value` column} computed by zipping the two columns.
    Rows whose value is None are skipped (but the key still appears with 0 if all its values are None)."""
    out = {}
    for k, v in zip(columns[key], columns[value]):
        out.setdefault(k, 0)
        if v is not None:
            out[k] += v
    return out

def dictionary_encode(values):
    """Return (dictionary, codes): dictionary lists distinct values in first-seen order, codes[i] is the dictionary index of values[i]."""
    index, codes = {}, []
    for v in values:
        codes.append(index.setdefault(v, len(index)))
    return list(index), codes

def dictionary_decode(dictionary, codes):
    """Inverse of dictionary_encode."""
    return [dictionary[c] for c in codes]

def run_length_encode(values):
    """[a, a, b, a] -> [(a, 2), (b, 1), (a, 1)]. Empty input gives []."""
    out = []
    for v in values:
        if out and out[-1][0] == v:
            out[-1] = (v, out[-1][1] + 1)
        else:
            out.append((v, 1))
    return out

def column_mean(values):
    """Mean of the non-None values (zeros count as values). Returns None when there are no non-None values."""
    present = [v for v in values if v is not None]
    return sum(present) / len(present) if present else None
```

**1. group_sum**

*Approach.* zip the key and value columns and accumulate into a dict, creating the key at 0 so keys whose values are all None still appear.

*Complexity.* O(rows).

*Common wrong answers.*

- Building a list of row dicts first costs memory and defeats the columnar point.
- Treating None as 0 silently changes counts; skip it explicitly.

**2. dictionary_encode / decode / RLE**

*Approach.* Assign each distinct value the next integer in first-seen order; decode indexes back. Run-length encode merges adjacent equal codes.

*Complexity.* O(n).

*Common wrong answers.*

- Sorting the dictionary changes codes and breaks decode symmetry.
- RLE only helps when equal values are adjacent; sort or cluster first.

**3. column_mean (debug)**

*Approach.* Filter on is not None, not on truthiness: zero is a valid value. Divide by the count of present values; return None if there are none.

*Complexity.* O(n).

*Common wrong answers.*

- if v drops zeros; len(values) counts the nulls in the denominator.
- SQL's AVG also ignores NULL, which is the behaviour to match.

</details>

---

## Chapter 18: High-performance computing with NumPy (needs numpy; the runner skips this chapter without it)

**The three exercises**

- pairwise_distances: Euclidean distance matrix with broadcasting and no Python loops.
- moving_average: sliding mean via cumulative sums.
- normalize_columns (debugging): crashes or corrupts its input for integer arrays.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 18 - High-performance computing with NumPy (needs numpy; the runner skips this chapter without it).

1. pairwise_distances: Euclidean distance matrix with broadcasting and no Python loops.
2. moving_average: sliding mean via cumulative sums.
3. normalize_columns (debugging): crashes or corrupts its input for integer arrays."""

import numpy as np

def pairwise_distances(points):
    """`points` is an (n, d) array. Return the (n, n) matrix of Euclidean distances. No Python-level loops over rows."""
    raise NotImplementedError()

def moving_average(x, w):
    """Mean of every window of w consecutive values: a float array of length len(x) - w + 1.
w < 1 or w > len(x) raises ValueError. Must be O(n), not O(n*w)."""
    raise NotImplementedError()

def normalize_columns(a):
    """Return a NEW float array where every column has mean 0 and standard deviation 1 (constant columns become all 0).
    The input array must not be modified."""
    a -= a.mean(axis=0)
    std = a.std(axis=0)
    a /= np.where(std == 0, 1, std)
    return a
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Pairwise Euclidean distance matrix vectorization.
2. Avoid nested Python loops which are 50x-100x slower.
3. Use NumPy broadcasting: diff = A[:, np.newaxis, :] - B[np.newaxis, :, :].

**Exercise 2**

1. Rolling window moving average in linear time.
2. Compute prefix sums (cumulative sum) in O(N).
3. Calculate window sums as prefix[i] - prefix[i - k] in O(1) per step.

**Exercise 3**

1. Column normalization across 2D arrays.
2. Compute column means and standard deviations with axis=0.
3. Subtract mean and divide by standard deviation with numerical epsilon to avoid zero division.

</details>

<details>
<summary>What the hidden tests check</summary>

- `moving_average_is_linear_time`
- `moving_average_values_and_errors`
- `normalize_columns_new_array_and_ints`
- `pairwise_is_vectorised`
- `pairwise_matches_loops`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import numpy as np

def pairwise_distances(points):
    """`points` is an (n, d) array. Return the (n, n) matrix of Euclidean distances. No Python-level loops over rows."""
    p = np.asarray(points, dtype=float)
    diff = p[:, None, :] - p[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))

def moving_average(x, w):
    """Mean of every window of w consecutive values: a float array of length len(x) - w + 1.
    w < 1 or w > len(x) raises ValueError. Must be O(n), not O(n*w)."""
    x = np.asarray(x, dtype=float)
    if w < 1 or w > len(x):
        raise ValueError("bad window")
    c = np.concatenate(([0.0], np.cumsum(x)))
    return (c[w:] - c[:-w]) / w

def normalize_columns(a):
    """Return a NEW float array where every column has mean 0 and standard deviation 1 (constant columns become all 0).
    The input array must not be modified."""
    a = np.asarray(a, dtype=float)
    centered = a - a.mean(axis=0)
    std = centered.std(axis=0)
    return centered / np.where(std == 0, 1, std)
```

**1. pairwise_distances**

*Approach.* Broadcast p[:, None, :] - p[None, :, :], square, sum over the last axis, sqrt. No Python loop over rows.

*Complexity.* Time O(n squared d), memory O(n squared d) for the temporary.

*Common wrong answers.*

- Nested Python loops are 10 to 100 times slower.
- For large n, avoid the 3-D temporary with the (a-b)^2 = a^2 + b^2 - 2ab expansion.

**2. moving_average**

*Approach.* Prefix sums with a leading zero: window sum is c[w:] - c[:-w]. Divide by w.

*Complexity.* O(n).

*Common wrong answers.*

- np.convolve is also O(n w); the prefix-sum version is O(n).
- Large floats accumulate rounding error in cumsum; use float64.

**3. normalize_columns (debug)**

*Approach.* In-place -= on an integer array fails or truncates. Convert to float, build new arrays, and guard zero standard deviation with np.where.

*Complexity.* O(n d).

*Common wrong answers.*

- a /= std divides by zero for constant columns.
- Mutating the caller's array is a hidden side effect.

</details>

---

## Chapter 19: C ABI, struct layout and the boundary with Rust/C extensions (stdlib only)

**The three exercises**

- struct_layout: compute field offsets and total size the way a C compiler does (natural alignment + tail padding).
- pack_record / unpack_record: a fixed binary wire format via `struct`.
- read_u32_le (debugging): reads a little-endian integer incorrectly.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 19 - C ABI, struct layout and the boundary with Rust/C extensions (stdlib only).

1. struct_layout: compute field offsets and total size the way a C compiler does (natural alignment + tail padding).
2. pack_record / unpack_record: a fixed binary wire format via `struct`.
3. read_u32_le (debugging): reads a little-endian integer incorrectly."""

import ctypes
import struct

def struct_layout(fields):
    """`fields` is a list of (name, type) with type in char, short, int, float, long long, double, void*.
Return ({name: offset}, total_size). Each field is aligned to its own size; the total size is rounded up to the
largest alignment among the fields (an empty struct has size 0)."""
    raise NotImplementedError()

def pack_record(rec_id, price, name):
    """Little-endian, no padding: uint32 id, float64 price, 8-byte name (UTF-8, truncated to 8 bytes, NUL padded). Always 20 bytes."""
    raise NotImplementedError()

def unpack_record(data):
    """Inverse of pack_record: returns (id, price, name) with trailing NULs stripped. Wrong length raises ValueError."""
    raise NotImplementedError()

def read_u32_le(buf, offset=0):
    """Read an unsigned 32-bit little-endian integer from bytes `buf` at `offset`."""
    return int.from_bytes(buf[offset:offset + 4], "big")
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. C struct memory alignment and padding calculation.
2. Each field is aligned to a memory address that is a multiple of its size.
3. Total struct size is padded to a multiple of the largest field's alignment.

**Exercise 2**

1. Binary record serialization with struct module.
2. Use struct.pack with explicit endianness prefix ('<' for little-endian).
3. Pad fixed-width strings with trailing NUL bytes and strip them upon unpacking.

**Exercise 3**

1. Endianness decoding bug triage.
2. Check byte order in int.from_bytes(buf, byteorder='little' vs 'big').
3. Verify offset and slice lengths match integer byte size.

</details>

<details>
<summary>What the hidden tests check</summary>

- `read_u32_le`
- `record_roundtrip`
- `record_wrong_length`
- `struct_layout_empty_and_known`
- `struct_layout_matches_ctypes`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import ctypes
import struct

def struct_layout(fields):
    """`fields` is a list of (name, type) with type in char, short, int, float, long long, double, void*.
    Return ({name: offset}, total_size). Each field is aligned to its own size; the total size is rounded up to the
    largest alignment among the fields (an empty struct has size 0)."""
    offsets, pos, biggest = {}, 0, 1
    for name, typ in fields:
        size = _SIZES[typ]
        pos = (pos + size - 1) // size * size
        offsets[name] = pos
        pos += size
        biggest = max(biggest, size)
    return offsets, (pos + biggest - 1) // biggest * biggest if fields else 0

def pack_record(rec_id, price, name):
    """Little-endian, no padding: uint32 id, float64 price, 8-byte name (UTF-8, truncated to 8 bytes, NUL padded). Always 20 bytes."""
    return struct.pack("<Id8s", rec_id, price, name.encode("utf-8")[:8])

def unpack_record(data):
    """Inverse of pack_record: returns (id, price, name) with trailing NULs stripped. Wrong length raises ValueError."""
    if len(data) != 20:
        raise ValueError("record must be 20 bytes")
    rec_id, price, raw = struct.unpack("<Id8s", data)
    return rec_id, price, raw.rstrip(b"\x00").decode("utf-8", errors="ignore")

def read_u32_le(buf, offset=0):
    """Read an unsigned 32-bit little-endian integer from bytes `buf` at `offset`."""
    return int.from_bytes(buf[offset:offset + 4], "little")
```

**1. struct_layout**

*Approach.* Align each field to its own size, add padding before it, and round the final size up to the largest alignment. This is the layout a C compiler uses on common ABIs.

*Complexity.* O(fields).

*Common wrong answers.*

- Forgetting tail padding makes arrays of structs misaligned.
- Alignment rules differ across ABIs; check with ctypes.sizeof on your target.

**2. pack_record / unpack_record**

*Approach.* struct.pack('<Id8s') fixes little-endian byte order and no padding; truncate and NUL-pad the name to 8 bytes; strip NULs when unpacking.

*Complexity.* O(1).

*Common wrong answers.*

- Native byte order ('@') adds padding and varies by machine.
- Decoding a truncated UTF-8 sequence can raise; this exercise ignores errors.

**3. read_u32_le (debug)**

*Approach.* The byte order argument decides meaning: 'little' puts the least significant byte first. Using 'big' reverses the number.

*Complexity.* O(1).

*Common wrong answers.*

- Mixing byte orders is the classic cross-language FFI bug.
- Slice bounds: buf[offset:offset+4] silently returns fewer bytes near the end.

</details>

---

## Chapter 20: Interview Practice: Leaked closures, concurrency rate limiters, and lock ordering

**The three exercises**

- WeakSubscriberRegistry: thread-safe event bus that uses weak references to avoid memory leaks.
- TokenBucketRateLimiter: thread-safe token bucket rate limiter with monotonic time replenishment.
- transfer_funds (debugging): fix lock-order inversion deadlock when transferring between accounts.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 20 - Interview Practice: Leaked closures, concurrency rate limiters, and lock ordering.

1. WeakSubscriberRegistry: thread-safe event bus that uses weak references to avoid memory leaks.
2. TokenBucketRateLimiter: thread-safe token bucket rate limiter with monotonic time replenishment.
3. transfer_funds (debugging): fix lock-order inversion deadlock when transferring between accounts."""

import threading
import time
import weakref

class WeakSubscriberRegistry:
    """Event subscriber registry that prevents circular reference memory leaks using weak references."""

    def __init__(self):
        raise NotImplementedError()

    def register(self, subscriber, callback):
        """Register `callback` for `subscriber`. Drops automatically when `subscriber` is garbage collected."""
        raise NotImplementedError()

    def notify(self, message):
        """Invoke callbacks for all currently alive subscribers, returning list of results."""
        raise NotImplementedError()

    def active_count(self):
        """Return number of currently active, non-collected subscribers."""
        raise NotImplementedError()

class TokenBucketRateLimiter:
    """Thread-safe Token Bucket Rate Limiter."""

    def __init__(self, rate: float, capacity: float):
        raise NotImplementedError()

    def allow_request(self, tokens: float=1.0) -> bool:
        """Return True if requested tokens are available and consumed; False otherwise."""
        raise NotImplementedError()

class Account:

    def __init__(self, account_id: int, balance: float):
        raise NotImplementedError()

def transfer_funds(acc_a, acc_b, amount):
    """Transfer `amount` from `acc_a` to `acc_b` safely using locking."""
    with acc_a.lock:
        with acc_b.lock:
            if acc_a.balance < amount:
                raise ValueError("insufficient funds")
            acc_a.balance -= amount
            acc_b.balance += amount
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Closure memory leak prevention using weak references.
2. Using weakref.WeakKeyDictionary allows subscriber instances to be collected.
3. Call gc.collect() to confirm that dropping external references reclaims memory.

**Exercise 2**

1. Thread-safe Token Bucket Rate Limiter.
2. Compute elapsed time using time.monotonic() and replenish tokens: min(capacity, current + elapsed * rate).
3. Synchronize token check and deduction inside a threading.Lock context manager.

**Exercise 3**

1. Deadlock diagnosis in concurrent fund transfers.
2. Acquiring locks in arbitrary order (e.g. acc_a then acc_b) causes lock-order inversion.
3. Sort lock acquisition canonically by account_id: `first, second = sorted([acc_a, acc_b], key=lambda a: a.account_id)`.

</details>

<details>
<summary>What the hidden tests check</summary>

- `rate_limiter_concurrency`
- `rate_limiter_replenishment`
- `transfer_funds_deadlock_free`
- `weak_subscriber_registry`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import threading
import time
import weakref

class WeakSubscriberRegistry:
    """Event subscriber registry that prevents circular reference memory leaks using weak references."""
    def __init__(self):
        self._subscribers = weakref.WeakKeyDictionary()

    def register(self, subscriber, callback):
        """Register `callback` for `subscriber`. Drops automatically when `subscriber` is garbage collected."""
        self._subscribers[subscriber] = callback

    def notify(self, message):
        """Invoke callbacks for all currently alive subscribers, returning list of results."""
        results = []
        for sub, cb in list(self._subscribers.items()):
            results.append(cb(message))
        return results

    def active_count(self):
        """Return number of currently active, non-collected subscribers."""
        return len(self._subscribers)

class TokenBucketRateLimiter:
    """Thread-safe Token Bucket Rate Limiter."""
    def __init__(self, rate: float, capacity: float):
        self.rate = float(rate)  # tokens added per second
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.last_update = time.monotonic()
        self._lock = threading.Lock()

    def allow_request(self, tokens: float = 1.0) -> bool:
        """Return True if requested tokens are available and consumed; False otherwise."""
        with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.last_update = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

class Account:
    def __init__(self, account_id: int, balance: float):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()

def transfer_funds(acc_a, acc_b, amount):
    """Transfer `amount` from `acc_a` to `acc_b` safely avoiding deadlock via canonical lock ordering."""
    if acc_a.account_id == acc_b.account_id:
        return
    # Order locks by account_id to eliminate lock-order inversion
    first, second = (acc_a, acc_b) if acc_a.account_id < acc_b.account_id else (acc_b, acc_a)
    with first.lock:
        with second.lock:
            if acc_a.balance < amount:
                raise ValueError("insufficient funds")
            acc_a.balance -= amount
            acc_b.balance += amount
```

**1. WeakSubscriberRegistry**

*Approach.* When a long-lived publisher stores closures or callbacks referencing subscriber objects, strong references prevent the subscriber from being collected by the CPython garbage collector even after the caller discards all references. By using weakref.WeakKeyDictionary or weakref.ref, the registry does not increment ob_refcnt, allowing automatic deallocation.

*Complexity.* Time: O(1) registration, O(K) notification where K is active subscribers. Space: O(K).

*Common wrong answers.*

- Using a standard dict mapping subscriber -> callback: creates strong references and permanent memory leaks.
- Modifying the subscribers dictionary during iteration in notify(): leads to RuntimeError: dictionary changed size during iteration. Must iterate over list(self._subscribers.items()).

**2. TokenBucketRateLimiter**

*Approach.* Token bucket smoothly replenishes tokens proportionally to elapsed monotonic time. Rather than running a background thread, calculate replenishment lazily on each request: tokens = min(capacity, tokens + (now - last_update) * rate). Synchronize with a threading.Lock.

*Complexity.* Time: O(1) per request. Space: O(1).

*Common wrong answers.*

- Using time.time() instead of time.monotonic(): system clock adjustments (NTP sync, leap seconds) can cause negative elapsed time or burst anomalies.
- Checking tokens without deducting atomically: race condition allowing two concurrent threads to both consume the last available token.

**3. transfer_funds (Debugging)**

*Approach.* Classic dining philosophers problem. When thread 1 executes transfer(A, B) and thread 2 executes transfer(B, A), thread 1 locks A and waits for B, while thread 2 locks B and waits for A, creating an unresolvable deadlock. Enforcing a global canonical locking order (e.g. always acquiring the lock with the smaller account_id first) guarantees lock acquisition symmetry and eliminates cycles in the resource allocation graph.

*Complexity.* Time: O(1). Space: O(1).

*Common wrong answers.*

- Locking accounts in the order they appear as arguments (acc_a then acc_b).
- Releasing locks prematurely before updating both balances, allowing intermediate inconsistent states to be read.

</details>

---

## Chapter 21: Scenario-based: Circuit breaker, LRU cache with TTL, and async event loop blocking

**The three exercises**

- CircuitBreaker: resilience pattern handling downstream RPC service failures.
- LRUCacheTTL: thread-safe LRU cache with per-item time-to-live and capacity eviction.
- fetch_metrics_async (debugging): fix event-loop stalling synchronous call in an async pipeline.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 21 - Scenario-based: Circuit breaker, LRU cache with TTL, and async event loop blocking.

1. CircuitBreaker: resilience pattern handling downstream RPC service failures.
2. LRUCacheTTL: thread-safe LRU cache with per-item time-to-live and capacity eviction.
3. fetch_metrics_async (debugging): fix event-loop stalling synchronous call in an async pipeline."""

import asyncio
import collections
import time

class CircuitBreakerOpenError(Exception):
    """Raised when an operation is attempted while the circuit breaker is OPEN."""
    pass

class CircuitBreaker:
    """State machine: CLOSED -> (failures >= threshold) -> OPEN -> (after timeout) -> HALF_OPEN -> CLOSED/OPEN."""

    def __init__(self, failure_threshold: int=3, recovery_timeout: float=0.5):
        raise NotImplementedError()

    def call(self, func, *args, **kwargs):
        raise NotImplementedError()

class LRUCacheTTL:
    """LRU cache where keys expire after `ttl` seconds."""

    def __init__(self, maxsize: int=100, default_ttl: float=60.0):
        raise NotImplementedError()

    def get(self, key, default=None):
        raise NotImplementedError()

    def set(self, key, value, ttl=None):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

async def fetch_metrics_async(endpoints):
    """Fetch metrics for endpoints asynchronously."""
    results = []
    for ep in endpoints:
        # BUG: Synchronous time.sleep freezes the entire event loop!
        time.sleep(0.02)
        results.append(f"metrics:{ep}")
    return results
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Resilient Circuit Breaker state transitions.
2. Track consecutive failure counts in CLOSED state; transition to OPEN when threshold reached.
3. After recovery_timeout, enter HALF_OPEN: allow 1 trial call; succeed -> CLOSED, fail -> OPEN.

**Exercise 2**

1. LRU Cache with time-to-live expiration.
2. Use collections.OrderedDict storing (value, expiry_timestamp).
3. On get(), if expired, delete and return default; otherwise move_to_end(). Evict oldest on set().

**Exercise 3**

1. Async event loop freezing bug.
2. Look for synchronous blocking functions like time.sleep() inside async coroutines.
3. Replace with `await asyncio.sleep()` or delegate to `asyncio.to_thread()`.

</details>

<details>
<summary>What the hidden tests check</summary>

- `circuit_breaker_transitions`
- `fetch_metrics_async_concurrency`
- `lru_cache_ttl_eviction`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
import asyncio
import collections
import time

class CircuitBreakerOpenError(Exception):
    """Raised when an operation is attempted while the circuit breaker is OPEN."""
    pass

class CircuitBreaker:
    """State machine: CLOSED -> (failures >= threshold) -> OPEN -> (after timeout) -> HALF_OPEN -> CLOSED/OPEN."""
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 0.5):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"
        self.failure_count = 0
        self.last_state_change = time.monotonic()

    def call(self, func, *args, **kwargs):
        now = time.monotonic()
        if self.state == "OPEN":
            if now - self.last_state_change > self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.last_state_change = now
            else:
                raise CircuitBreakerOpenError("Circuit is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                self.last_state_change = now
            elif self.state == "CLOSED":
                self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            if self.state in ("CLOSED", "HALF_OPEN") and self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_state_change = now
            elif self.state == "HALF_OPEN":
                self.state = "OPEN"
                self.last_state_change = now
            raise

class LRUCacheTTL:
    """LRU cache where keys expire after `ttl` seconds."""
    def __init__(self, maxsize: int = 100, default_ttl: float = 60.0):
        self.maxsize = maxsize
        self.default_ttl = default_ttl
        self._data = collections.OrderedDict()  # key -> (value, expiry_timestamp)

    def get(self, key, default=None):
        if key not in self._data:
            return default
        val, expiry = self._data[key]
        if time.monotonic() > expiry:
            del self._data[key]
            return default
        # Move to end for LRU recency
        self._data.move_to_end(key)
        return val

    def set(self, key, value, ttl=None):
        expiry = time.monotonic() + (ttl if ttl is not None else self.default_ttl)
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = (value, expiry)
        if len(self._data) > self.maxsize:
            self._data.popitem(last=False)  # Evict oldest

    def __len__(self):
        # Prune expired on length query
        now = time.monotonic()
        keys_to_del = [k for k, (_, exp) in self._data.items() if exp < now]
        for k in keys_to_del:
            del self._data[k]
        return len(self._data)

async def fetch_metrics_async(endpoints):
    """Fetch metrics for endpoints concurrently without stalling the event loop."""
    async def _fetch_one(ep):
        await asyncio.sleep(0.02)
        return f"metrics:{ep}"
    tasks = [_fetch_one(ep) for ep in endpoints]
    return await asyncio.gather(*tasks)
```

**1. CircuitBreaker**

*Approach.* Finite state machine with 3 states: CLOSED (normal operations; tracks consecutive failures), OPEN (fails fast immediately by raising CircuitBreakerOpenError without attempting RPC call), and HALF_OPEN (after recovery_timeout, allows a single probe request; success resets to CLOSED, failure flips back to OPEN).

*Complexity.* Time: O(1) overhead per call. Space: O(1).

*Common wrong answers.*

- Resetting failure_count on every single call rather than only on successes or state reset.
- Not handling arbitrary exceptions thrown by downstream calls, leaving the circuit in an inconsistent state.

**2. LRUCacheTTL**

*Approach.* Combines LRU eviction policy with per-item TTL expiration using collections.OrderedDict. Each entry stores (value, expiry_timestamp). On get(), if the current monotonic timestamp exceeds expiry, the item is purged immediately. Accessing a valid item moves it to the end via move_to_end(). When capacity is exceeded, popitem(last=False) evicts the oldest item.

*Complexity.* Time: O(1) get and set. Space: O(maxsize).

*Common wrong answers.*

- Failing to update LRU recency on cache hits: items accessed frequently still get evicted as if they were stale.
- Calculating expiration against wall-clock time rather than monotonic time.

**3. fetch_metrics_async (Debugging)**

*Approach.* Calling blocking synchronous APIs (such as time.sleep, requests.get, or socket.recv) inside an async def coroutine blocks the OS thread executing the event loop. This starves all other concurrent coroutines. The fix replaces time.sleep with await asyncio.sleep, and runs requests concurrently using asyncio.gather().

*Complexity.* Time: O(max(T)) concurrent latency instead of O(sum(T)) serialized. Space: O(N) tasks.

*Common wrong answers.*

- Using time.sleep() instead of asyncio.sleep() in async functions.
- Awaiting each coroutine sequentially inside a for loop rather than launching concurrently via asyncio.gather() or TaskGroup.

</details>

---

## Chapter 22: Capstone Playbook: Metaclass plugin registries, chunked streaming aggregators, and generator cleanup

**The three exercises**

- PluginRegistryMeta: Metaclass that automatically registers and validates plugin classes.
- chunked_stream_aggregator: Memory-bounded generator computing summary metrics across chunks.
- managed_resource_stream (debugging): Fix generator resource handle leak on early break or exception.

<details>
<summary>Starter code (what `python exercises/run.py --init` creates)</summary>

```python
"""Chapter 22 - Capstone Playbook: Metaclass plugin registries, chunked streaming aggregators, and generator cleanup.

1. PluginRegistryMeta: Metaclass that automatically registers and validates plugin classes.
2. chunked_stream_aggregator: Memory-bounded generator computing summary metrics across chunks.
3. managed_resource_stream (debugging): Fix generator resource handle leak on early break or exception."""

from typing import Dict, Any, Iterator, Tuple

class PluginRegistryMeta(type):
    """Metaclass that registers non-abstract plugins in a class-level dictionary."""

    def __new__(mcls, name, bases, namespace):
        raise NotImplementedError()

def chunked_stream_aggregator(stream: Iterator[float], chunk_size: int) -> Iterator[Tuple[int, int, float, float, float]]:
    """Process `stream` in chunks of `chunk_size`.
Yields (chunk_idx, count, mean, min_val, max_val) for each chunk.
Never loads the entire stream into memory at once."""
    raise NotImplementedError()

class MockResource:

    def __init__(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

def managed_resource_stream(resource, items):
    """Yield items while keeping resource open, closing it when done."""
    # BUG: If consumer breaks early or raises, resource.close() is never called!
    for item in items:
        yield item * 2
    resource.close()
```

</details>

<details>
<summary>Hints (open one level at a time, only after a real attempt)</summary>

**Exercise 1**

1. Metaclass-driven plugin validation and discovery.
2. Override __new__(mcls, name, bases, namespace) to inspect class attributes before construction.
3. Verify plugin_name is defined and execute() is callable; register in base class dictionary.

**Exercise 2**

1. Chunked streaming aggregator for out-of-core data processing.
2. Iterate through stream, collecting items into a chunk list up to chunk_size.
3. Yield chunk summary statistics (index, count, mean, min, max) and reset chunk list.

**Exercise 3**

1. Generator resource leak cleanup.
2. If a consumer breaks out of a generator early, code after the loop is never reached.
3. Wrap the generator body in `try...finally: resource.close()` to guarantee cleanup.

</details>

<details>
<summary>What the hidden tests check</summary>

- `chunked_stream_aggregator`
- `managed_resource_stream_guaranteed_cleanup`
- `plugin_registry_meta`

</details>

<details>
<summary>Reference solution and walkthrough (look after you have tried)</summary>

```python
from typing import Dict, Any, Iterator, Tuple

class PluginRegistryMeta(type):
    """Metaclass that registers non-abstract plugins in a class-level dictionary."""
    def __new__(mcls, name, bases, namespace):
        cls = super().__new__(mcls, name, bases, namespace)
        if not hasattr(cls, "_registry"):
            cls._registry = {}
        # Only register concrete subclasses (those that provide a plugin_name)
        plugin_name = namespace.get("plugin_name")
        if plugin_name:
            if not callable(namespace.get("execute")):
                raise TypeError(f"Plugin {name} must implement callable 'execute(self, payload)'")
            cls._registry[plugin_name] = cls
        return cls

def chunked_stream_aggregator(stream: Iterator[float], chunk_size: int) -> Iterator[Tuple[int, int, float, float, float]]:
    """Process `stream` in chunks of `chunk_size`.
    Yields (chunk_idx, count, mean, min_val, max_val) for each chunk.
    Never loads the entire stream into memory at once."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    chunk_idx = 0
    chunk = []
    for item in stream:
        chunk.append(float(item))
        if len(chunk) == chunk_size:
            yield (chunk_idx, len(chunk), sum(chunk) / len(chunk), min(chunk), max(chunk))
            chunk_idx += 1
            chunk = []
    if chunk:
        yield (chunk_idx, len(chunk), sum(chunk) / len(chunk), min(chunk), max(chunk))

class MockResource:
    def __init__(self):
        self.is_open = True

    def close(self):
        self.is_open = False

def managed_resource_stream(resource, items):
    """Yield items from `items`, guaranteeing `resource.close()` is called even on early exit."""
    try:
        for item in items:
            yield item * 2
    finally:
        resource.close()
```

**1. PluginRegistryMeta**

*Approach.* Metaclass intercepts class creation at import/definition time by overriding __new__(mcls, name, bases, namespace). It inspects class attributes and validates that concrete plugin classes provide non-empty plugin_name and a callable execute method, automatically populating the base class registry dictionary.

*Complexity.* Time: O(1) per class declaration. Space: O(P) where P is number of registered plugins.

*Common wrong answers.*

- Validating abstract base classes as plugins: must only register concrete subclasses that specify plugin_name.
- Not checking if execute is callable, allowing non-functional plugin classes to be registered.

**2. chunked_stream_aggregator**

*Approach.* Streaming generator that buffers records into fixed-size batches of chunk_size. It computes summary statistics (count, mean, min, max) for each chunk and yields them immediately, maintaining constant memory overhead regardless of the total stream length.

*Complexity.* Time: O(N) where N is total items in stream. Space: O(chunk_size) strictly bounded.

*Common wrong answers.*

- Converting the stream to list(stream) before chunking, which defeats memory bounding and exhausts RAM on multi-gigabyte datasets.
- Forgetting to yield the final remainder chunk if len(stream) is not an exact multiple of chunk_size.

**3. managed_resource_stream (Debugging)**

*Approach.* Generators can be abandoned by callers using break or raising exceptions before consuming all items. When this happens, execution stops at the yield statement and code after the loop is never reached, leaking underlying resources. Wrapping the generator loop in try...finally guarantees that finally executes when the generator is garbage collected or closed via gen.close() (raising GeneratorExit).

*Complexity.* Time: O(N). Space: O(1).

*Common wrong answers.*

- Placing resource.close() after the for loop without a finally block: early exit leaks the resource handle.
- Catching and suppressing GeneratorExit inside the finally block, which violates CPython generator protocol.

</details>

