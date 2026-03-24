from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def model(y, t):
    """
    微分方程模型函数
    参数:
    y - 依赖变量
    t - 独立变量（时间）

    返回:
    dydt - y的导数
    """
    k = 0.3  # 常数k
    dydt = -k * y
    return dydt

# 初始条件
y0 = 5

# 时间点
t = np.linspace(0, 20, 100)

# 求解微分方程
y = odeint(model, y0, t)

# 绘制结果
plt.plot(t, y)
plt.xlabel('时间')
plt.ylabel('y(t)')
plt.title('微分方程求解示例')
plt.show()
