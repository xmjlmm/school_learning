# import pandas as pd
# import numpy as np
#
# # 定义矩阵的形状
# shape1 = (54, 42, 3)
# shape2 = (42, 3)
#
# # 读取数据
# df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2.xlsx", sheet_name="2023年统计的相关数据")
#
# # 创建矩阵
# ps, p, m, c = np.zeros(shape2, dtype=np.float32), np.zeros(shape2, dtype=np.float32), np.zeros(shape1,
#                                                                                                dtype=np.float32), np.zeros(
#     shape1, dtype=np.float32)
#
# # 确保价格列为字符串类型
# df['销售单价/(元/斤)'] = df['销售单价/(元/斤)'].astype(str)
#
# # 提取最小价和最大价
# min_prices, max_prices = [], []
#
# for price in df['销售单价/(元/斤)']:
#     try:
#         min_price, max_price = price.split('-')
#         min_prices.append(float(min_price))
#         max_prices.append(float(max_price))
#     except ValueError:
#         min_prices.append(np.nan)
#         max_prices.append(np.nan)
#
# # 将最小价和最大价分别添加到DataFrame中
# df['销售单价(最小值)'] = min_prices
# df['销售单价(最大值)'] = max_prices
#
# # 填充矩阵
# for i, crop_id in enumerate(df['作物编号'].unique()):
#     crop_data = df[df['作物编号'] == crop_id]
#     for season in crop_data['种植季次'].unique():
#         season_data = crop_data[crop_data['种植季次'] == season]
#         if not season_data.empty:
#             # 计算最小价和最大价的均值
#             min_price = season_data['销售单价(最小值)'].mean()
#             max_price = season_data['销售单价(最大值)'].mean()
#             avg_price = (min_price + max_price) / 2
#
#             if season == '单季':
#                 season_index = 0
#             elif season == '第一季':
#                 season_index = 1
#             elif season == '第二季':
#                 season_index = 2
#             else:
#                 continue
#             ps[i, season_index] = avg_price
#
# # 转换为 DataFrame 并保存到 Excel 文件
# ps_df = pd.DataFrame(ps)
# ps_df.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\预期价格矩阵.xlsx", index=False)
#
# # 打印矩阵
# print(ps_df)


import pandas as pd
import numpy as np

# 定义矩阵的形状
shape1 = (54, 42, 3)
shape2 = (44, 3)

# 读取数据
df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2.xlsx", sheet_name="2023年统计的相关数据")

# 创建矩阵
ps, p, m, c = np.zeros(shape2, dtype=np.float32), np.zeros(shape2, dtype=np.float32), np.zeros(shape1, dtype=np.float32), np.zeros(shape1, dtype=np.float32)

# 确保价格列为字符串类型
df['销售单价/(元/斤)'] = df['销售单价/(元/斤)'].astype(str)

# 提取最小价和最大价
min_prices, max_prices = [], []

for price in df['销售单价/(元/斤)']:
    try:
        min_price, max_price = price.split('-')
        min_prices.append(float(min_price))
        max_prices.append(float(max_price))
    except ValueError:
        min_prices.append(np.nan)
        max_prices.append(np.nan)

# 将最小价和最大价分别添加到DataFrame中
df['销售单价(最小值)'] = min_prices
df['销售单价(最大值)'] = max_prices

# 获取作物编号与蔬菜名称的映射关系
crop_names = df[['作物编号', '作物名称']].drop_duplicates().set_index('作物编号')['作物名称'].to_dict()

# 填充矩阵
for i, crop_id in enumerate(df['作物编号'].unique()):
    crop_data = df[df['作物编号'] == crop_id]
    for season in crop_data['种植季次'].unique():
        season_data = crop_data[crop_data['种植季次'] == season]
        if not season_data.empty:
            # 计算最小价和最大价的均值
            min_price = season_data['销售单价(最小值)'].mean()
            max_price = season_data['销售单价(最大值)'].mean()
            avg_price = (min_price + max_price) / 2

            if season == '单季':
                season_index = 0
            elif season == '第一季':
                season_index = 1
            elif season == '第二季':
                season_index = 2
            else:
                continue
            ps[i, season_index] = avg_price

# 转换为 DataFrame 并插入蔬菜名称
ps_df = pd.DataFrame(ps, columns=['单季', '第一季', '第二季'])
ps_df.index = [crop_names.get(crop_id, f"未知作物 {crop_id}") for crop_id in df['作物编号'].unique()]

# 保存 DataFrame 到 Excel 文件
ps_df.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\预期价格矩阵.xlsx")

# 打印矩阵
print(ps_df)
