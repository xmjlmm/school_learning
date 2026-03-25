import numpy as np

class CustomEnvironment:
    def __init__(self):
        self.state = 0
        self.num_states = 4
        self.num_actions = 2

    def reset(self):
        self.state = 0
        return self.state

    def step(self, action):
        if action == 0:
            self.state += 1
        elif action == 1:
            self.state -= 1

        done = False
        if self.state <= 0 or self.state >= self.num_states - 1:
            done = True

        reward = 1 if done else 0
        return self.state, reward, done

# Actor 网络
class Actor:
    def __init__(self, num_states, num_actions):
        self.weights = np.random.rand(num_states, num_actions)

    def predict(self, state):
        logits = np.dot(state, self.weights)
        probs = np.exp(logits) / np.sum(np.exp(logits))
        return probs

    def train(self, state, action, advantage, learning_rate):
        probs = self.predict(state)
        action_probs = probs[action]
        gradient = -action_probs * advantage * state
        self.weights -= learning_rate * gradient[:, np.newaxis]

# Critic 网络
class Critic:
    def __init__(self, num_states):
        self.weights = np.random.rand(num_states, 1)

    def predict(self, state):
        return np.dot(state, self.weights)

    def train(self, state, target_value, learning_rate):
        prediction = self.predict(state)
        error = target_value - prediction
        gradient = -error * state
        self.weights -= learning_rate * gradient[:, np.newaxis]

# A2C 算法
class A2C:
    def __init__(self, num_states, num_actions, learning_rate_actor=0.01, learning_rate_critic=0.01, gamma=0.99):
        self.actor = Actor(num_states, num_actions)
        self.critic = Critic(num_states)
        self.learning_rate_actor = learning_rate_actor
        self.learning_rate_critic = learning_rate_critic
        self.gamma = gamma

    def get_action(self, state):
        probs = self.actor.predict(state)
        action = np.random.choice(range(probs.shape[0]), p=probs)
        return action

    def train(self, state, action, reward, next_state, done):
        # 计算优势函数
        value = self.critic.predict(state)
        next_value = self.critic.predict(next_state) if not done else 0
        advantage = reward + self.gamma * next_value - value

        # 训练 Actor 和 Critic
        self.actor.train(state, action, advantage, self.learning_rate_actor)
        self.critic.train(state, reward + self.gamma * next_value, self.learning_rate_critic)

# 创建环境和 A2C 算法
env = CustomEnvironment()
a2c = A2C(env.num_states, env.num_actions)

# 训练 A2C
for episode in range(1000):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = a2c.get_action(state)
        next_state, reward, done = env.step(action)
        a2c.train(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

    print(f"Episode: {episode+1}, Total Reward: {total_reward}")

