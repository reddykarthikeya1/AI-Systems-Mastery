# 🐣 Interactive Foundations Playground: Distributed Data Parallel (DDP)

> *"In naive distributed training, all GPUs compute the backward pass in silence, then freeze completely while synchronizing gradients over the network. PyTorch DDP uses Gradient Bucketing to transmit the top layers' gradients over the wire while the bottom layers are still calculating backprop."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. The Power of Overlapping Communication with Compute

In standard autograd backpropagation:
- Gradients are computed in **reverse topological order** (Layer $L \to \text{Layer } L-1 \to \dots \to \text{Layer } 1$).
- **Naive Training**: Wait until Layer 1 finishes backprop, then launch AllReduce for the entire model. The network sat idle during backprop, and compute sits idle during AllReduce!
- **PyTorch DDP (Overlapped)**:
  - When Layer $L$ computes its gradients, they are ready immediately!
  - Why wait for Layer 1? Put Layer $L$'s gradients in an outgoing mail bucket!
  - As soon as the bucket reaches **25 Megabytes**, fire an asynchronous Ring AllReduce in the background!
  - By the time Layer 1 finishes backprop, 90% of the model's gradients have **already finished synchronizing over the network**!

---

## 2. Gradient Bucketing: Why 25 MB?

Why doesn't DDP send gradients one tensor at a time?
- A model has thousands of small weight tensors (biases, layer norm scales).
- Sending 10,000 tiny packets triggers severe **network latency overhead ($\alpha$)**!
- PyTorch DDP packs gradients into **25 MB buckets**:
  - Big enough to saturate network bandwidth ($\beta$).
  - Small enough to start transmitting early in the backward pass.
