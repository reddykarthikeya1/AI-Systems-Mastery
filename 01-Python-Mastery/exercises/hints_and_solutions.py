"""Progressive 3-level hints and detailed architectural explanations for all 23 chapters.

Usage via run.py:
    python exercises/run.py --hints 00          # view hints for chapter 00
    python exercises/run.py --hints 00 1        # view hints for chapter 00, problem 1
    python exercises/run.py --explain 00        # view full solution explanations for chapter 00
"""

HINTS = {
    "ch00": [
        [
            "Think about object identity (id()) versus value equality (==).",
            "Group indices by id(o) using a dictionary mapping id to a list of indices.",
            "Sort groups with len > 1 by their first index; sort the indices inside ascending."
        ],
        [
            "Recursion is your friend for deep structures.",
            "Check for isinstance(val, (list, dict, tuple)) and recursively snapshot children.",
            "Leave atomic/scalar objects (ints, strings, None) unchanged; rebuild new container instances."
        ],
        [
            "Look at the function signature's default argument: tags=[].",
            "When is `tags=[]` evaluated? At function definition time in CPython!",
            "Replace `tags=[]` with `tags=None` and initialize `tags = []` inside the function body."
        ]
    ],
    "ch01": [
        [
            "Think about dividing a list into slices of size k.",
            "Use range(0, len(items), k) to generate slice start points.",
            "Slice items[i:i+k] and raise ValueError if k <= 0."
        ],
        [
            "Split string lines and partition key-value pairs.",
            "Use s.split('=', 1) so values with '=' aren't truncated.",
            "Typecast booleans, ints, floats and strip extraneous whitespace."
        ],
        [
            "Floating-point math in financial calculations introduces binary precision rounding errors.",
            "Avoid float arithmetic; multiply dollar amounts by 100 or use Decimal/integer cents.",
            "Store and compute monetary values as integer cents."
        ]
    ],
    "ch02": [
        [
            "Preserve first-seen order while filtering out duplicates in O(N).",
            "Use a set to track seen elements while yielding or appending.",
            "In Python 3.7+, dict.fromkeys() preserves insertion order and hashes in O(1)."
        ],
        [
            "An LRU cache evicts the least recently used item when capacity is exceeded.",
            "Use collections.OrderedDict or a doubly-linked list with hash map.",
            "When accessing or updating a key, call move_to_end(key); popitem(last=False) when full."
        ],
        [
            "Finding top K frequent elements efficiently without sorting the full array in O(N log N).",
            "Count frequencies with collections.Counter, then use a min-heap of size K via heapq.",
            "heapq.nlargest(k, counter.items(), key=lambda x: (x[1], x[0])) gives O(N log K)."
        ]
    ],
    "ch03": [
        [
            "Function composition applies functions from right to left or left to right.",
            "functools.reduce(lambda acc, f: f(acc), funcs, initial_value) simplifies chaining.",
            "Return a closure taking *args, **kwargs and passing the intermediate result through funcs."
        ],
        [
            "Late binding in closures: loop variables bind by reference to the enclosing frame.",
            "Default argument values freeze values at closure definition time: `def mul(x, i=i):`.",
            "Alternatively, use a factory function `make_mul(i)` that creates an isolated scope."
        ],
        [
            "Decorators that replace functions lose original docstrings, __name__, and signatures.",
            "functools.wraps(fn) copies __module__, __name__, __qualname__, __doc__, and __annotations__.",
            "Ensure the wrapper function returns the decorated function result and maintains cache hits."
        ]
    ],
    "ch04": [
        [
            "Creating custom immutable value types that support arithmetic and hashing.",
            "Implement __eq__, __hash__, and arithmetic dunder methods (__add__, __sub__).",
            "Ensure objects with equal values produce identical __hash__ values for set/dict storage."
        ],
        [
            "Validating attribute assignment dynamically on classes.",
            "Use the descriptor protocol (__set_name__, __get__, __set__) or __setattr__.",
            "Store private state in instance.__dict__ with private prefixed keys to avoid recursion."
        ],
        [
            "Metaclass or __init_subclass__ registry duplicate handling.",
            "When a subclass registers a duplicate name, validate before adding to the registry dict.",
            "Raise ValueError with descriptive message if the key already exists."
        ]
    ],
    "ch05": [
        [
            "Calculating recursive deep memory size of complex nested objects.",
            "sys.getsizeof() only reports the shallow pointer array container overhead.",
            "Traverse nested containers recursively while maintaining a `seen` set of object ids."
        ],
        [
            "Avoid memory leaks from long-lived event listeners or caches.",
            "Use weakref.ref, weakref.WeakSet, or weakref.WeakKeyDictionary.",
            "When the target object is dereferenced externally, it is cleanly garbage collected."
        ],
        [
            "Circular reference leaks with __del__ methods in older CPython versions.",
            "Break reference cycles explicitly or rely on weakref callbacks instead of __del__.",
            "Call gc.collect() to reclaim cyclic graphs that cannot be freed by refcounts."
        ]
    ],
    "ch06": [
        [
            "Running multiple asynchronous coroutines concurrently with bounded parallelism.",
            "Use asyncio.Semaphore to gate concurrent tasks.",
            "Wrap coroutines in asyncio.create_task and await asyncio.gather(*tasks)."
        ],
        [
            "Returning the first completed result from multiple async requests.",
            "asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED).",
            "Cancel remaining pending tasks to avoid socket leaks and dangling coroutines."
        ],
        [
            "CPU-bound or blocking I/O calls freezing the single-threaded asyncio event loop.",
            "Never call time.sleep(), requests.get(), or heavy math directly inside coroutines.",
            "Offload synchronous blocking code using `await asyncio.to_thread(func, *args)`."
        ]
    ],
    "ch07": [
        [
            "Validating dictionary data at runtime against type annotations.",
            "Inspect __annotations__ and use typing.get_origin / typing.get_args.",
            "Handle Union types, Optional types, and check isinstance() accordingly."
        ],
        [
            "Immutable dataclass-like class versioning.",
            "Freeze attributes by defining __setattr__ to disallow mutation after initialization.",
            "Implement custom __lt__, __gt__, and __eq__ based on parsed semantic version tuples."
        ],
        [
            "TypeVar variance: Covariance (covariant=True) allows subtypes; contravariance allows supertypes.",
            "Immutable sequences should be covariant; mutable containers must be invariant.",
            "Use typing.Protocol for structural duck-typing without inheritance hierarchies."
        ]
    ],
    "ch08": [
        [
            "Parsing semantic version strings and PEP 440 constraints.",
            "Split versions into major, minor, patch tuples and compare lexically.",
            "Handle compatible release operator (~=) by freezing upper bound to next major."
        ],
        [
            "Resolving dependency conflict trees across packages.",
            "Topological sorting / DFS with visited set to detect cycles.",
            "Track constraints per package and raise IncompatibleVersionError on disjoint ranges."
        ],
        [
            "Wheel tag extraction and manylinux compatibility check.",
            "Extract Python tag, ABI tag, and platform tag from wheel filename.",
            "Ensure system glibc version meets or exceeds wheel minimum requirement."
        ]
    ],
    "ch09": [
        [
            "Retrying flaky external calls with exponential backoff and jitter.",
            "Loop with retry count, calculating delay = base * (factor ** attempt) + jitter.",
            "Re-raise the final caught exception if all retry attempts are exhausted."
        ],
        [
            "Thread-safe rate limiter for API clients.",
            "Sliding window counter using collections.deque of timestamps protected by a Lock.",
            "Pop timestamps older than (now - window) before comparing current count against limit."
        ],
        [
            "Mocking async dependencies in pytest without leaking unawaited coroutines.",
            "Use unittest.mock.AsyncMock with return_value or side_effect.",
            "Verify assertions using mock.assert_awaited_once_with()."
        ]
    ],
    "ch10": [
        [
            "Measuring memory growth per line of code.",
            "Use tracemalloc.start(), take snapshot1, execute code, take snapshot2.",
            "Compare snapshots using snapshot2.compare_to(snapshot1, 'lineno')."
        ],
        [
            "Bounded cache avoiding unbounded memory expansion.",
            "Implement a maximum size and drop oldest keys when limit is reached.",
            "Use collections.OrderedDict or cachetools to prevent process OOM crashes."
        ],
        [
            "CPU profiling analysis using cProfile and pstats.",
            "cProfile.Profile(), enable(), code(), disable().",
            "pstats.Stats(prof).strip_dirs().sort_stats('cumulative').print_stats(10)."
        ]
    ],
    "ch11": [
        [
            "Characterizing legacy function behavior with regression tests.",
            "Record input-output pairs across diverse boundary inputs before refactoring.",
            "Ensure refactored version produces identical output for all characterization cases."
        ],
        [
            "Shadow execution / dual-writing pattern.",
            "Call legacy implementation first, call new implementation in try/except.",
            "Compare results; if they differ, log telemetry without impacting caller; return legacy result."
        ],
        [
            "Defensive copying in legacy functions that inadvertently mutate caller arguments.",
            "Check if inputs are sorted or modified in place (e.g. list.sort()).",
            "Use sorted() or defensive copy to ensure input arguments remain unmutated."
        ]
    ],
    "ch12": [
        [
            "Preventing SQL injection and managing transaction atomicity.",
            "Never use f-strings or string concatenation to build SQL statements.",
            "Use parameterized queries with context manager transactions (commit on success, rollback on error)."
        ],
        [
            "Eliminating N+1 queries in relational data access.",
            "Instead of querying children in a loop, query all children using WHERE parent_id IN (...).",
            "Group children in a dictionary keyed by parent_id in O(N) application time."
        ],
        [
            "Verifying database indexes with EXPLAIN QUERY PLAN.",
            "Run EXPLAIN QUERY PLAN before queries in SQLite to confirm 'SEARCH TABLE USING INDEX'.",
            "Ensure queries avoid full table scans ('SCAN TABLE') on large tables."
        ]
    ],
    "ch13": [
        [
            "Pydantic V2 schema validation and custom field sanitization.",
            "Use @field_validator with mode='before' or mode='after'.",
            "Strip whitespace, lowercase email addresses, and raise ValueError on malformed inputs."
        ],
        [
            "Strict models rejecting extra unexpected fields.",
            "model_config = ConfigDict(extra='forbid', str_strip_whitespace=True).",
            "Validate payload with model.model_validate(data) and handle ValidationError."
        ],
        [
            "FastAPI ASGI lifespan context manager.",
            "Use @asynccontextmanager on app lifespan to initialize and teardown DB pools.",
            "Yield control during server execution; cleanup resources in finally block."
        ]
    ],
    "ch14": [
        [
            "Constant-time signature verification preventing timing attacks.",
            "Never compare cryptographic hashes or tokens with standard `==`.",
            "Use hmac.compare_digest(token_a, token_b) to prevent side-channel timing analysis."
        ],
        [
            "JWT token generation and verification.",
            "Encode header, payload, and HMAC-SHA256 signature encoded with base64url.",
            "Verify signature, check 'exp' timestamp against time.time(), and reject 'none' algorithm."
        ],
        [
            "Role-Based Access Control (RBAC) permission resolution.",
            "Support wildcards (e.g., 'reports:*') and role inheritance hierarchies.",
            "Evaluate permissions using set intersections or prefix tree matching."
        ]
    ],
    "ch15": [
        [
            "Priority and delayed task queues with Redis or heapq.",
            "Use heapq with (delivery_timestamp, priority, task_id, task) tuples.",
            "Implement a worker loop that pops tasks only when delivery_timestamp <= now."
        ],
        [
            "Exponential backoff with full jitter for distributed task retry.",
            "delay = random.uniform(0, min(cap, base * 2 ** attempt)).",
            "Prevents thundering herd problem when a shared dependency recovers."
        ],
        [
            "Worker task retry state preservation.",
            "Do not discard failed task parameters; increment retry_count and reschedule.",
            "Move task to Dead Letter Queue (DLQ) when max retries exceeded."
        ]
    ],
    "ch16": [
        [
            "Consistent partition assignment for event streaming.",
            "hash(key) % num_partitions to route keys to deterministic partitions.",
            "Ensure records with the same partition key preserve strictly ordered processing."
        ],
        [
            "Idempotent consumer deduplication.",
            "Track processed message IDs in a bounded window or Redis set.",
            "Skip processing if message ID was already committed in the deduplication store."
        ],
        [
            "At-least-once delivery with manual offset commit.",
            "Process the batch completely before committing offsets to the broker.",
            "Guarantees no data loss if worker crashes during processing."
        ]
    ],
    "ch17": [
        [
            "Columnar array operations and null handling.",
            "Separate valid values array from null bitmask / boolean validity mask.",
            "Calculate mean or sum ignoring masked null positions."
        ],
        [
            "Run-length encoding (RLE) for repeated categorical data compression.",
            "Compress consecutive duplicate values into (value, count) pairs.",
            "Decompress by repeating elements into flat array."
        ],
        [
            "Dictionary encoding for string columns.",
            "Store unique string values in a dictionary array, store indices in integer array.",
            "Significantly reduces memory footprint for low-cardinality string columns."
        ]
    ],
    "ch18": [
        [
            "Pairwise Euclidean distance matrix vectorization.",
            "Avoid nested Python loops which are 50x-100x slower.",
            "Use NumPy broadcasting: diff = A[:, np.newaxis, :] - B[np.newaxis, :, :].",
        ],
        [
            "Rolling window moving average in linear time.",
            "Compute prefix sums (cumulative sum) in O(N).",
            "Calculate window sums as prefix[i] - prefix[i - k] in O(1) per step."
        ],
        [
            "Column normalization across 2D arrays.",
            "Compute column means and standard deviations with axis=0.",
            "Subtract mean and divide by standard deviation with numerical epsilon to avoid zero division."
        ]
    ],
    "ch19": [
        [
            "C struct memory alignment and padding calculation.",
            "Each field is aligned to a memory address that is a multiple of its size.",
            "Total struct size is padded to a multiple of the largest field's alignment."
        ],
        [
            "Binary record serialization with struct module.",
            "Use struct.pack with explicit endianness prefix ('<' for little-endian).",
            "Pad fixed-width strings with trailing NUL bytes and strip them upon unpacking."
        ],
        [
            "Endianness decoding bug triage.",
            "Check byte order in int.from_bytes(buf, byteorder='little' vs 'big').",
            "Verify offset and slice lengths match integer byte size."
        ]
    ],
    "ch20": [
        [
            "Closure memory leak prevention using weak references.",
            "Using weakref.WeakKeyDictionary allows subscriber instances to be collected.",
            "Call gc.collect() to confirm that dropping external references reclaims memory."
        ],
        [
            "Thread-safe Token Bucket Rate Limiter.",
            "Compute elapsed time using time.monotonic() and replenish tokens: min(capacity, current + elapsed * rate).",
            "Synchronize token check and deduction inside a threading.Lock context manager."
        ],
        [
            "Deadlock diagnosis in concurrent fund transfers.",
            "Acquiring locks in arbitrary order (e.g. acc_a then acc_b) causes lock-order inversion.",
            "Sort lock acquisition canonically by account_id: `first, second = sorted([acc_a, acc_b], key=lambda a: a.account_id)`."
        ]
    ],
    "ch21": [
        [
            "Resilient Circuit Breaker state transitions.",
            "Track consecutive failure counts in CLOSED state; transition to OPEN when threshold reached.",
            "After recovery_timeout, enter HALF_OPEN: allow 1 trial call; succeed -> CLOSED, fail -> OPEN."
        ],
        [
            "LRU Cache with time-to-live expiration.",
            "Use collections.OrderedDict storing (value, expiry_timestamp).",
            "On get(), if expired, delete and return default; otherwise move_to_end(). Evict oldest on set()."
        ],
        [
            "Async event loop freezing bug.",
            "Look for synchronous blocking functions like time.sleep() inside async coroutines.",
            "Replace with `await asyncio.sleep()` or delegate to `asyncio.to_thread()`."
        ]
    ],
    "ch22": [
        [
            "Metaclass-driven plugin validation and discovery.",
            "Override __new__(mcls, name, bases, namespace) to inspect class attributes before construction.",
            "Verify plugin_name is defined and execute() is callable; register in base class dictionary."
        ],
        [
            "Chunked streaming aggregator for out-of-core data processing.",
            "Iterate through stream, collecting items into a chunk list up to chunk_size.",
            "Yield chunk summary statistics (index, count, mean, min, max) and reset chunk list."
        ],
        [
            "Generator resource leak cleanup.",
            "If a consumer breaks out of a generator early, code after the loop is never reached.",
            "Wrap the generator body in `try...finally: resource.close()` to guarantee cleanup."
        ]
    ]
}


EXPLANATIONS = {
    "ch20": [
        {
            "problem": "WeakSubscriberRegistry",
            "approach": "When a long-lived publisher stores closures or callbacks referencing subscriber objects, strong references prevent the subscriber from being collected by the CPython garbage collector even after the caller discards all references. By using weakref.WeakKeyDictionary or weakref.ref, the registry does not increment ob_refcnt, allowing automatic deallocation.",
            "complexity": "Time: O(1) registration, O(K) notification where K is active subscribers. Space: O(K).",
            "pitfalls": [
                "Using a standard dict mapping subscriber -> callback: creates strong references and permanent memory leaks.",
                "Modifying the subscribers dictionary during iteration in notify(): leads to RuntimeError: dictionary changed size during iteration. Must iterate over list(self._subscribers.items())."
            ]
        },
        {
            "problem": "TokenBucketRateLimiter",
            "approach": "Token bucket smoothly replenishes tokens proportionally to elapsed monotonic time. Rather than running a background thread, calculate replenishment lazily on each request: tokens = min(capacity, tokens + (now - last_update) * rate). Synchronize with a threading.Lock.",
            "complexity": "Time: O(1) per request. Space: O(1).",
            "pitfalls": [
                "Using time.time() instead of time.monotonic(): system clock adjustments (NTP sync, leap seconds) can cause negative elapsed time or burst anomalies.",
                "Checking tokens without deducting atomically: race condition allowing two concurrent threads to both consume the last available token."
            ]
        },
        {
            "problem": "transfer_funds (Debugging)",
            "approach": "Classic dining philosophers problem. When thread 1 executes transfer(A, B) and thread 2 executes transfer(B, A), thread 1 locks A and waits for B, while thread 2 locks B and waits for A, creating an unresolvable deadlock. Enforcing a global canonical locking order (e.g. always acquiring the lock with the smaller account_id first) guarantees lock acquisition symmetry and eliminates cycles in the resource allocation graph.",
            "complexity": "Time: O(1). Space: O(1).",
            "pitfalls": [
                "Locking accounts in the order they appear as arguments (acc_a then acc_b).",
                "Releasing locks prematurely before updating both balances, allowing intermediate inconsistent states to be read."
            ]
        }
    ],
    "ch21": [
        {
            "problem": "CircuitBreaker",
            "approach": "Finite state machine with 3 states: CLOSED (normal operations; tracks consecutive failures), OPEN (fails fast immediately by raising CircuitBreakerOpenError without attempting RPC call), and HALF_OPEN (after recovery_timeout, allows a single probe request; success resets to CLOSED, failure flips back to OPEN).",
            "complexity": "Time: O(1) overhead per call. Space: O(1).",
            "pitfalls": [
                "Resetting failure_count on every single call rather than only on successes or state reset.",
                "Not handling arbitrary exceptions thrown by downstream calls, leaving the circuit in an inconsistent state."
            ]
        },
        {
            "problem": "LRUCacheTTL",
            "approach": "Combines LRU eviction policy with per-item TTL expiration using collections.OrderedDict. Each entry stores (value, expiry_timestamp). On get(), if the current monotonic timestamp exceeds expiry, the item is purged immediately. Accessing a valid item moves it to the end via move_to_end(). When capacity is exceeded, popitem(last=False) evicts the oldest item.",
            "complexity": "Time: O(1) get and set. Space: O(maxsize).",
            "pitfalls": [
                "Failing to update LRU recency on cache hits: items accessed frequently still get evicted as if they were stale.",
                "Calculating expiration against wall-clock time rather than monotonic time."
            ]
        },
        {
            "problem": "fetch_metrics_async (Debugging)",
            "approach": "Calling blocking synchronous APIs (such as time.sleep, requests.get, or socket.recv) inside an async def coroutine blocks the OS thread executing the event loop. This starves all other concurrent coroutines. The fix replaces time.sleep with await asyncio.sleep, and runs requests concurrently using asyncio.gather().",
            "complexity": "Time: O(max(T)) concurrent latency instead of O(sum(T)) serialized. Space: O(N) tasks.",
            "pitfalls": [
                "Using time.sleep() instead of asyncio.sleep() in async functions.",
                "Awaiting each coroutine sequentially inside a for loop rather than launching concurrently via asyncio.gather() or TaskGroup."
            ]
        }
    ],
    "ch22": [
        {
            "problem": "PluginRegistryMeta",
            "approach": "Metaclass intercepts class creation at import/definition time by overriding __new__(mcls, name, bases, namespace). It inspects class attributes and validates that concrete plugin classes provide non-empty plugin_name and a callable execute method, automatically populating the base class registry dictionary.",
            "complexity": "Time: O(1) per class declaration. Space: O(P) where P is number of registered plugins.",
            "pitfalls": [
                "Validating abstract base classes as plugins: must only register concrete subclasses that specify plugin_name.",
                "Not checking if execute is callable, allowing non-functional plugin classes to be registered."
            ]
        },
        {
            "problem": "chunked_stream_aggregator",
            "approach": "Streaming generator that buffers records into fixed-size batches of chunk_size. It computes summary statistics (count, mean, min, max) for each chunk and yields them immediately, maintaining constant memory overhead regardless of the total stream length.",
            "complexity": "Time: O(N) where N is total items in stream. Space: O(chunk_size) strictly bounded.",
            "pitfalls": [
                "Converting the stream to list(stream) before chunking, which defeats memory bounding and exhausts RAM on multi-gigabyte datasets.",
                "Forgetting to yield the final remainder chunk if len(stream) is not an exact multiple of chunk_size."
            ]
        },
        {
            "problem": "managed_resource_stream (Debugging)",
            "approach": "Generators can be abandoned by callers using break or raising exceptions before consuming all items. When this happens, execution stops at the yield statement and code after the loop is never reached, leaking underlying resources. Wrapping the generator loop in try...finally guarantees that finally executes when the generator is garbage collected or closed via gen.close() (raising GeneratorExit).",
            "complexity": "Time: O(N). Space: O(1).",
            "pitfalls": [
                "Placing resource.close() after the for loop without a finally block: early exit leaks the resource handle.",
                "Catching and suppressing GeneratorExit inside the finally block, which violates CPython generator protocol."
            ]
        }
    ]
}


try:  # written walkthroughs for chapters 00-19 live in their own module
    from _explanations_core import CORE
    EXPLANATIONS = {**CORE, **EXPLANATIONS}
except ImportError:  # pragma: no cover
    pass
