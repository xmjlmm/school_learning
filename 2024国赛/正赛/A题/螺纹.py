import numpy as np
import pandas as pd

# Constants
initial_speed = 1.0  # m/s
spiral_p = 0.55  # 螺距，单位：m
number_of_segments = 223  # 板凳节数
head_length = 3.41  # 龙头长度，单位：m
body_length = 2.20  # 龙身/龙尾长度，单位：m

# Time settings
total_time = 300  # 总时间(s)
delta_t = 1  # 时间步长(s)
time_steps = np.arange(0, total_time + delta_t, delta_t)

# Initialize arrays for positions and velocities
positions = {}
velocities = {}

# Initialize 龙头
positions["龙头"] = np.zeros((len(time_steps), 2))  # [x, y]
velocities["龙头"] = np.zeros(len(time_steps))

# Initialize 龙身 segments
for i in range(1, number_of_segments + 1):
    positions[f"第{i}节龙身"] = np.zeros((len(time_steps), 2))
    velocities[f"第{i}节龙身"] = np.zeros(len(time_steps))

# Initialize 龙尾
positions["龙尾(后)"] = np.zeros((len(time_steps), 2))
velocities["龙尾(后)"] = np.zeros(len(time_steps))

# Initial position of the 龙头
positions["龙头"][0] = [0, 0]

# Loop through each second to calculate positions and velocities
for t in range(1, len(time_steps)):
    angle_increment = initial_speed / spiral_p  # how much the angle increases each second
    total_angle = angle_increment * t  # Total angle after t seconds

    # Update 龙头 position
    positions["龙头"][t] = [spiral_p * total_angle * np.cos(total_angle),
                            spiral_p * total_angle * np.sin(total_angle)]

    # Update 龙身 and 龙尾 positions
    for i in range(1, number_of_segments + 1):
        if i == 1:
            positions["第1节龙身"][t] = positions["龙头"][t] + [head_length, 0]
        elif i == 201:
            positions["龙尾(后)"][t] = positions[f"第{i - 1}节龙身"][t] + [body_length, 0]
        else:
            positions[f"第{i}节龙身"][t] = positions[f"第{i - 1}节龙身"][t] + [body_length, 0]

    # Calculate velocities
    velocities["龙头"][t] = initial_speed  # 龙头速度始终保持1 m/s
    for i in range(1, number_of_segments + 1):
        velocities[f"第{i}节龙身"][t] = velocities["龙头"][t]  # 同样速度假设

# Prepare the results for saving
result_positions = pd.DataFrame({
    "时间": time_steps,
    "龙头_x(m)": positions["龙头"][:, 0],
    "龙头_y(m)": positions["龙头"][:, 1],
    "第1节龙身_x(m)": positions["第1节龙身"][:, 0],
    "第1节龙身_y(m)": positions["第1节龙身"][:, 1],
    "第51节龙身_x(m)": positions["第51节龙身"][:, 0],
    "第51节龙身_y(m)": positions["第51节龙身"][:, 1],
    "第101节龙身_x(m)": positions["第101节龙身"][:, 0],
    "第101节龙身_y(m)": positions["第101节龙身"][:, 1],
    "第151节龙身_x(m)": positions["第151节龙身"][:, 0],
    "第151节龙身_y(m)": positions["第151节龙身"][:, 1],
    "第201节龙身_x(m)": positions["第201节龙身"][:, 0],
    "第201节龙身_y(m)": positions["第201节龙身"][:, 1],
    "龙尾(后)_x(m)": positions["龙尾(后)"][:, 0],
    "龙尾(后)_y(m)": positions["龙尾(后)"][:, 1],
})

print(result_positions)
# # Save to Excel file
result_positions.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\A题\\问题一result.xlsx")
