import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
from matplotlib.font_manager import FontProperties

# 设置字体属性
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=14)

# 生成模拟数据 (你可以使用自己的数据)
np.random.seed(0)
data = np.random.rand(20, 20)

# 计算距离矩阵 (皮尔逊相关系数)
corr = np.corrcoef(data)

# 转化为距离矩阵（pdist 直接计算距离，不需要转换）
distance_matrix = pdist(corr)

# 层次聚类
Z = linkage(distance_matrix, method='average')

# 创建一个子图，左边为树状图，上面为树状图，右下角为热力图
fig = plt.figure(figsize=(12, 10))  # 增加整体图像宽度
ax_dendro_x = fig.add_axes([0.3, 0.9, 0.6, 0.05])  # 上方树状图
ax_dendro_y = fig.add_axes([0.2, 0.3, 0.1, 0.6])  # 左侧树状图
ax_heatmap = fig.add_axes([0.3, 0.3, 0.8, 0.6])   # 热力图

# 绘制上方的树状图
dendrogram(Z, ax=ax_dendro_x, color_threshold=0, orientation='top')
ax_dendro_x.set_xticks([])
ax_dendro_x.set_yticks([])

# 绘制左侧的树状图
dendrogram(Z, ax=ax_dendro_y, color_threshold=0, orientation='left')
ax_dendro_y.set_xticks([])
ax_dendro_y.set_yticks([])

# 绘制热力图
sns.heatmap(
    corr, annot=True, fmt=".1f", linewidths=.5, cmap='coolwarm', cbar=True,
    ax=ax_heatmap, cbar_kws={"shrink": 1.0, "aspect": 15, "pad": 0.1}
)

# 隐藏左侧的 y 轴标签
ax_heatmap.yaxis.set_ticks_position('right')
ax_heatmap.yaxis.set_label_position('right')
ax_heatmap.set_yticklabels([f'单品{i+1}' for i in range(data.shape[0])], rotation=0, fontproperties=font)

# 设置中文标题和标签
ax_heatmap.set_xticklabels([f'单品{i+1}' for i in range(data.shape[1])], rotation=90, fontproperties=font)

# 显示图形
plt.show()
