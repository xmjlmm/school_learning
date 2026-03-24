import pandas as pd

df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理.xlsx", sheet_name="Sheet2")

prices = df['销售单价/(元/斤)']

min_price, max_price = [], []

for price in prices:
    min_p, max_p = price.split('-')
    min_price.append(min_p)
    max_price.append(max_p)

df['销售单价_最小值'] = min_price
df['销售单价_最大值'] = max_price

df.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理_修改.xlsx", index=False)