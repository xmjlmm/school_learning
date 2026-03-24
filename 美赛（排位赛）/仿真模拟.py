'''
import numpy as np

# 定义参数
rho = 1    # 密度
g = 9.8    # 重力加速度
phi = 30   # 内摩擦角,设定为30°
beta = 30  # 地表斜角,设定为30°
mu = np.tan(np.radians(phi))  # 干摩擦系数
xi = 0.1   # 湍流系数,设定为0.1
k = 1      # 压力系数,设定为1

# 雪崩流高度和速度
h = 5      # 雪崩流高度,设定为5m
u = 10     # 运动速度,设定为10m/s
n = 10     # 仿真步数

# 初始化
H = np.zeros((n, n))  # 雪崩流高度
U = np.zeros((n, n))  # 运动速度
F = np.zeros((n, n))  # 摩擦阻力

# 仿真
for i in range(n):
    for j in range(n):
        H[i, j] = h
        U[i, j] = u
        F[i, j] = (rho * g * np.sin(np.radians(beta)) * (mu + xi * U[i, j] * U[i, j] / g / H[i, j])) * H[i, j] * U[i, j] #计算摩擦阻力

print("摩擦阻力：")
print(F)
'''
'''
import numpy as np
import matplotlib.pyplot as plt

# 假设参数
m = 1000  # 雪块质量，单位 kg
g = 9.81  # 重力加速度，单位 m/s^2
theta = np.radians(30)  # 斜坡角度，转换为弧度
mu = 0.1  # 摩擦系数
v0 = 0  # 初始速度，单位 m/s
s0 = 0  # 初始位置，单位 m
t_sim = 10  # 模拟时间，单位 s
dt = 0.01  # 时间步长，单位 s

# 时间数组
t = np.arange(0, t_sim, dt)

# 力的计算
F_downhill = m * g * np.sin(theta)  # 斜坡下的力
F_friction = mu * m * g * np.cos(theta)  # 摩擦力

# 加速度的计算
a = (F_downhill - F_friction) / m  # 加速度

# 速度和位置的计算
'''
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义雪崩的物理属性
mass = 1000.0  # 雪崩的质量, 单位 kg
g = 9.81  # 重力加速度, 单位 m/s^2
slope_angle = np.radians(45)  # 坡度, 我们设为45度角
friction_coefficient = 0.1  # 摩擦系数, 取0.1

# 定义雪崩的初始状态
position = 0.0  # 位置, 单位 m
velocity = 0.0  # 速度, 单位 m/s
state = np.array([position, velocity])  # 初始状态

# 定义微分方程
def avalanche_equation(state, t):
    position, velocity = state
    acceleration = g * np.sin(slope_angle) - friction_coefficient * g * np.cos(slope_angle) * np.sign(velocity)
    return np.array([velocity, acceleration])

# 设定仿真的时间间隔
t = np.arange(0.0, 10.0, 0.1)

# 运行仿真
solution = odeint(avalanche_equation, state, t)

# 可视化结果
plt.plot(t, solution[:, 0])
plt.xlabel('时间 (s)')
plt.ylabel('位置 (m)')
plt.show()
'''
'''
import numpy as np
import matplotlib.pyplot as plt

#初始化参数和数组
N = 100 # 雪崩中的颗粒数
m = 1 # 每个颗粒的质量(mass)
delta_t = 0.1 # 时间步长
t_end = 10 # 仿真结束时间
g = 9.8 # 重力加速度

# 颗粒的初始位置和速度
positions = np.zeros(N)
velocities = np.zeros(N)

# 记录颗粒位置的数组
pos_over_time = np.zeros([int(t_end / delta_t), N])

# 仿真主循环
for t in np.arange(0, t_end, delta_t):
    # 计算施加在每个颗粒上的力
    forces = np.zeros(N) - g * m

    # 更新颗粒的速度和位置
    velocities = velocities + (forces / m) * delta_t
    positions = positions + velocities * delta_t

    # 记录颗粒位置
    pos_over_time[int(t / delta_t), :] = positions

# 画图
for i in range(N):
    plt.plot(np.arange(0, t_end, delta_t), pos_over_time[:, i])

plt.xlabel('time (s)')
plt.ylabel('position (m)')
plt.show()
'''

'''
import numpy as np
import matplotlib.pyplot as plt

# 摩擦系数的取值范围
friction_coefficients = np.linspace(0.1, 0.5, 5)


# 随机生成模拟数据的函数
def simulate_avalanche(friction_coefficient):
    time = np.linspace(0.1, 0.2, 100)
    height = 18 - 5 * friction_coefficient * time
    speed = 47.5 - 2 * friction_coefficient * time
    volume = 630000 + 20000 * friction_coefficient * time
    duration = 150 + 100 * friction_coefficient * time

    return time, height, speed, volume, duration


# 用于存储模拟结果的字典
results = {}

# 进行模拟
for coef in friction_coefficients:
    time, height, speed, volume, duration = simulate_avalanche(coef)
    results[coef] = {
        'time': time,
        'height': height,
        'speed': speed,
        'volume': volume,
        'duration': duration
    }
'''
'''
import numpy as np
import matplotlib.pyplot as plt

N = 1  # 颗粒数
m = 1.0  # 颗粒质量
dt = 0.1  # 时间步长
t_end = 10.0  # 仿真结束时间
g = 9.8  # 重力加速度

# 创建figure和axes
fig, ax = plt.subplots()

# 初始化速度并记录结果用于敏感性分析
initial_velocities = np.linspace(0.0, 1.0, 5)
final_positions = []

# 遍历每个初始速度
for v0 in initial_velocities:
    # 颗粒初始位置和速度
    pos = np.zeros(N)
    vel = np.ones(N) * v0

    # 对每一时刻进行仿真
    for t in np.arange(0, t_end, dt):
        # 计算作用在颗粒上的力
        forces = -g * m
        # 更新颗粒的速度和位置
        vel = vel + (forces / m) * dt
        pos = pos + vel * dt

    # 记录最终位置
    final_positions.append(pos[0])

# 绘制初始速度对最终位置的影响
ax.plot(initial_velocities, final_positions, 'o-', label='g=' + str(g))

# 添加图例和标签
ax.legend()
ax.set_xlabel('初始速度 (m/s)')
ax.set_ylabel('最终位置 (m)')
plt.show()
'''


import numpy as np
import matplotlib.pyplot as plt

# 初始值
velocity = 10.0    # 初始速度
time = 1.0         # 投射时间

# 计算投射位移的函数
def calculate_displacement(gravity, velocity, time):
    displacement_x = velocity * time
    displacement_y = 0.5 * gravity * time ** 2
    return displacement_x, displacement_y

# 重力加速度的范围
gravity_values = np.linspace(-9.9, -9.7, 100)

# 计算每个重力值的位移
displacements = [calculate_displacement(g, velocity, time) for g in gravity_values]

# 获取x位移和y位移的值
displacement_x_values = [d[0] for d in displacements]
displacement_y_values = [d[1] for d in displacements]

# 绘制图形
plt.figure(figsize=(10,6))
plt.plot(gravity_values, displacement_x_values, label='Displacement X')
plt.plot(gravity_values, displacement_y_values, label='Displacement Y')
plt.xlabel('Gravity (m/s^2)')
plt.ylabel('Displacement (m)')
plt.legend()
plt.title('Sensitivity Analysis: Displacement vs. Gravity')
plt.grid(True)
plt.show()

'''
import numpy as np
import matplotlib.pyplot as plt

# 初始值
velocity = 10.0    # 初始速度
time = 1.0         # 投射时间

# 计算投射位移的函数
def calculate_displacement(gravity, velocity, time):
    displacement_y = 0.5 * gravity * time ** 2
    return displacement_y

# 重力加速度的范围
gravity_values = np.linspace(-9.9, -9.7, 100)

# 计算每个重力值的位移
displacement_y_values = [calculate_displacement(g, velocity, time) for g in gravity_values]

# 绘制图形
plt.figure(figsize=(10,6))
plt.plot(gravity_values, displacement_y_values)
plt.xlabel('Gravity (m/s^2)')
plt.ylabel('Displacement y (m)')
plt.title('Sensitivity Analysis: Displacement vs. Gravity')
plt.grid(True)
plt.show()
'''