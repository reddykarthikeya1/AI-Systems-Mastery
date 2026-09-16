"""Module 12: Redis Data Structures, Memory & Persistence Engine (Solution).

Implements:
1. SimpleDynamicString (SDS) with binary safety and exponential preallocation.
2. SkipList with level indexing and span calculation for O(log N) rank & range operations.
3. SortedSet (ZSET) integrating hash table (dict) with SkipList.
4. RedisEngine with RESP protocol formatting, BGREWRITEAOF log compaction, and approximate LRU eviction.
"""

from __future__ import annotations

import random
import time
from typing import Literal


class SimpleDynamicString:
    """A binary-safe string buffer mimicking Redis SDS (sds.c)."""

    def __init__(self, init_data: str | bytes = "") -> None:
        raw = init_data.encode("utf-8") if isinstance(init_data, str) else bytes(init_data)
        self._len: int = len(raw)
        self._alloc: int = self._len
        self._buf: bytearray = bytearray(raw)

    @property
    def len(self) -> int:
        return self._len

    @property
    def alloc(self) -> int:
        return self._alloc

    def append(self, data: str | bytes) -> None:
        raw = data.encode("utf-8") if isinstance(data, str) else bytes(data)
        add_len = len(raw)
        if add_len == 0:
            return

        new_len = self._len + add_len
        if new_len > self._alloc:
            # Redis SDS pre-allocation strategy:
            # If new_len < 1MB (1024*1024), double the allocation.
            # If new_len >= 1MB, allocate new_len + 1MB.
            one_mb = 1024 * 1024
            if new_len < one_mb:
                new_alloc = new_len * 2
            else:
                new_alloc = new_len + one_mb

            # Extend underlying buffer with zeros up to new_alloc
            self._buf.extend(b"\x00" * (new_alloc - len(self._buf)))
            self._alloc = new_alloc

        # Copy raw bytes into active slice
        self._buf[self._len : new_len] = raw
        self._len = new_len

    def truncate(self, new_length: int) -> None:
        """Truncate length without deallocating buffer (lazy freeing)."""
        if new_length < self._len:
            self._len = max(0, new_length)

    def to_bytes(self) -> bytes:
        return bytes(self._buf[: self._len])

    def __str__(self) -> str:
        return self.to_bytes().decode("utf-8", errors="replace")

    def __len__(self) -> int:
        return self._len


class SkipListNode:
    """A node in the Redis SkipList."""

    def __init__(self, member: str, score: float, level: int) -> None:
        self.member = member
        self.score = score
        self.forward: list[SkipListNode | None] = [None] * level
        self.span: list[int] = [0] * level


class SkipList:
    """A multi-level probabilistic SkipList for ordered range retrieval and rank queries."""

    def __init__(self, max_level: int = 16, p: float = 0.5) -> None:
        self.max_level = max_level
        self.p = p
        self.level = 1
        self.length = 0
        # Sentinel head node with max_level forward pointers
        self.head = SkipListNode(member="", score=float("-inf"), level=self.max_level)
        for i in range(self.max_level):
            self.head.span[i] = 0

    def random_level(self) -> int:
        lvl = 1
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, member: str, score: float) -> SkipListNode:
        update: list[SkipListNode] = [self.head] * self.max_level
        rank: list[int] = [0] * self.max_level

        curr = self.head
        for i in range(self.level - 1, -1, -1):
            rank[i] = 0 if i == self.level - 1 else rank[i + 1]
            while curr.forward[i] and (
                curr.forward[i].score < score
                or (curr.forward[i].score == score and curr.forward[i].member < member)
            ):
                rank[i] += curr.span[i]
                curr = curr.forward[i]  # type: ignore[assignment]
            update[i] = curr

        lvl = self.random_level()
        if lvl > self.level:
            for i in range(self.level, lvl):
                rank[i] = 0
                update[i] = self.head
                update[i].span[i] = self.length
            self.level = lvl

        new_node = SkipListNode(member=member, score=score, level=lvl)
        for i in range(lvl):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

            # Update span based on traversed ranks
            new_node.span[i] = update[i].span[i] - (rank[0] - rank[i])
            update[i].span[i] = (rank[0] - rank[i]) + 1

        # Increment span for untouched upper levels
        for i in range(lvl, self.level):
            update[i].span[i] += 1

        self.length += 1
        return new_node

    def delete(self, member: str, score: float) -> bool:
        update: list[SkipListNode] = [self.head] * self.max_level

        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] and (
                curr.forward[i].score < score
                or (curr.forward[i].score == score and curr.forward[i].member < member)
            ):
                curr = curr.forward[i]  # type: ignore[assignment]
            update[i] = curr

        target = curr.forward[0]
        if target is None or target.score != score or target.member != member:
            return False

        for i in range(self.level):
            if update[i].forward[i] is target:
                update[i].span[i] += target.span[i] - 1
                update[i].forward[i] = target.forward[i]
            else:
                update[i].span[i] -= 1

        while self.level > 1 and self.head.forward[self.level - 1] is None:
            self.level -= 1

        self.length -= 1
        return True

    def range_by_score(self, min_score: float, max_score: float) -> list[tuple[str, float]]:
        results: list[tuple[str, float]] = []
        curr = self.head

        # Jump forward using highest possible levels until right before min_score
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] and curr.forward[i].score < min_score:
                curr = curr.forward[i]  # type: ignore[assignment]

        curr = curr.forward[0]  # type: ignore[assignment]
        while curr and curr.score <= max_score:
            results.append((curr.member, curr.score))
            curr = curr.forward[0]

        return results

    def get_rank(self, member: str, score: float) -> int:
        rank = 0
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] and (
                curr.forward[i].score < score
                or (curr.forward[i].score == score and curr.forward[i].member <= member)
            ):
                rank += curr.span[i]
                curr = curr.forward[i]  # type: ignore[assignment]

            if curr.member == member and curr.score == score:
                return rank
        return 0


class SortedSet:
    """Redis Sorted Set (ZSET) combining Dict (O(1) lookup) + SkipList (O(log N) range & rank)."""

    def __init__(self) -> None:
        self._dict: dict[str, float] = {}
        self._sl: SkipList = SkipList()

    def zadd(self, member: str, score: float) -> bool:
        if member in self._dict:
            old_score = self._dict[member]
            if old_score == score:
                return False
            self._sl.delete(member, old_score)
            self._dict[member] = score
            self._sl.insert(member, score)
            return False

        self._dict[member] = score
        self._sl.insert(member, score)
        return True

    def zscore(self, member: str) -> float | None:
        return self._dict.get(member)

    def zrangebyscore(self, min_score: float, max_score: float) -> list[tuple[str, float]]:
        return self._sl.range_by_score(min_score, max_score)

    def zrank(self, member: str) -> int | None:
        if member not in self._dict:
            return None
        rank = self._sl.get_rank(member, self._dict[member])
        return rank if rank > 0 else None

    def zrem(self, member: str) -> bool:
        if member not in self._dict:
            return False
        score = self._dict.pop(member)
        self._sl.delete(member, score)
        return True

    def __len__(self) -> int:
        return len(self._dict)


def format_resp_command(*args: str) -> str:
    """Format command arguments into Redis Serialization Protocol (RESP) Array."""
    parts = [f"*{len(args)}\r\n"]
    for arg in args:
        encoded = arg.encode("utf-8")
        parts.append(f"${len(encoded)}\r\n{arg}\r\n")
    return "".join(parts)


class RedisEngine:
    """Core in-memory Redis Engine featuring SDS, ZSET, LRU eviction, and AOF rewrite."""

    def __init__(
        self,
        max_memory_bytes: int = 10_000_000,
        eviction_policy: Literal["noeviction", "allkeys-lru"] = "allkeys-lru",
        maxmemory_samples: int = 5,
    ) -> None:
        self.max_memory_bytes = max_memory_bytes
        self.eviction_policy = eviction_policy
        self.maxmemory_samples = maxmemory_samples

        self._strings: dict[str, SimpleDynamicString] = {}
        self._zsets: dict[str, SortedSet] = {}
        self._access_times: dict[str, float] = {}
        self.aof_log: list[str] = []

    def _estimate_memory(self) -> int:
        total = 0
        for k, v in self._strings.items():
            total += len(k) + v.alloc + 64
        for k, z in self._zsets.items():
            total += len(k) + len(z) * 64 + 128
        return total

    def evict_if_needed(self) -> str | None:
        if self.eviction_policy != "allkeys-lru":
            return None

        if self._estimate_memory() <= self.max_memory_bytes:
            return None

        all_keys = list(self._access_times.keys())
        if not all_keys:
            return None

        sample_size = min(self.maxmemory_samples, len(all_keys))
        sampled_keys = random.sample(all_keys, sample_size)
        oldest_key = min(sampled_keys, key=lambda k: self._access_times.get(k, 0.0))

        if oldest_key in self._strings:
            del self._strings[oldest_key]
        elif oldest_key in self._zsets:
            del self._zsets[oldest_key]

        del self._access_times[oldest_key]
        return oldest_key

    def set(self, key: str, value: str | bytes) -> None:
        self.evict_if_needed()
        self._strings[key] = SimpleDynamicString(value)
        self._access_times[key] = time.time()
        val_str = value if isinstance(value, str) else value.decode("utf-8", errors="replace")
        self.aof_log.append(format_resp_command("SET", key, val_str))

    def get(self, key: str) -> bytes | None:
        if key in self._strings:
            self._access_times[key] = time.time()
            return self._strings[key].to_bytes()
        return None

    def incrby(self, key: str, amount: int = 1) -> int:
        current_bytes = self.get(key)
        current_val = int(current_bytes.decode("utf-8")) if current_bytes is not None else 0
        new_val = current_val + amount
        self._strings[key] = SimpleDynamicString(str(new_val))
        self._access_times[key] = time.time()
        self.aof_log.append(format_resp_command("INCRBY", key, str(amount)))
        return new_val

    def zadd(self, key: str, member: str, score: float) -> bool:
        self.evict_if_needed()
        if key not in self._zsets:
            self._zsets[key] = SortedSet()
        is_new = self._zsets[key].zadd(member, score)
        self._access_times[key] = time.time()
        self.aof_log.append(format_resp_command("ZADD", key, str(score), member))
        return is_new

    def zscore(self, key: str, member: str) -> float | None:
        if key in self._zsets:
            self._access_times[key] = time.time()
            return self._zsets[key].zscore(member)
        return None

    def zrangebyscore(self, key: str, min_score: float, max_score: float) -> list[tuple[str, float]]:
        if key in self._zsets:
            self._access_times[key] = time.time()
            return self._zsets[key].zrangebyscore(min_score, max_score)
        return []

    def zrank(self, key: str, member: str) -> int | None:
        if key in self._zsets:
            self._access_times[key] = time.time()
            return self._zsets[key].zrank(member)
        return None

    def bgrewriteaof(self) -> list[str]:
        """Compact RAM keyspace into minimal canonical RESP commands."""
        compacted: list[str] = []
        for key, sds in self._strings.items():
            compacted.append(format_resp_command("SET", key, sds.to_bytes().decode("utf-8", errors="replace")))

        for key, zset in self._zsets.items():
            for member, score in zset.zrangebyscore(float("-inf"), float("inf")):
                compacted.append(format_resp_command("ZADD", key, str(score), member))

        return compacted
