#!/usr/bin/env python3
"""Make every Track B client read its host/port from the environment.

Why this is necessary
---------------------
The course originally hard-coded `localhost:5432`, `localhost:3306` and friends.
That breaks the moment a learner already runs one of those services natively -
which is common, and was true on the machine this course was built on: a native
PostgreSQL 17 service held port 5432, so the course's tests silently connected
to the *wrong server* and failed password authentication. The symptom ("password
authentication failed") pointed nowhere near the cause.

Hard-coding a well-known port assumes you own the machine. You do not.

After this change every client resolves its connection like so:

    host = os.environ.get("COURSE_PG_HOST", "localhost")
    port = int(os.environ.get("COURSE_PG_PORT", "15432"))

and `docker-compose.yml` publishes on the same non-default host ports, so the
course never collides with a learner's own services. `.env.example` documents
every variable.

Usage::

    python tools/make_ports_configurable.py            # apply
    python tools/make_ports_configurable.py --check     # report only
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# service -> (env prefix, default host port chosen to avoid the standard one)
SERVICES = {
    "postgres": ("COURSE_PG", 15432, 5432),
    "mysql": ("COURSE_MYSQL", 13306, 3306),
    "mongo": ("COURSE_MONGO", 17017, 27017),
    "redis": ("COURSE_REDIS", 16379, 6379),
    "clickhouse": ("COURSE_CLICKHOUSE", 18123, 8123),
    "qdrant": ("COURSE_QDRANT", 16333, 6333),
    "dynamodb": ("COURSE_DYNAMO", 18000, 8000),
    "neo4j": ("COURSE_NEO4J", 17687, 7687),
    "elasticsearch": ("COURSE_ES", 19200, 9200),
    "oracle": ("COURSE_ORACLE", 11521, 1521),
}

# Which default port literal identifies which service inside the Python clients.
PORT_TO_SERVICE = {std: name for name, (_, _, std) in SERVICES.items()}


def patch_compose() -> list[str]:
    """Publish each service on its non-colliding host port."""
    path = ROOT / "docker-compose.yml"
    text = original = path.read_text(encoding="utf-8")
    notes: list[str] = []

    for name, (_prefix, host_port, container_port) in SERVICES.items():
        # "- "5432:5432""  ->  "- "15432:5432""
        pattern = re.compile(rf'(-\s*")(\d+):({container_port})(")')

        def repl(m: re.Match[str]) -> str:
            if m.group(2) == str(host_port):
                return m.group(0)
            return f"{m.group(1)}{host_port}:{m.group(3)}{m.group(4)}"

        new_text, count = pattern.subn(repl, text)
        if count:
            text = new_text
            notes.append(f"  compose: {name} published on {host_port} -> {container_port}")

    if text != original:
        path.write_text(text, encoding="utf-8")
    return notes


def patch_clients() -> list[str]:
    """Rewrite hard-coded defaults in `*_live.py` to read the environment."""
    notes: list[str] = []
    for path in sorted(ROOT.glob("Module_*/project_solution/*_live.py")):
        if path.name.startswith("test_"):
            continue
        text = original = path.read_text(encoding="utf-8")

        for std_port, service in PORT_TO_SERVICE.items():
            prefix, host_port, _ = SERVICES[service]

            # port: int = 5432   ->   port: int | None = None  (resolved below)
            text = re.sub(
                rf"port:\s*int\s*=\s*{std_port}\b",
                f'port: int = int(os.environ.get("{prefix}_PORT", "{host_port}"))',
                text,
            )
            # bare ":5432" inside a URL literal
            text = text.replace(f"localhost:{std_port}", f"localhost:{host_port}")
            text = text.replace(f"127.0.0.1:{std_port}", f"127.0.0.1:{host_port}")

        text = re.sub(
            r'host:\s*str\s*=\s*"localhost"',
            'host: str = os.environ.get("COURSE_DB_HOST", "localhost")',
            text,
        )

        if text != original and not re.search(r"^import os$", text, re.M):
            text = re.sub(
                r"(from __future__ import annotations\n)",
                r"\1\nimport os\n",
                text,
                count=1,
            )

        if text != original:
            path.write_text(text, encoding="utf-8")
            notes.append(f"  client: {path.relative_to(ROOT)}")
    return notes


def write_env_example() -> None:
    lines = [
        "# ---------------------------------------------------------------------------",
        "#  Course service endpoints",
        "# ---------------------------------------------------------------------------",
        "#  Every port below is deliberately NON-STANDARD so the course never collides",
        "#  with a database you already run natively. If you have your own PostgreSQL",
        "#  on 5432 or MySQL on 3306, this course will not touch it.",
        "#",
        "#  Override any value to point the tests at your own instance instead.",
        "#  `docker compose up` publishes exactly these ports.",
        "# ---------------------------------------------------------------------------",
        "",
        'COURSE_DB_HOST=localhost',
        "",
    ]
    for name, (prefix, host_port, container_port) in SERVICES.items():
        lines.append(f"# {name} (container listens on {container_port})")
        lines.append(f"{prefix}_PORT={host_port}")
    lines += [
        "",
        "# Credentials (development only - never reuse these anywhere real)",
        "COURSE_PG_USER=postgres",
        "COURSE_PG_PASSWORD=coursepw",
        "COURSE_PG_DB=coursedb",
        "COURSE_MYSQL_PASSWORD=coursepw",
        "COURSE_NEO4J_AUTH=neo4j/coursepw123",
        "",
    ]
    (ROOT / ".env.example").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        print("check mode: no files written")
        return 0

    notes = patch_compose() + patch_clients()
    write_env_example()
    for note in notes:
        print(note)
    print(f"\npatched {len(notes)} location(s); wrote .env.example")
    return 0


if __name__ == "__main__":
    sys.exit(main())
