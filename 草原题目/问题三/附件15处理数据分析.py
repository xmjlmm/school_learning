import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# 读取数据
df = pd.read_excel(r"F:\数模\2024年国赛复习资料\国赛提高\补充草原题\数据集\监测点数据\附件14：内蒙古自治区锡林郭勒盟典型草原不同放牧强度土壤碳氮监测数据集（2012年8月15日-2020年8月15日）\透视处理数据.xlsx")

# print(df.head())

# 设置中文字体
font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=14)

# 设置绘图风格
sns.set(style="whitegrid", palette="coolwarm")

# 设置图形大小
plt.figure(figsize=(15, 8))

# 小提琴图
sns.violinplot(x='year', y='干重', hue='放牧强度', data=df, split=True, inner='quartile')
# 抖动散点图
sns.stripplot(x='year', y='干重', hue='放牧强度', data=df, jitter=True, dodge=True, linewidth=1)

# 设置图标题和标签，使用中文标题
plt.title('年份与放牧强度对干重的影响', fontproperties=font)
plt.xlabel('年份', fontproperties=font)
plt.ylabel('干重 (%)', fontproperties=font)
plt.legend(title='放牧强度', prop=font)
plt.show()