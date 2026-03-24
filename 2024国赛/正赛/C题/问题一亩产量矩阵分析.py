import pandas as pd
import numpy as np

# 读取两个Excel文件
df1 = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2.xlsx", sheet_name="2023年统计的相关数据")
df2 = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2.xlsx", sheet_name="2023年的农作物种植情况")

# 处理第一个DataFrame
df1 = df1[['作物编号', '作物名称', '地块类型', '种植季次', '亩产量/斤', '种植成本/(元/亩)', '销售单价/(元/斤)']]

# 处理第二个DataFrame
df2 = df2[['种植地块', '作物编号', '作物名称', '作物类型', '种植面积/亩', '种植季次']]

# 确保 '种植地块' 列的数据类型为字符串
df2['种植地块'] = df2['种植地块'].astype(str)
df2['作物名称'] = df2['作物名称'].astype(str)
df2['种植季次'] = df2['种植季次'].astype(str)

# 确定地块编号和作物名称的唯一值（应确保有41种地块，54种作物和3个季次）
land_plots = sorted(df2['种植地块'].unique())[:41]  # 取前41个唯一值
vegetable_names = sorted(df2['作物名称'].unique())[:54]  # 取前54个唯一值
seasons = sorted(df2['种植季次'].unique())[:3]  # 取前3个季次

# 创建映射字典
land_plot_to_index = {plot: idx for idx, plot in enumerate(land_plots)}
vegetable_name_to_index = {name: idx for idx, name in enumerate(vegetable_names)}
season_map = {season: idx for idx, season in enumerate(seasons)}

# 初始化矩阵
shape = (len(land_plots), len(vegetable_names), len(seasons))
matrix = np.zeros(shape, dtype=np.float32)

# 填充矩阵
for _, row in df2.iterrows():
    land_plot_idx = land_plot_to_index.get(row['种植地块'], -1)
    vegetable_name_idx = vegetable_name_to_index.get(row['作物名称'], -1)
    season_idx = season_map.get(row['种植季次'], -1)

    if land_plot_idx != -1 and vegetable_name_idx != -1 and season_idx != -1:
        # 使用列表1中的亩产量/斤值填充矩阵
        matching_rows = df1[(df1['作物编号'] == row['作物编号']) &
                            (df1['种植季次'] == row['种植季次']) &
                            (df1['地块类型'] == row['种植地块'])]
        if not matching_rows.empty:
            matrix[land_plot_idx, vegetable_name_idx, season_idx] = matching_rows['亩产量/斤'].values[0]

# 转换为 DataFrame
index = pd.MultiIndex.from_product(
    [land_plots, vegetable_names, seasons],
    names=['种植地块', '作物名称', '季次']
)
df_matrix = pd.DataFrame(matrix.flatten(), index=index, columns=['亩产量/斤']).reset_index()
df_matrix_pivot = df_matrix.pivot_table(index=['种植地块', '作物名称'], columns='季次', values='亩产量/斤')

# 保存 DataFrame 到 Excel 文件
df_matrix_pivot.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\亩产量矩阵.xlsx")

# 打印矩阵的部分内容
print(df_matrix_pivot.head())
