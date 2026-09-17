"""Tests for Subclass Auto-Registration Metaclass."""
from __future__ import annotations

import pytest
from p01_class_registry_meta import RegistryMeta


def test_class_registry_meta():
    class Base(metaclass=RegistryMeta): pass
    class Worker(Base): pass
    class Server(Base): pass
    assert 'Worker' in RegistryMeta.registry
    assert 'Server' in RegistryMeta.registry
