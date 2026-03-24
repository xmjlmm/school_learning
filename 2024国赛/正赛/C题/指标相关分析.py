import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 从Excel文件中读取数据
df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理单价(qqq已处理).xlsx", sheet_name="Sheet1")

# 设置中文字体
font = FontProperties(fname="C:\\Windows\\Fonts\\simsun.ttc", size=16)
plt.rcParams['font.sans-serif'] = [font.get_name()]  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

# # 打印实际的列名称以核对
# print("DataFrame列名称:")
# print(df.columns)

# print(df)

# 更新特征列表以匹配实际的列名称
features = ['种植面积/亩', '亩产量/斤', '种植成本/(元/亩)', '总成本', '利润/元', '单价', '总销售额']

# 提取与作物相关的特征
data = df[features]

# 计算皮尔逊相关系数矩阵
correlation_matrix = data.corr(method='pearson')

# 打印相关系数矩阵
print(correlation_matrix)

# 绘制热图
plt.figure(figsize=(10, 8))  # 调整图像尺寸
# 调一下字体大小
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5, fmt=".2f")
# sns.heatmap(correlation_matrix, annot=True, cmap='YlOrBr', vmin=-1, vmax=1, linewidths=0.5, fmt=".2f")
# sns.heatmap(correlation_matrix, annot=True, cmap='YlOrRd', vmin=-1, vmax=1, linewidths=0.5, fmt=".2f")
# sns.heatmap(correlation_matrix, annot=True, cmap='PuRd', vmin=-1, vmax=1, linewidths=0.5, fmt=".2f")
# sns.heatmap(correlation_matrix, annot=True, cmap='BuPu', vmin=-1, vmax=1, linewidths=0.5, fmt=".2f")
# sns.heatmap(correlation_matrix, annot=True, cmap='GnBu', vmin=-1, vmax=1, linewidths=0.5, fmt=".2f")
sns.heatmap(correlation_matrix, annot=True, cmap='PuBu', vmin=-1, vmax=1, linewidths=0.5, fmt=".2f")
# 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu'
# 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'
# 添加标题
plt.title('皮尔逊相关系数矩阵', fontproperties=font, fontsize=14)

# 添加坐标轴标签（中文）
plt.xlabel('特征', fontproperties=font, fontsize=14)
plt.ylabel('特征', fontproperties=font, fontsize=14)

# 保存图像到文件（可选）
plt.savefig("correlation_matrix_heatmap.png", dpi=300)

# 显示图像
plt.show()
