import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties

# 假设的AGV1和AGV2路径坐标点
agv1_x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
agv1_y = [0, 0, 0, 0, 0, 0, 0, 0, 0]
agv1_z = [1, 2, 3, 4, 5, 6, 7, 8, 9]

agv2_x = [7, 6, 5, 4, 3, 2, 1, 0]
agv2_y = [1, 1, 1, 1, 1, 1, 1, 1]
agv2_z = [2, 3, 4, 5, 6, 7, 8, 9]

font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)

# 创建3D坐标轴
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制AGV1和AGV2的路径
ax.plot(agv1_x, agv1_y, agv1_z, c='red', label='AGV1')
ax.plot(agv2_x, agv2_y, agv2_z, c='orange', linestyle='--', label='AGV2')

# 设置图例
ax.legend()

# 设置坐标轴标签
ax.set_xlabel('X 轴', fontproperties=font)
ax.set_ylabel('Y 轴', fontproperties=font)
ax.set_zlabel('Z 轴', fontproperties=font)

# 设置图标题
ax.set_title('两个AGV路径图', fontproperties=font)

# 显示图形
plt.show()
