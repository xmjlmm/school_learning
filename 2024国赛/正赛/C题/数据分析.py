import pandas as pd

df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理(已处理).xlsx")

price = df['销售单价/(元/斤)']
min_prices, max_prices = [], []

for i in price:
    min_price, max_price = i.split('-')
    min_prices.append(min_price)
    max_prices.append(max_price)

# 将最小价和最大价分别添加到DataFrame中
df['销售单价(最小值)'] = min_prices
df['销售单价(最大值)'] = max_prices

# 导出df

df.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理单价(已处理).xlsx", index=False)