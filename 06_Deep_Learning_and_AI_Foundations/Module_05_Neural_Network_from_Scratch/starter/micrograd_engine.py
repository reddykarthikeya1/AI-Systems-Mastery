"""Starter template for Micrograd autograd engine."""
from __future__ import annotations


class Value:
    """Scalar autograd node tracking computational DAG and reverse-mode gradients."""

    def __init__(self, data: float, _children: tuple[Value, ...] = (), _op: str = ""):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __add__(self, other: Value | float) -> Value:
        raise NotImplementedError

    def __mul__(self, other: Value | float) -> Value:
        raise NotImplementedError

    def relu(self) -> Value:
        raise NotImplementedError

    def backward(self) -> None:
        """Topologically sort the computational DAG and execute backward passes in reverse."""
        raise NotImplementedError
