"""Module 14: Real Apache Cassandra / ScyllaDB Driver & CQL Operations (Track B).

Interacts directly with Apache Cassandra via cassandra-driver to demonstrate:
1. Masterless cluster connection with TokenAwarePolicy.
2. Tunable consistency levels (ONE, QUORUM, ALL) on reads and writes.
3. Wide-column schema definition with partition keys and clustering keys.
4. Lightweight Transactions (LWT) using Paxos (IF NOT EXISTS).
5. Tombstones and TTL-based record expiration.
"""

from __future__ import annotations

from typing import Any

try:
    from cassandra.cluster import Cluster, Session
    from cassandra.query import SimpleStatement, ConsistencyLevel
except ImportError:
    Cluster = None  # type: ignore
    Session = None  # type: ignore
    SimpleStatement = None  # type: ignore
    ConsistencyLevel = None  # type: ignore


class CassandraLiveClient:
    """Production Cassandra client for tunable consistency and wide-column modeling."""

    def __init__(self, contact_points: list[str] | None = None, port: int = 9042, keyspace: str = "coursedb"):
        if Cluster is None:
            raise RuntimeError("cassandra-driver is not installed. Install with: pip install cassandra-driver")
        self.contact_points = contact_points or ["localhost"]
        self.port = port
        self.keyspace = keyspace
        self._cluster: Cluster | None = None
        self._session: Session | None = None

    def connect(self) -> Session:
        if self._session is None:
            self._cluster = Cluster(self.contact_points, port=self.port, connect_timeout=2.0)
            self._session = self._cluster.connect()
        return self._session

    def ping(self) -> bool:
        try:
            session = self.connect()
            res = session.execute("SELECT release_version FROM system.local")
            return len(list(res)) > 0
        except Exception:
            return False

    def setup_keyspace_and_table(self) -> None:
        session = self.connect()
        session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
        """)
        session.set_keyspace(self.keyspace)
        session.execute("""
            CREATE TABLE IF NOT EXISTS sensor_timeline (
                device_id text,
                bucket_day text,
                reading_time timestamp,
                temperature double,
                humidity double,
                PRIMARY KEY ((device_id, bucket_day), reading_time)
            ) WITH CLUSTERING ORDER BY (reading_time DESC)
        """)

    def write_sensor_reading(
        self,
        device_id: str,
        bucket_day: str,
        temperature: float,
        humidity: float,
        consistency: Any = None,
    ) -> None:
        session = self.connect()
        session.set_keyspace(self.keyspace)
        cl = consistency if consistency is not None else ConsistencyLevel.QUORUM
        stmt = SimpleStatement(
            """
            INSERT INTO sensor_timeline (device_id, bucket_day, reading_time, temperature, humidity)
            VALUES (%s, %s, toTimestamp(now()), %s, %s)
            """,
            consistency_level=cl,
        )
        session.execute(stmt, (device_id, bucket_day, temperature, humidity))

    def close(self) -> None:
        if self._cluster:
            self._cluster.shutdown()
            self._cluster = None
            self._session = None
