import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# # 创建一个示例DataFrame
# data = {
#     'A': [1, 2, 3, 4, 5],
#     'B': [5, 4, 3, 2, 1],
#     'C': [2, 3, 4, 5, 6],
#     'D': [5, 3, 6, 7, 2]
# }
#
# df = pd.DataFrame(data)

df = pd.read_excel("F:\\数模\\国赛\\模型\\相关系数\\八年级女生体测数据.xlsx")

# 设置中文字体
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=11.5)


# 计算相关性矩阵
correlation_matrix = df.corr()

# 打印相关性矩阵
print("Correlation Matrix:")
print(correlation_matrix)

# 绘制相关性热力图
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, fmt=".3f", cmap='coolwarm', linewidths=0.5)
plt.xticks(fontproperties=font)
plt.yticks(fontproperties=font)
plt.title('Correlation Matrix Heatmap')
plt.show()
