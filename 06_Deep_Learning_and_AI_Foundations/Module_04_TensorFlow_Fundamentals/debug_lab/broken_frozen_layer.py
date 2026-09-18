# Debug Lab: Frozen Pretrained Layer Keeps Changing During Fine-Tuning
# Course 06 - Module 04 TensorFlow Fundamentals

class Layer:
    def __init__(self, name, weight, trainable):
        self.name = name
        self.weight = weight
        self.trainable = trainable


def compute_gradients(layers, loss_signal):
    return {layer.name: loss_signal * 0.1 for layer in layers}


def apply_gradients(layers, grads, lr=0.1):
    for layer in layers:
        layer.weight -= lr * grads[layer.name]


def train_step(layers, loss_signal, lr=0.1):
    grads = compute_gradients(layers, loss_signal)
    apply_gradients(layers, grads, lr)


if __name__ == "__main__":
    layers = [
        Layer("pretrained_encoder", weight=1.000, trainable=False),
        Layer("classifier_head", weight=0.500, trainable=True),
    ]

    print("Weights before fine-tuning:")
    for l in layers:
        print(f"  {l.name}: {l.weight:.4f} (trainable={l.trainable})")

    for _ in range(3):
        train_step(layers, loss_signal=1.0)

    print("Weights after 3 fine-tuning steps:")
    for l in layers:
        print(f"  {l.name}: {l.weight:.4f} (trainable={l.trainable})")
