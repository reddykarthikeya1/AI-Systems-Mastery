# Debug Lab: Hand-Rolled Backprop Network Fails to Learn XOR
# Course 06 - Module 05 Neural Network from Scratch

import math
import random


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(s):
    return s * (1.0 - s)


def forward(x, w1, w2):
    h = sigmoid(sum(wi * xi for wi, xi in zip(w1, x)))
    o = sigmoid(h * w2)
    return h, o


def train(data, epochs=400, lr=0.5):
    random.seed(1)
    w1 = [random.uniform(-1, 1) for _ in range(2)]
    w2 = random.uniform(-1, 1)
    losses = []
    for _ in range(epochs):
        total_loss = 0.0
        for x, y in data:
            h, o = forward(x, w1, w2)
            error = o - y
            total_loss += error ** 2
            d_out = error * sigmoid_derivative(o)
            d_hidden = sigmoid_derivative(h)
            w2 -= lr * d_out * h
            for i in range(len(w1)):
                w1[i] -= lr * d_hidden * x[i]
        losses.append(total_loss / len(data))
    return losses, w1, w2


if __name__ == "__main__":
    xor_data = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
    losses, w1, w2 = train(xor_data)

    print("XOR training loss every 100 epochs:")
    for i in range(0, len(losses), 100):
        print(f"  epoch {i}: loss = {losses[i]:.4f}")
    print(f"Final loss: {losses[-1]:.4f}")

    print("\nPredictions after training:")
    for x, y in xor_data:
        _, o = forward(x, w1, w2)
        print(f"  input={x} target={y} predicted={o:.3f}")
