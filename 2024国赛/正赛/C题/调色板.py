import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# 使用 Colorbrewer 的色盲友好配色方案
colors = ListedColormap(['#E41A1C', '#377EB8', '#4DAF4A'])

# 进行绘图时使用这些颜色
scatter = ax.scatter(x, y, z, c=data_clean['Cluster'], cmap=colors, s=50, edgecolor='k')
