# Debug Lab: Parameter Blows Up During "PyTorch-style" Training Loop
# Course 06 - Module 03 PyTorch Fundamentals

class Param:
    def __init__(self, value):
        self.value = value
        self.grad = 0.0


def zero_grad(params):
    for p in params:
        p.grad = 0.0


def backward(params, xs, ys):
    # simulates d(loss)/d(w) for y_hat = w*x, loss = (y_hat - y)^2
    for x, y in zip(xs, ys):
        pred = sum(p.value for p in params) * x
        error = pred - y
        for p in params:
            p.grad += 2 * error * x


def optimizer_step(params, lr):
    for p in params:
        p.value -= lr * p.grad


def train(xs, ys, epochs=10, lr=0.01):
    params = [Param(0.5)]
    history = []
    for _ in range(epochs):
        backward(params, xs, ys)
        optimizer_step(params, lr)
        history.append(params[0].value)
    return history


if __name__ == "__main__":
    xs = [1.0, 2.0, 3.0, 4.0]
    ys = [2.0, 4.0, 6.0, 8.0]  # true relationship: y = 2x

    weights = train(xs, ys)

    print("Weight after each training step (should settle near 2.0):")
    for i, w in enumerate(weights):
        print(f"  step {i}: w = {w:.4f}")
    print(f"Final weight: {weights[-1]:.4f}")
