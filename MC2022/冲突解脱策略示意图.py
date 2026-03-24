# 论文1 p27

import matplotlib.pyplot as plt
import matplotlib.patches as patches
# 创建新的图形和轴对象
fig, ax = plt.subplots()
# 设置图形大小
fig.set_size_inches(8, 8)

# 绘制格子背景
for x in range(7):
    for y in range(7):
        rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor='none')
        ax.add_patch(rect)

# 填充特定的格子
for i in range(1, 4):
    for j in range(3, 5):
        rect = patches.Rectangle((i, j), 1, 1, linewidth=1, edgecolor='black', facecolor='green')
        ax.add_patch(rect)

# 绘制圆形及其编号，位置需要根据实际情况调整
circle_positions = [(4, 1), (4, 3), (3, 2), (5, 2)]
numbers = [1, 1, 2, 2]
for pos, num in zip(circle_positions, numbers):
    circle = patches.Circle((pos[0] + 0.5, pos[1] + 0.5), 0.4, linewidth=1, edgecolor='black', facecolor='orange')
    ax.add_patch(circle)
    # 添加文本
    plt.text(pos[0] + 0.5, pos[1] + 0.5, str(num), color='black', fontsize=15, ha='center', va='center')

# 绘制连接线
# 使用箭头指示从上面的2号圆到下面的1号圆
ax.annotate('', xy=(3.5, 2.5), xytext=(5.5, 2.5),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
# 从1号圆指向1号圆
ax.annotate('', xy=(4.5, 1.5), xytext=(4.5, 3.5),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))

# 绘制等待区域的标记，位置根据实际情况调整
plt.text(2.5, 2.5, 'wait', color='black', fontsize=15, ha='center', va='center')

# 禁用轴线
ax.axis('off')

# 设置坐标轴的显示范围
ax.set_xlim(0, 11)
ax.set_ylim(0, 11)

# 展示图形
plt.show()