# 🐣 Interactive Foundations Playground: Reinforcement Learning & Policy Gradients

> *"Supervised learning is a teacher telling you the right answer. Reinforcement learning is a dog learning tricks: you give a biscuit when it sits, and it figures out how to get more biscuits."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. The Markov Decision Process (MDP)

Everything in RL is framed as an MDP $(S, A, P, R, \gamma)$:
- **State $s$**: Where the agent is (e.g. chess board layout).
- **Action $a$**: What the agent chooses to do (e.g. move pawn to E4).
- **Reward $R$**: The feedback score (+1 for winning, -1 for losing).
- **Discount Factor $\gamma \in [0, 1]$**: How much the agent values immediate rewards vs future rewards. A treat today is worth more than a treat next week!

---

## 2. The Bellman Equation: Self-Consistent Value

How good is state $s$?
The **Bellman Optimality Equation** states:
$$V^*(s) = \max_a \left[ R(s, a) + \gamma \sum_{s'} P(s' \mid s, a) V^*(s') \right]$$
*"The value of your current position is the immediate reward plus the discounted value of the best next position."*

---

## 3. Policy Gradients (REINFORCE) & The Bridge to RLHF

In deep learning, the policy is a neural network $\pi_\theta(a \mid s)$ that outputs probabilities over actions:
- **The Objective**: Maximize expected total reward $J(\theta) = \mathbb{E}[R]$.
- **The Policy Gradient Theorem**:
$$\nabla_\theta J(\theta) = \mathbb{E} \left[ \nabla_\theta \log \pi_\theta(a \mid s) \cdot G_t \right]$$
- If an action led to high reward ($G_t > 0$), we push $\theta$ in the direction that makes that action **more likely**.
- If it led to a penalty ($G_t < 0$), we make that action **less likely**.

**Connection to ChatGPT**: During RLHF (Reinforcement Learning from Human Feedback), the "action" is generating a token, and the "reward" is the score from a human preference reward model!
