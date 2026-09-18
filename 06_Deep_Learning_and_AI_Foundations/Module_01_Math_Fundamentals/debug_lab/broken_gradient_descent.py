# Debug Lab: Linear Regression Gradient Descent Divergence
# Course 06 - Module 01 Math Fundamentals

def compute_gradient(x_vals, y_vals, w, b):
    n = len(x_vals)
    dw = sum((w * x + b - y) * x for x, y in zip(x_vals, y_vals)) / n
    db = sum((w * x + b - y) for x, y in zip(x_vals, y_vals)) / n
    return dw, db


def mse_loss(x_vals, y_vals, w, b):
    n = len(x_vals)
    return sum((w * x + b - y) ** 2 for x, y in zip(x_vals, y_vals)) / n


def train(x_vals, y_vals, epochs=6, lr=0.05):
    w, b = 0.0, 0.0
    history = []
    for _ in range(epochs):
        history.append(mse_loss(x_vals, y_vals, w, b))
        dw, db = compute_gradient(x_vals, y_vals, w, b)
        w = w + lr * dw
        b = b + lr * db
    return history, w, b


if __name__ == "__main__":
    xs = [1.0, 2.0, 3.0, 4.0, 5.0]
    ys = [3.0, 5.0, 7.0, 9.0, 11.0]  # true relationship: y = 2x + 1

    history, final_w, final_b = train(xs, ys)

    print("Training a linear model y = w*x + b to fit y = 2x + 1")
    print("MSE loss per epoch:", [round(v, 3) for v in history])
    print(f"Final parameters: w={final_w:.4f}, b={final_b:.4f}")
    print(f"Loss moved from {history[0]:.4f} to {history[-1]:.4f} over {len(history)} epochs")
