import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理_修改.xlsx", sheet_name="Sheet1")
# print(df)
# 假设数据如下
crop_names = df['作物名称']
planting_season = df['种植季次']  # 种植季次
yield_per_acre = df['亩产量/斤']  # 亩产量/斤
for i in yield_per_acre:
    if yield_per_acre[i] == '单季':
        yield_per_acre[i] = 0
    elif yield_per_acre[i] == '第一季':
        yield_per_acre[i] = 1
    else:
        yield_per_acre[i] = 2


# 创建x轴、y轴、z轴的数据
x = np.arange(len(crop_names))  # x轴为作物名称，数值代替名称
y = np.array(planting_season)  # y轴为种植季次
z = np.array(yield_per_acre)  # z轴为亩产量

# 创建3D图形
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# 绘制三维折线图
ax.plot(x, y, z, marker='o')

# 设置坐标轴标签
ax.set_xticks(x)
ax.set_xticklabels(crop_names)
ax.set_xlabel('作物名称')
ax.set_ylabel('种植季次')
ax.set_zlabel('亩产量/斤')

# 显示图形
plt.show()
