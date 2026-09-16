"""Unit tests for the Configuration & Data Migration Engine."""

from __future__ import annotations

from pathlib import Path

import pytest
from config_migrator import ConfigMigrator


def test_load_and_validate_json(tmp_path: Path) -> None:
    """Test loading and validating valid JSON configuration."""
    migrator = ConfigMigrator(required_keys={"service", "port"})
    json_file = tmp_path / "app.json"
    json_file.write_text('{"service": "payment", "port": 8080}', encoding="utf-8")

    data = migrator.load_file(json_file)
    assert isinstance(data, dict)
    assert data["service"] == "payment"
    assert migrator.validate_schema(data) is True


def test_missing_schema_keys_raises_error() -> None:
    """Test missing required schema keys raises KeyError."""
    migrator = ConfigMigrator(required_keys={"service", "port", "secret_key"})
    invalid_data = {"service": "payment", "port": 8080}

    with pytest.raises(KeyError) as exc_info:
        migrator.validate_schema(invalid_data)
    assert "secret_key" in str(exc_info.value)


def test_atomic_export_json_and_csv(tmp_path: Path) -> None:
    """Test atomic exporting across JSON and CSV formats."""
    migrator = ConfigMigrator()

    # JSON export
    dest_json = tmp_path / "out.json"
    migrator.export_atomic({"key": "val"}, dest_json)
    assert dest_json.exists()
    assert '"key": "val"' in dest_json.read_text(encoding="utf-8")

    # CSV export
    dest_csv = tmp_path / "out.csv"
    table_data = [{"id": "1", "user": "alice"}, {"id": "2", "user": "bob"}]
    migrator.export_atomic(table_data, dest_csv)
    assert dest_csv.exists()
    lines = dest_csv.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "id,user"
    assert lines[1] == "1,alice"


def test_unsupported_extension_raises_value_error(tmp_path: Path) -> None:
    """Test loading file with unsupported extension raises ValueError."""
    migrator = ConfigMigrator()
    bad_file = tmp_path / "config.xml"
    bad_file.write_text("<config></config>", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported file format"):
        migrator.load_file(bad_file)


def test_file_not_found_raises_error(tmp_path: Path) -> None:
    """Test loading nonexistent file raises FileNotFoundError."""
    migrator = ConfigMigrator()
    missing = tmp_path / "does_not_exist.json"
    with pytest.raises(FileNotFoundError):
        migrator.load_file(missing)


def test_load_and_export_toml(tmp_path: Path) -> None:
    """Test loading and exporting TOML configuration format."""
    migrator = ConfigMigrator(required_keys={"database"})
    toml_file = tmp_path / "settings.toml"
    toml_file.write_text('[database]\nhost = "localhost"\nport = 5432\n', encoding="utf-8")

    data = migrator.load_file(toml_file)
    assert isinstance(data, dict)
    assert data["database"]["port"] == 5432
    assert migrator.validate_schema(data) is True

    out_toml = tmp_path / "out.toml"
    migrator.export_atomic(data, out_toml)
    assert out_toml.exists()


def test_load_csv_configuration(tmp_path: Path) -> None:
    """Test loading CSV data produces list of dictionaries."""
    migrator = ConfigMigrator()
    csv_file = tmp_path / "users.csv"
    csv_file.write_text("name,role\nalice,admin\nbob,dev\n", encoding="utf-8")

    data = migrator.load_file(csv_file)
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "alice"
    assert data[1]["role"] == "dev"


def test_atomic_export_cleans_up_temporary_files(tmp_path: Path) -> None:
    """Test atomic export leaves no temp files on disk."""
    migrator = ConfigMigrator()
    dest = tmp_path / "atomic.json"
    migrator.export_atomic({"service": "auth", "version": 2}, dest)
    assert dest.exists()
    assert '"version": 2' in dest.read_text(encoding="utf-8")
    tmp_files = list(tmp_path.glob("*.tmp"))
    assert len(tmp_files) == 0


def test_empty_required_keys_validation() -> None:
    """Test validation with empty required keys always passes."""
    migrator = ConfigMigrator()
    assert migrator.validate_schema({}) is True
    assert migrator.validate_schema({"any": "value"}) is True


def test_load_file_csv_empty_header(tmp_path: Path) -> None:
    """Test loading a CSV file with only headers returns empty list."""
    migrator = ConfigMigrator()
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("col1,col2\n", encoding="utf-8")
    data = migrator.load_file(empty_csv)
    assert data == []
