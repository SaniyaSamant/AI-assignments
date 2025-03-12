import numpy as np
import gym

# Initialize the environment (deterministic for debugging)
env = gym.make("FrozenLake-v1", is_slippery=False, render_mode=None)

# Hyperparameters
alpha = 0.8          # Learning rate
gamma = 0.95         # Discount factor
epsilon = 1.0        # Initial exploration rate
epsilon_min = 0.01   # Minimum exploration rate
epsilon_decay = 0.995
episodes = 10000     # Increased number of episodes

# Initialize Q-table
Q = np.zeros([env.observation_space.n, env.action_space.n])

# Training the agent
for episode in range(episodes):
    state = env.reset()[0]
    done = False

    while not done:
        # Epsilon-greedy action selection
        if np.random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state, :])

        # Perform action and observe outcome
        next_state, reward, done, _, _ = env.step(action)

        # Debug: Print when a reward is received
        if reward > 0:
            print(f"Episode {episode}: Reached goal at state {next_state}")

        # Q-learning update
        Q[state, action] = Q[state, action] + alpha * (
            reward + gamma * np.max(Q[next_state, :]) - Q[state, action]
        )
        state = next_state

    # Decay epsilon
    if epsilon > epsilon_min:
        epsilon *= epsilon_decay

    # Optional: Print progress every 1000 episodes
    if (episode + 1) % 1000 == 0:
        print(f"Episode {episode + 1}/{episodes} completed.")

# Display the learned Q-table
print("\nTrained Q-Table:")
print(Q)
