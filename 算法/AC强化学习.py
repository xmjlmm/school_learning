import numpy as np
import tensorflow as tf
import gym

# 定义 Actor 网络
class ActorNetwork(tf.keras.Model):
    def __init__(self, state_dim, action_dim):
        super(ActorNetwork, self).__init__()
        self.dense1 = tf.keras.layers.Dense(64, activation='relu')
        self.dense2 = tf.keras.layers.Dense(64, activation='relu')
        self.output_layer = tf.keras.layers.Dense(action_dim, activation='softmax')

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return self.output_layer(x)

# 定义 Critic 网络
class CriticNetwork(tf.keras.Model):
    def __init__(self, state_dim):
        super(CriticNetwork, self).__init__()
        self.dense1 = tf.keras.layers.Dense(64, activation='relu')
        self.dense2 = tf.keras.layers.Dense(64, activation='relu')
        self.output_layer = tf.keras.layers.Dense(1, activation=None)

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return self.output_layer(x)

# 定义 Actor-Critic 算法
class ActorCritic:
    def __init__(self, state_dim, action_dim, lr_actor=0.001, lr_critic=0.001, gamma=0.99):
        self.actor = ActorNetwork(state_dim, action_dim)
        self.critic = CriticNetwork(state_dim)
        self.optimizer_actor = tf.keras.optimizers.Adam(lr_actor)
        self.optimizer_critic = tf.keras.optimizers.Adam(lr_critic)
        self.gamma = gamma

    def train_step(self, state, action, reward, next_state, done):
        with tf.GradientTape() as tape_actor, tf.GradientTape() as tape_critic:
            # 计算 Actor 的动作概率分布
            action_probs = self.actor(state, training=True)
            # 从动作概率分布中采样动作
            chosen_action_probs = tf.reduce_sum(action_probs * tf.one_hot(action, depth=action_dim), axis=1)
            # 计算 Critic 的状态值
            state_value = self.critic(state, training=True)
            # 计算 TD 误差
            td_error = reward + (1 - done) * self.gamma * self.critic(next_state, training=True) - state_value
            # 计算 Actor 和 Critic 的损失
            actor_loss = -tf.math.log(chosen_action_probs) * td_error
            critic_loss = 0.5 * td_error ** 2

        # 计算 Actor 和 Critic 的梯度
        grads_actor = tape_actor.gradient(actor_loss, self.actor.trainable_variables)
        grads_critic = tape_critic.gradient(critic_loss, self.critic.trainable_variables)

        # 更新 Actor 和 Critic 的参数
        self.optimizer_actor.apply_gradients(zip(grads_actor, self.actor.trainable_variables))
        self.optimizer_critic.apply_gradients(zip(grads_critic, self.critic.trainable_variables))

# 创建环境
env = gym.make('CartPole-v1')
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n

# 初始化 Actor-Critic 算法
ac_agent = ActorCritic(state_dim, action_dim)

# 训练
for episode in range(1000):
    state = env.reset()
    total_reward = 0
    done = False
    while not done:
        # 根据策略选择动作
        action_probs = ac_agent.actor(np.expand_dims(state, axis=0), training=False).numpy()[0]
        action = np.random.choice(action_dim, p=action_probs)
        # 执行动作
        next_state, reward, done, _ = env.step(action)
        # 计算累积奖励
        total_reward += reward
        # 训练 Actor-Critic 算法
        ac_agent.train_step(np.expand_dims(state, axis=0), action, reward, np.expand_dims(next_state, axis=0), done)
        state = next_state
    print(f'Episode: {episode+1}, Total Reward: {total_reward}')
