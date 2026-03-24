import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

# 参数
n = 16  # 螺旋线的圈数
p = 0.55  # 螺距
k = p / (2 * np.pi)  # k = p/(2*pi)
r0 = p * n  # 初始半径

# 定义微分方程
def dtheta_dt(t, theta):
    r = r0 - k * theta
    return 1 / np.sqrt(k**2 + r**2)

# 计算 theta(t)
def compute_theta(t_end):
    sol = solve_ivp(dtheta_dt, [0, t_end], [0], dense_output=True)  # 使用 dense_output=True 生成连续解
    if sol.success:  # 检查解是否成功
        theta_at_t = sol.sol(t_end)  # 在 t_end 处评估解
        return theta_at_t[0]  # 返回解中的 theta 值
    else:
        raise RuntimeError("Failed to solve the ODE")

# 计算 x, y 坐标
def compute_xy(theta):
    r = r0 - k * theta
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def equation(x1):
    x0 = np.pi
    # term1 = (r0 - k * x1) * np.cos(x1) - (r0 - k * x0) * np.cos(x0)
    # term2 = (r0 - k * x1) * np.sin(x1) - (r0 - k * x0) * np.sin(x0)
    # D = 2.2
    # return term1**2 + term2**2 - D**2
    D = 2.2
    tmp1 = np.cos(x1 - x0)
    tmp2 = (r0 - k * x1) ** 2 + (r0 - k * x0) ** 2 - D ** 2
    tmp3 = 2 * (r0 - k * x1) * (r0 - k * x0)
    return tmp1 - tmp2 / tmp3

def compute_next_theta(theta):
    x1_initial_guess = theta - 0.1  # 初始猜测值
    x1_solution = fsolve(equation, x1_initial_guess)
    return x1_solution
# 定义方程

# print(compute_next_theta(np.pi))
# 使用fsolve求解x1

# 计算每个时间点的 theta 和对应的 (x, y)
times = [0, 60, 120, 180, 240, 300, 360, 420, 445]
theta_values = [compute_theta(t) for t in times]
coordinates = [compute_xy(theta) for theta in theta_values]
print(compute_next_theta(np.pi))
for t, (x, y) in zip(times, coordinates):
    print(f"At time {t} s: x = {x:.2f}, y = {y:.2f}, s = {x**2 + y**2:.2f}")
