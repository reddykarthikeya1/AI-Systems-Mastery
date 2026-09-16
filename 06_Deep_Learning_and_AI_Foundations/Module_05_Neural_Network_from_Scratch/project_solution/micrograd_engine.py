"""Production solution for Micrograd autograd engine."""
from __future__ import annotations


class Value:
    """Scalar autograd node tracking computational DAG and reverse-mode gradients."""

    def __init__(self, data: float, _children: tuple[Value, ...] = (), _op: str = ""):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __repr__(self) -> str:
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"

    def __add__(self, other: Value | float) -> Value:
        other_val = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other_val.data, (self, other_val), "+")

        def _backward():
            self.grad += 1.0 * out.grad
            other_val.grad += 1.0 * out.grad

        out._backward = _backward
        return out

    def __radd__(self, other: Value | float) -> Value:
        return self + other

    def __mul__(self, other: Value | float) -> Value:
        other_val = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other_val.data, (self, other_val), "*")

        def _backward():
            self.grad += other_val.data * out.grad
            other_val.grad += self.data * out.grad

        out._backward = _backward
        return out

    def __rmul__(self, other: Value | float) -> Value:
        return self * other

    def __sub__(self, other: Value | float) -> Value:
        return self + (-1.0 * other)

    def __rsub__(self, other: Value | float) -> Value:
        return (other if isinstance(other, Value) else Value(other)) - self

    def __pow__(self, other: float) -> Value:
        assert isinstance(other, (int, float)), "Power must be int or float."
        out = Value(self.data**other, (self,), f"**{other}")

        def _backward():
            self.grad += (other * (self.data ** (other - 1))) * out.grad

        out._backward = _backward
        return out

    def relu(self) -> Value:
        out = Value(max(0.0, self.data), (self,), "ReLU")

        def _backward():
            self.grad += (1.0 if self.data > 0.0 else 0.0) * out.grad

        out._backward = _backward
        return out

    def backward(self) -> None:
        # Build topological graph
        topo: list[Value] = []
        visited: set[Value] = set()

        def build_topo(v: Value):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        self.grad = 1.0
        for node in reversed(topo):
            node._backward()
