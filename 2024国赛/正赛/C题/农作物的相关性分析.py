import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 从Excel文件中读取数据
df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理单价(qqq已处理).xlsx", sheet_name="Sheet1")

# 设置中文字体
font = FontProperties(fname="C:\\Windows\\Fonts\\simsun.ttc", size=14)
plt.rcParams['font.sans-serif'] = [font.get_name()]  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

# 打印实际的列名称以核对
print("DataFrame列名称:")
print(df.columns)

# 选择数值类型的列进行相关性分析
# 请确认数值类型的列（例如：种植面积/亩、亩产量/斤等）
# 这里假设以下列都是数值类型
numeric_features = ['种植面积/亩', '亩产量/斤', '种植成本/(元/亩)', '总成本', '利润/元', '单价', '总销售额']

# 创建一个新的数据框，列名是作物名称
# 将每个作物的数值特征提取出来
df_vegetable_features = df[['作物名称'] + numeric_features]

# 设定作物名称为索引
df_vegetable_features.set_index('作物名称', inplace=True)

# 计算作物之间的相关性矩阵
# 首先，转置数据框，以便每列代表一个作物的特征
df_transposed = df_vegetable_features.T

# 计算相关性矩阵
correlation_matrix = df_transposed.corr(method='pearson')

# 打印相关系数矩阵
print(correlation_matrix)

# 绘制热图
plt.figure(figsize=(18, 16))  # 调整图像尺寸，增加宽度和高度
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5, fmt=".2f", annot_kws={"size": 10})

# 添加标题
plt.title('作物之间的皮尔逊相关系数矩阵', fontproperties=font, fontsize=20)

# 添加坐标轴标签（中文）
plt.xlabel('作物', fontproperties=font, fontsize=16)
plt.ylabel('作物', fontproperties=font, fontsize=16)

# 自动调整坐标轴标签
plt.xticks(rotation=90)  # 旋转x轴标签，防止重叠
plt.yticks(rotation=0)   # 旋转y轴标签

# 保存图像到文件（可选）
plt.savefig("vegetable_correlation_heatmap.png", dpi=300, bbox_inches='tight')

# 显示图像
plt.show()
