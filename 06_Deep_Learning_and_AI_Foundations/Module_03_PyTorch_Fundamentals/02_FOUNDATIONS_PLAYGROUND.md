# 🐣 Interactive Foundations Playground: PyTorch Fundamentals & Autograd

> *"A PyTorch Tensor is a chunk of contiguous raw memory viewed through a mathematical lens. Transposing a matrix doesn't move a single byte; it just changes the stride!"*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. Storage, Strides & Contiguity

Inside PyTorch, a tensor consists of two things:
1. **Storage**: A flat, 1-dimensional array of numbers in RAM or GPU VRAM.
2. **Metadata**: Shape, Storage Offset, and **Strides** (how many memory steps to take to advance one index).

Suppose you have a $(3, 3)$ matrix. Its strides are $(3, 1)$ — jump 3 floats to go down a row, jump 1 float to go right a column.
- When you call `tensor.t()`, PyTorch simply swaps the strides to $(1, 3)$. **Zero memory copied! ($O(1)$ operation).**
- But because the memory is no longer sequentially aligned along rows, calling `.view()` will crash!
- Calling `.contiguous()` forces PyTorch to allocate a new flat memory buffer that matches the transposed shape.

---

## 2. Dynamic Computational Graphs: How Autograd Works

PyTorch builds the graph **while your code runs**:
- When `y = x * 2 + 3` runs, PyTorch attaches a `grad_fn` object to `y` pointing to `<AddBackward>`.
- The `<AddBackward>` points to `<MulBackward>`, which points to `x`.
- When you call `loss.backward()`, PyTorch walks this graph in reverse topological order, multiplying local gradients by upstream derivatives.

---

## 3. Custom Autograd Functions

When writing custom GPU operations or numerically sensitive activations, you subclass `torch.autograd.Function` and define:
1. `forward(ctx, x)`: Computes output and saves inputs needed for backward using `ctx.save_for_backward()`.
2. `backward(ctx, grad_output)`: Receives upstream gradient and returns $\nabla_x L$.
