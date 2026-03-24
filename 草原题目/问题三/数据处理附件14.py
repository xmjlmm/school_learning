import pandas as pd

df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\国赛提高\\补充草原题\\数据集\\监测点数据\\附件14：内蒙古自治区锡林郭勒盟典型草原不同放牧强度土壤碳氮监测数据集（2012年8月15日-2020年8月15日）\\内蒙古自治区锡林郭勒盟典型草原不同放牧强度土壤碳氮监测数据集（2012年8月15日-2020年8月15日）.xlsx")

# 将year相同和放牧小区相同和放牧强度的数据进行合并，求取他们的平均值
df_merged = df.groupby(['year', '放牧小区（plot）', '放牧强度（intensity）']).mean()
df_merged.reset_index(inplace=True)
print(df_merged)

# 将数据导出到Excel文件
df_merged.to_excel("F:\\数模\\2024年国赛复习资料\\国赛提高\\补充草原题\\数据集\\监测点数据\\附件14：内蒙古自治区锡林郭勒盟典型草原不同放牧强度土壤碳氮监测数据集（2012年8月15日-2020年8月15日）\\内蒙古自治区锡林郭勒盟典型草原不同放牧强度土壤碳氮监测数据集（2012年8月15日-2020年8月15日）合并.xlsx", index=False)
# print(df)

# 根据上述数据，据不同年份、不同地区及不同放牧强度下的数据情况绘制小提琴图和抖动散点图
import matplotlib.pyplot as plt
import seaborn as sns
