# 🐣 Interactive Foundations Playground: Multivariable Calculus for Learning

> *"Calculus in Machine Learning is simple: Gradients point uphill, Jacobians measure vector stretches, and Hessians tell you if you are resting safely at the bottom of a bowl or balanced on a knife-edge saddle."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. The Gradient: Nature's Uphill Compass

Imagine standing on a foggy mountainside. You cannot see the summit, but you can feel the slope of the ground beneath your feet.
- The **Gradient** $\nabla f(x)$ is a vector pointing in the direction of **steepest uphill ascent**.
- Its magnitude $\|\nabla f(x)\|$ tells you how steep the hill is.
- In machine learning, we want to **minimize** loss (walk down the valley to safety), so we take a step in the opposite direction:
$$x_{new} = x - \alpha \nabla f(x)$$
That is **Gradient Descent**!

---

## 2. The Jacobian: The Multi-Output Stretch Matrix

When a function takes a single number and outputs a single number, its derivative is a single slope $f'(x)$.
- What if a function takes a vector of $n$ inputs and produces a vector of $m$ outputs (like a neural network layer or Softmax)?
$$f: \mathbb{R}^n \to \mathbb{R}^m$$
- The derivative is a matrix of all possible partial derivatives called the **Jacobian** $J \in \mathbb{R}^{m \times n}$:
$$J_{ij} = \frac{\partial f_i}{\partial x_j}$$
- The Jacobian tells you: *"If I tweak input knob $j$ by 0.01, how much does output gauge $i$ twitch?"*

---

## 3. The Softmax Derivative: Clean Analytical Beauty

Softmax turns raw logits $z$ into probabilities:
$$S_i = \frac{e^{z_i}}{\sum_k e^{z_k}}$$
Its Jacobian has a famous, elegant form:
$$\frac{\partial S_i}{\partial z_j} = \begin{cases} S_i(1 - S_i) & \text{if } i = j \\ -S_i S_j & \text{if } i \neq j \end{cases} = S_i (\delta_{ij} - S_j)$$
In matrix form: $J = \text{diag}(S) - S S^T$!

---

## 4. The Hessian: Bowl vs Saddle Curvature

The **Hessian** $H$ is the matrix of second derivatives:
$$H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}$$
- If all eigenvalues of $H$ are positive ($H$ is positive definite), the surface is a **bowl curving up** $\implies$ **Local Minimum**!
- If some are positive and some are negative, you are at a **saddle point**!
