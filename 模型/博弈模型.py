import numpy as np
import matplotlib.pyplot as plt

# 玩家数量
n_players = 1000

# p-beauty contest游戏的p值
p = 0.6

# 游戏迭代次数
n_rounds = 30

# 初始化玩家的策略
strategies = np.random.uniform(0, 100, n_players)

# 追踪平均策略
average_strategy = np.zeros(n_rounds)

# 运行游戏
for i in range(n_rounds):
    # 计算当前平均策略
    average_strategy[i] = np.mean(strategies)

    # 玩家更新策略
    strategies = p * average_strategy[i]

# 绘制平均策略随时间的变化
plt.plot(average_strategy)
plt.xlabel("Round")
plt.ylabel("Average Strategy")
plt.title("Convergence of strategies in p-beauty contest")
plt.show()