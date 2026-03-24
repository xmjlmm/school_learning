import pandas as pd

df1 = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理.xlsx", sheet_name="Sheet1")

df2 = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理.xlsx", sheet_name="Sheet2")

# 将df1的作物编号和作物名称和df2的作物编号和作物名称合并, 需要df1的种植面积/亩, 种植季次和df2中的亩产量/斤，种植成本/(元/亩)，销售单价/(元/斤)然后将合并后的结果保存为新的Excel文件

merged_df = pd.merge(df1, df2, on=['作物编号', '作物名称', '种植季次'])

# 去掉空缺值
merged_df = merged_df.fillna('')

# print(merged_df)

merged_df.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理(二次已处理).xlsx")