#!/usr/bin/env python3
"""Cross-Format Configuration & Data Migration Engine.

Module 07 Turnkey Project Implementation.
Demonstrates pathlib.Path, JSON/CSV/TOML serialization, and Atomic Writes.
"""

from __future__ import annotations

import csv
import json
import tomllib
from pathlib import Path
from typing import Any, ClassVar


class ConfigMigrator:
    """Safely loads, validates, transforms, and exports configurations across formats."""

    SUPPORTED_EXTENSIONS: ClassVar[set[str]] = {".json", ".toml", ".csv"}

    def __init__(self, required_keys: set[str] | None = None) -> None:
        self.required_keys = required_keys or set()

    def load_file(self, file_path: Path) -> dict[str, Any] | list[dict[str, Any]]:
        """Loads data from JSON, TOML, or CSV based on file extension."""
        if not file_path.exists():
            raise FileNotFoundError(f"Source file does not exist: {file_path}")

        suffix = file_path.suffix.lower()
        if suffix not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file format '{suffix}'. Supported: {self.SUPPORTED_EXTENSIONS}")

        if suffix == ".json":
            return json.loads(file_path.read_text(encoding="utf-8"))
        elif suffix == ".toml":
            return tomllib.loads(file_path.read_text(encoding="utf-8"))
        elif suffix == ".csv":
            with open(file_path, encoding="utf-8", newline="") as f:
                return list(csv.DictReader(f))

        raise ValueError(f"Unhandled file extension {suffix}")

    def validate_schema(self, data: dict[str, Any]) -> bool:
        """Validates that all required configuration keys are present."""
        missing = self.required_keys - set(data.keys())
        if missing:
            raise KeyError(f"Configuration missing required schema keys: {missing}")
        return True

    def export_atomic(self, data: Any, target_path: Path) -> None:
        """Atomically serializes data to disk, preventing half-written corrupted files."""
        suffix = target_path.suffix.lower()
        temp_path = target_path.with_suffix(f"{target_path.suffix}.tmp")

        if suffix == ".json":
            content = json.dumps(data, indent=2)
            temp_path.write_text(content, encoding="utf-8")
        elif suffix == ".csv":
            if not isinstance(data, list) or not data:
                raise ValueError("CSV export requires a non-empty list of dictionaries.")
            fieldnames = list(data[0].keys())
            with open(temp_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
                writer.writeheader()
                writer.writerows(data)
        elif suffix == ".toml":
            # Simple flat dictionary TOML emitter
            lines = []
            for k, v in data.items():
                if isinstance(v, str):
                    lines.append(f'{k} = "{v}"')
                elif isinstance(v, bool):
                    lines.append(f"{k} = {'true' if v else 'false'}")
                else:
                    lines.append(f"{k} = {v}")
            temp_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        else:
            raise ValueError(f"Cannot export to unsupported extension '{suffix}'")

        # Atomic replacement: single filesystem transaction
        temp_path.replace(target_path)


def main() -> None:
    print("=" * 65)
    print("      CONFIGURATION & DATA MIGRATOR CLI")
    print("=" * 65)

    migrator = ConfigMigrator(required_keys={"app_name", "environment", "port"})

    source_toml_path = Path("sample_app.toml")
    source_toml_path.write_text(
        'app_name = "AuthService"\nenvironment = "production"\nport = 9000\nenabled = true\n',
        encoding="utf-8",
    )

    print("\n1. Loading and Validating Source TOML Config:")
    config = migrator.load_file(source_toml_path)
    print(f"Loaded Dict: {config}")
    migrator.validate_schema(config)  # type: ignore
    print("Schema Validation: PASSED")

    print("\n2. Atomically Migrating Config to JSON Format:")
    dest_json_path = Path("migrated_config.json")
    migrator.export_atomic(config, dest_json_path)
    print(f"Exported JSON Content:\n{dest_json_path.read_text(encoding='utf-8')}")

    # Cleanup demo files
    source_toml_path.unlink(missing_ok=True)
    dest_json_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
