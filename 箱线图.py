import matplotlib.pyplot as plt

# 设置字体, 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决图像中的'-'负号的乱码问题
plt.rcParams['axes.unicode_minus'] = False

ClassA_C = [80, 90, 75, 65, 85, 95, 100, 100, 80, 70, 90, 95, 85, 86, 92, 90, 95, 90, 85, 100]
ClassB_C = [60, 70, 80, 65, 75, 80, 73, 75, 85, 90, 95, 65, 70, 75, 80, 85, 95, 85, 80, 70]
ClassC_C = [60, 80, 100, 100, 100, 100, 90, 95, 95, 95, 85, 95, 95, 95, 95, 80, 95, 90, 90, 90]

fig = plt.figure(figsize=(8, 6), facecolor='#B0C4DE')
ax = fig.add_subplot(facecolor='white')
# 红橙黄绿青蓝紫
color_list = ['#FF0000', '#FF8C00', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#800080']

x_labels = ['甲班', '乙班', '丙班']
x_loc = [1, 2, 3]

boxplot_data = [ClassA_C, ClassB_C, ClassC_C]

ax.boxplot(boxplot_data, positions=x_loc, widths=0.4, patch_artist=True,
           medianprops={'lw': 1, 'color': '#FF8C00'},
           boxprops={'facecolor': 'None', 'edgecolor': '#FF8C00'},
           capprops={'lw': 1, 'color': '#FF8C00'},
           whiskerprops={'ls': '-', 'lw': 1, 'color': '#FF8C00'},
           showfliers=True,
           flierprops={'marker': 'o', 'markerfacecolor': '#FF8C00', 'markeredgecolor': '#FF8C00', 'markersize': 8})
ax.grid(True, ls=':', color='b', alpha=0.3)
plt.title('甲乙丙各班语文成绩Box_chart分析', fontweight='bold')
ax.set_xticks(x_loc)
ax.set_xticklabels(x_labels, rotation=90)
ax.set_ylabel('分数/百分制', fontweight='bold')
# 设置x, y坐标轴的刻度标签字体加粗
plt.xticks(weight='bold')
plt.yticks(weight='bold')
fig.tight_layout()
plt.show()

