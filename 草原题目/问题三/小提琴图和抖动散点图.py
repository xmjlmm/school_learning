# 根据上述数据，据不同年份、不同地区及不同放牧强度下的数据情况绘制小提琴图和抖动散点图
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df_merged = pd.read_excel("F:\\数模\\2024年国赛复习资料\\国赛提高\\补充草原题\\数据集\\监测点数据\\附件14：内蒙古自治区锡林郭勒盟典型草原不同放牧强度土壤碳氮监测数据集（2012年8月15日-2020年8月15日）\\内蒙古自治区锡林郭勒盟典型草原不同放牧强度土壤碳氮监测数据集（2012年8月15日-2020年8月15日）合并.xlsx")
# print(df_merged)

# 设置绘图风格
sns.set(style="whitegrid", palette="coolwarm")

# 设置图形大小
plt.figure(figsize=(20, 15))


# 创建子图
fig, axes = plt.subplots(5, 1, figsize=(10, 20))
# plt.figure(figsize=(10, 10))
# 绘制小提琴图和抖动散点图：SOC土壤有机碳
sns.violinplot(ax=axes[0], x='year', y='SOC土壤有机碳', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
sns.stripplot(ax=axes[0], x='year', y='SOC土壤有机碳', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)
axes[0].set_title('SOC土壤有机碳')
axes[0].set_ylabel('SOC土壤有机碳 (%)')



# 绘制小提琴图和抖动散点图：SIC土壤无机碳
sns.violinplot(ax=axes[1], x='year', y='SIC土壤无机碳', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
sns.stripplot(ax=axes[1], x='year', y='SIC土壤无机碳', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)
axes[0].set_title('SIC土壤无机碳')
axes[0].set_ylabel('SIC土壤无机碳 (%)')

# 绘制小提琴图和抖动散点图：土壤全碳
sns.violinplot(ax=axes[2], x='year', y='STC土壤全碳', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
sns.stripplot(ax=axes[2], x='year', y='STC土壤全碳', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)
axes[0].set_title('Soil Total Carbon (STC)')
axes[0].set_ylabel('Soil Total Carbon (%)')

# 绘制小提琴图和抖动散点图：全氮
sns.violinplot(ax=axes[3], x='year', y='全氮N', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
sns.stripplot(ax=axes[3], x='year', y='全氮N', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)
axes[1].set_title('Total Nitrogen (TN)')
axes[1].set_ylabel('Total Nitrogen (%)')

# 绘制小提琴图和抖动散点图：土壤C/N比
sns.violinplot(ax=axes[4], x='year', y='土壤C/N比', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
sns.stripplot(ax=axes[4], x='year', y='土壤C/N比', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)
axes[2].set_title('Soil C/N Ratio')
axes[2].set_ylabel('Soil C/N Ratio')

# 调整布局
plt.tight_layout()
plt.show()


# 设置绘图风格和调色板
sns.set(style="whitegrid", palette="coolwarm")

# 绘制SOC土壤有机碳小提琴图和抖动散点图
plt.figure(figsize=(15, 8))

# 小提琴图
sns.violinplot(x='year', y='SOC土壤有机碳', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
# 抖动散点图
sns.stripplot(x='year', y='SOC土壤有机碳', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)

# 设置图标题和标签
plt.title('Soil SOC Ratio by Year and Grazing Intensity')
plt.xlabel('Year')
plt.ylabel('Soil SOC Ratio')
plt.legend(title='Grazing Intensity')
plt.show()


# 绘制SOC土壤有机碳小提琴图和抖动散点图
plt.figure(figsize=(15, 8))

# 小提琴图
sns.violinplot(x='year', y='SIC土壤无机碳', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
# 抖动散点图
sns.stripplot(x='year', y='SIC土壤无机碳', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)

# 设置图标题和标签
plt.title('Soil SIC Ratio by Year and Grazing Intensity')
plt.xlabel('Year')
plt.ylabel('Soil SIC Ratio')
plt.legend(title='Grazing Intensity')
plt.show()


# 绘制土壤全碳小提琴图和抖动散点图
plt.figure(figsize=(15, 8))

# 小提琴图
sns.violinplot(x='year', y='STC土壤全碳', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
# 抖动散点图
sns.stripplot(x='year', y='STC土壤全碳', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)

# 设置图标题和标签
plt.title('Soil Total Carbon (STC) by Year and Grazing Intensity')
plt.xlabel('Year')
plt.ylabel('Soil Total Carbon (%)')
plt.legend(title='Grazing Intensity')
plt.show()


# 绘制土壤全氮小提琴图和抖动散点图
plt.figure(figsize=(15, 8))

# 小提琴图
sns.violinplot(x='year', y='全氮N', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
# 抖动散点图
sns.stripplot(x='year', y='全氮N', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)

# 设置图标题和标签
plt.title('Total Nitrogen (N) by Year and Grazing Intensity')
plt.xlabel('Year')
plt.ylabel('Total Nitrogen (%)')
plt.legend(title='Grazing Intensity')
plt.show()


# 绘制土壤C/N比小提琴图和抖动散点图
plt.figure(figsize=(15, 8))

# 小提琴图
sns.violinplot(x='year', y='土壤C/N比', hue='放牧强度（intensity）', data=df_merged, split=True, inner='quartile')
# 抖动散点图
sns.stripplot(x='year', y='土壤C/N比', hue='放牧强度（intensity）', data=df_merged, jitter=True, dodge=True, linewidth=1)

# 设置图标题和标签
plt.title('Soil C/N Ratio by Year and Grazing Intensity')
plt.xlabel('Year')
plt.ylabel('Soil C/N Ratio')
plt.legend(title='Grazing Intensity')
plt.show()

