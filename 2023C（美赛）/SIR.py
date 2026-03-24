'''Social distancing coefficient (beta)：social distancing coefficient, 用于描述COVID-19传染率的一个参数
Recovery rate (gamma)：用于描述COVID-19患者治愈率的一个参数
Incubation period (sigma)：用于描述COVID-19患者潜伏期的一个参数
Population number (N)：描述总人口数
Initial infected population (I0)：描述初始感染人口数
Initial susceptible population (S0)：描述初始易感人口数
Initial recovered population (R0)：描述初始治愈人口数
Time step (dt)：描述每个时间步长的大小
Total time (t_max)：描述模拟的总时间
T2PL模型（S, I, R）：描述每个时间步长中的状态变化'''

# 正演欧拉法
import numpy as np
import matplotlib.pyplot as plt

def T2PL(N, beta, gamma, sigma, I0, R0, S0, t_max, dt):
    # 初始化状态矩阵
    S = np.zeros(t_max)
    I = np.zeros(t_max)
    R = np.zeros(t_max)

    # 初始化状态值
    S[0] = S0
    I[0] = I0
    R[0] = R0

    # 进行求解
    for t in range(1, t_max):
        # 计算新的状态值
        dS = -beta * S[t - 1] * I[t - 1] / N
        dI = beta * S[t - 1] * I[t - 1] / N - gamma * I[t - 1] - sigma * I[t - 1]
        dR = gamma * I[t - 1] + sigma * I[t - 1]

        # 更新状态值
        S[t] = S[t - 1] + dS * dt
        I[t] = I[t - 1] + dI * dt
        R[t] = R[t - 1] + dR * dt

    return S, I, R

# 参数设置
N = 1000
beta = 15
gamma = 1
sigma = 3
I0 = 1
R0 = 0
S0 = N - I0 - R0
t_max = 100
dt = 0.1

# 进行求解
S, I, R = T2PL(N, beta, gamma, sigma, I0, R0, S0, t_max, dt)
print(S, I, R)
# 绘制结果


plt.plot(S, label='Susceptible')
plt.plot(I, label='Infected')
plt.plot(R, label='Recovered')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.show()


'''import numpy as np

def T2PL(N, beta, gamma, sigma, I0, R0, S0, t_max, dt):
    # 初始化状态矩阵
    S = np.zeros(t_max)
    I = np.zeros(t_max)
    R = np.zeros(t_max)

    # 初始化状态值
    S[0] = S0
    I[0] = I0
    R[0] = R0

    # 进行求解
    for t in range(1, t_max):
        # 计算新的状态值
        dS = -beta * S[t - 1] * I[t - 1] / N
        dI = beta * S[t - 1] * I[t - 1] / N - gamma * I[t - 1] - sigma * I[t - 1]
        dR = gamma * I[t - 1] + sigma * I[t - 1]

        # 更新状态值
        S[t] = S[t - 1] + dS * dt
        I[t] = I[t - 1] + dI * dt
        R[t] = R[t - 1] + dR * dt

    return S, I, R

# 参数设置
N = 1000
beta = 0.1
gamma = 0.05
sigma = 0.1
I0 = 1
R0 = 0
S0 = N - I0 - R0
t_max = 100
dt = 0.1

# 进行求解
S, I, R = T2PL(N, beta, gamma, sigma, I0, R0, S0, t_max, dt)

# 绘制结果
import matplotlib.pyplot as plt

plt.plot(S, label='Susceptible')
plt.plot(I, label='Infected')
plt.plot(R, label='Recovered')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.show()'''



'''import numpy as np

def T2PL(N, beta, gamma, sigma, I0, R0, S0, t_max, dt):
    # 初始化状态矩阵
    S = np.zeros(t_max)
    I = np.zeros(t_max)
    R = np.zeros(t_max)

    # 初始化状态值
    S[0] = S0
    I[0] = I0
    R[0] = R0

    # 进行求解
    for t in range(1, t_max):
        # 计算新的状态值
        dS = -beta * S[t - 1] * I[t - 1] / N
        dI = beta * S[t - 1] * I[t - 1] / N - gamma * I[t - 1] - sigma * I[t - 1]
        dR = gamma * I[t - 1] + sigma * I[t - 1]

        # 更新状态值
        S[t] = S[t - 1] + (dS + dS * (2 - dt) / 2) * dt
        I[t] = I[t - 1] + (dI + dI * (2 - dt) / 2) * dt
        R[t] = R[t - 1] + (dR + dR * (2 - dt) / 2) * dt

    return S, I, R

# 参数设置
N = 1000
beta = 0.1
gamma = 0.05
sigma = 0.1
I0 = 1
R0 = 0
S0 = N - I0 - R0
t_max = 100
dt = 0.1

# 进行求解
S, I, R = T2PL(N, beta, gamma, sigma, I0, R0, S0, t_max, dt)

# 绘制结果
import matplotlib.pyplot as plt

plt.plot(S, label='Susceptible')
plt.plot(I, label='Infected')
plt.plot(R, label='Recovered')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.show()'''


# 龙格库塔法
'''import numpy as np

def T2PL(N, beta, gamma, sigma, I0, R0, S0, t_max, dt):
    # 初始化状态矩阵
    S = np.zeros(t_max)
    I = np.zeros(t_max)
    R = np.zeros(t_max)

    # 初始化状态值
    S[0] = S0
    I[0] = I0
    R[0] = R0

    # 进行求解
    for t in range(1, t_max):
        # 计算新的状态值
        dS = -beta * S[t - 1] * I[t - 1] / N
        dI = beta * S[t - 1] * I[t - 1] / N - gamma * I[t - 1] - sigma * I[t - 1]
        dR = gamma * I[t - 1] + sigma * I[t - 1]

        # 更新状态值
        S[t] = S[t - 1] + (dS + dS * (1 - dt) / 2) * dt
        I[t] = I[t - 1] + (dI + dI * (1 - dt) / 2) * dt
        R[t] = R[t - 1] + (dR + dR * (1 - dt) / 2) * dt

    return S, I, R

# 参数设置
N = 1000
beta = 15
gamma = 0.05
sigma = 0.1
I0 = 1
R0 = 0
S0 = N - I0 - R0
t_max = 100
dt = 0.1

# 进行求解
S, I, R = T2PL(N, beta, gamma, sigma, I0, R0, S0, t_max, dt)

# 绘制结果
import matplotlib.pyplot as plt

plt.plot(S, label='Susceptible')
plt.plot(I, label='Infected')
plt.plot(R, label='Recovered')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.show()'''
