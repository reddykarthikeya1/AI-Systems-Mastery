"""Tests for Unit of Work Transaction Manager."""
from __future__ import annotations

import pytest
from p01_transactional_uow import UnitOfWork


import pytest

def test_transactional_uow():
    uow = UnitOfWork()
    with uow:
        pass
    assert uow.state == 'committed'
    assert uow.log == ['commit']
    uow2 = UnitOfWork()
    with pytest.raises(RuntimeError):
        with uow2:
            raise RuntimeError('db error')
    assert uow2.state == 'rolled_back'
    assert uow2.log == ['rollback']
