import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=14)

# 准备数据
labels = np.array(['流动性', '准确定', '方差', '我最常性', '占有率', '灵活性', '信誉度', '弹性', '平均周期'])
num_vars = len(labels)

# 供应商数据 (假设有5个供应商)
S201 = [0.8, 0.6, 0.5, 0.9, 0.7, 0.8, 0.5, 0.6, 0.7]
S229 = [0.6, 0.7, 0.6, 0.8, 0.8, 0.5, 0.7, 0.7, 0.6]
S361 = [0.7, 0.6, 0.7, 0.7, 0.6, 0.6, 0.8, 0.8, 0.5]
S140 = [0.9, 0.8, 0.8, 0.7, 0.6, 0.5, 0.6, 0.7, 0.8]
S108 = [0.5, 0.5, 0.6, 0.6, 0.7, 0.8, 0.7, 0.6, 0.9]

# 将数据整理成一个列表
values = [S201, S229, S361, S140, S108]

# 绘制雷达图
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
values = [v + [v[0]] for v in values]  # 闭合雷达图
angles += angles[:1]  # 闭合角度

# 设置雷达图的参数
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# 绘制每一个供应商的数据线
for i, v in enumerate(values):
    ax.plot(angles, v, linewidth=2, linestyle='solid', label=f'S{i + 201}')

# 填充雷达图内部
for v in values:
    ax.fill(angles, v, alpha=0.25)

# 添加标签
ax.set_yticklabels([])  # 隐藏圆形坐标标签
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontproperties=font)

# 添加图例
ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

# 设置标题
plt.title('供应商特征比较', fontproperties=font)

# 显示图形
plt.show()
