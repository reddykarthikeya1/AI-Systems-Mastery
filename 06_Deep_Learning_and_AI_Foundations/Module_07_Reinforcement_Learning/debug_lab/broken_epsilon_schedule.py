# Debug Lab: Bandit Agent Never Stops Exploring
# Course 06 - Module 07 Reinforcement Learning

import random


def choose_action(q_values, epsilon, rng):
    if rng.random() < epsilon:
        return rng.randrange(len(q_values))
    return max(range(len(q_values)), key=lambda a: q_values[a])


def update_epsilon(epsilon, decay_rate=0.01):
    return epsilon + decay_rate


def train_bandit(true_rewards, episodes=300):
    rng = random.Random(3)
    q_values = [0.0] * len(true_rewards)
    counts = [0] * len(true_rewards)
    epsilon = 0.10
    epsilon_history = []
    for _ in range(episodes):
        action = choose_action(q_values, epsilon, rng)
        reward = true_rewards[action] + rng.uniform(-0.05, 0.05)
        counts[action] += 1
        q_values[action] += (reward - q_values[action]) / counts[action]
        epsilon = min(1.0, update_epsilon(epsilon))
        epsilon_history.append(epsilon)
    return q_values, epsilon_history


if __name__ == "__main__":
    true_rewards = [0.2, 0.5, 0.9, 0.1]  # arm 2 is clearly the best

    q_values, epsilon_history = train_bandit(true_rewards)

    print("Learned Q-values per arm:", [round(q, 3) for q in q_values])
    print(f"Exploration rate (epsilon) at episode 0:   {epsilon_history[0]:.3f}")
    print(f"Exploration rate (epsilon) at episode 50:  {epsilon_history[50]:.3f}")
    print(f"Exploration rate (epsilon) at episode 150: {epsilon_history[150]:.3f}")
    print(f"Exploration rate (epsilon) at episode 299: {epsilon_history[299]:.3f}")
    best_arm = max(range(len(q_values)), key=lambda a: q_values[a])
    print(f"Policy's preferred arm after training: {best_arm} (true best arm is 2)")
