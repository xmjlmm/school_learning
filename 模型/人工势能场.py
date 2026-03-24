import numpy as np
import matplotlib.pyplot as plt


# 创建一个人工势能场的函数
def potential_field(x, y, target, obstacles, q_star):
    """
    计算给定位置的人工势能。

    参数:
    x, y -- 点的坐标
    target -- 目标位置的坐标 (tx, ty)
    obstacles -- 障碍物位置列表 [(ox1, oy1), (ox2, oy2), ...]
    q_star -- 影响范围参数，当障碍物距离小于此值时将增大势能

    返回:
    U -- 在点 (x, y) 的总势能
    """
    # 初始化势能为0
    U = 0

    # 计算吸引势能
    U_attr = 0.5 * np.linalg.norm([x - target[0], y - target[1]]) ** 2

    # 计算斥力势能
    U_rep = 0
    for (ox, oy) in obstacles:
        dist = np.linalg.norm([x - ox, y - oy])
        if dist < q_star:
            U_rep += 0.5 * (1 / dist - 1 / q_star) ** 2
        else:
            U_rep += 0

    # 总势能为吸引势能和斥力势能之和
    U = U_attr + U_rep

    return U


# 目标位置
target = (10, 10)

# 障碍物位置列表
obstacles = [(5, 5), (3, 8), (7, 7)]

# 影响范围参数
q_star = 2

# 生成网格点
x_range = np.linspace(0, 15, 100)
y_range = np.linspace(0, 15, 100)
x_grid, y_grid = np.meshgrid(x_range, y_range)

# 计算每个网格点的势能
U_grid = np.zeros_like(x_grid)
for i in range(x_grid.shape[0]):
    for j in range(x_grid.shape[1]):
        U_grid[i, j] = potential_field(x_grid[i, j], y_grid[i, j], target, obstacles, q_star)

# 绘图显示势能场
plt.figure(figsize=(8, 6))
plt.contourf(x_grid, y_grid, U_grid, levels=50, cmap='viridis')
plt.colorbar()
plt.plot(target[0], target[1], 'r*', markersize=15, label='Target')
plt.scatter([o[0] for o in obstacles], [o[1] for o in obstacles], color='r', label='Obstacles')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Artificial Potential Field')
plt.legend()
plt.show()
