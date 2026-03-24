import matplotlib.pyplot as plt

# 设置矩阵的行和列标签
rows = ['高', '中', '低']
cols = ['强', '中', '弱']

# 设置每个策略对应的颜色
colors = ["green", "lightgreen", "orange", "red"]

# 创建一个8x8的图形
fig, ax = plt.subplots(figsize=(8, 8))

# 绘制矩阵的每个单元格
for i, row in enumerate(rows):
    for j, col in enumerate(cols):
        index = i if i != 2 else i + j
        ax.text(j, 2-i, f'{row}\n{col}', va='center', ha='center', size='large')
        ax.add_patch(plt.Rectangle((j, 2-i), 1, 1, fill=True, color=colors[index]))

# 绘制策略的文字
strategies = [
    "增长/投资", "增长/投资", "持有/选择",
    "增长/投资", "持有/选择", "收获/剥离",
    "持有/选择", "收获/剥离", "收获/剥离"
]
for i, strategy in enumerate(strategies):
    ax.text(i % 3, 2 - i // 3, strategy, va='center', ha='center')

# 设置坐标轴的标签
ax.set_xticks([0.5, 1.5, 2.5])
ax.set_yticks([0.5, 1.5, 2.5])
ax.set_xticklabels(['市场竞争力\n强', '市场竞争力\n中', '市场竞争力\n弱'])
ax.set_yticklabels(['行业吸引力\n高', '行业吸引力\n中', '行业吸引力\n低'])

# 隐藏坐标轴的线和刻度
ax.set_xticks([], minor=True)
ax.set_yticks([], minor=True)
for edge in ['left', 'right', 'top', 'bottom']:
    ax.spines[edge].set_visible(False)

# 显示图形
plt.show()
