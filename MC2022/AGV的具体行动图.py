# 论文1 p33
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 从图像中估计的路径点，实际应用中应该使用精确数据
# 提取图中显示的坐标
agv1_coords = np.array([
    (26, 11), (26, 10), (25, 10), (24, 10), (23, 10), (22, 10), (21, 10), (20, 10),
    (19, 10), (18, 10), (17, 10), (16, 9), (16, 8), (16, 7), (16, 6), (16, 5),
    (15, 4), (14, 3), (13, 2), (12, 1), (11, 1), (10, 1), (9, 1), (8, 1), (7, 1),
    (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (0, 1)
])

agv2_coords = np.array([
    (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12),
    (7, 13), (7, 14), (7, 15), (7, 16), (7, 17), (7, 18), (7, 19), (7, 20), (7, 21),
    (7, 22), (7, 23), (7, 24), (7, 25), (7, 26), (7, 27), (7, 28), (7, 29), (7, 30),
    (7, 31), (7, 32), (7, 33), (7, 34)
])

font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)

# 分离坐标点为X, Y
agv1_x, agv1_y = agv1_coords[:, 0], agv1_coords[:, 1]
agv2_x, agv2_y = agv2_coords[:, 0], agv2_coords[:, 1]

# 创建3D坐标轴
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制AGV1和AGV2的路径
# 这里假设Z轴坐标只是路径点的索引，没有实际Z轴高度数据
ax.plot(agv1_x, agv1_y, np.arange(len(agv1_x)), c='red', label='AGV1')
ax.plot(agv2_x, agv2_y, np.arange(len(agv2_x)), c='orange', linestyle='--', label='AGV2')

# 设置图例
ax.legend()

# 设置坐标轴标签
ax.set_xlabel('X 轴', fontproperties=font)
ax.set_ylabel('Y 轴', fontproperties=font)
ax.set_zlabel('Z 轴', fontproperties=font)

# 设置图标题
ax.set_title('图 3-8 基于AGV的路线示例图', fontproperties=font)

# 显示图形
plt.show()
