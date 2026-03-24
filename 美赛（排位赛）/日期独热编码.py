'''
import pandas as pd

# 原始数据
df = pd.read_csv("D://数模//美赛//2023校赛//处理后data1.csv")
dates = df['date']

# 将原始数据转换为pandas的日期格式
dates = pd.to_datetime(dates)
length = len(dates)
for i in range(length):
    date = dates[i]
    # 提取月份和日期信息，添加到新的DataFrame中
    df = pd.DataFrame()
    df['month'] = date.month
    df['day'] = date.day

    # 使用pandas的get_dummies()函数转换为独热编码
    df_encoded = pd.get_dummies(df, columns=['month', 'day'])

    # 显示独热编码后的DataFrame
    print(df_encoded)

'''


import pandas as pd

# 原始数据
df = pd.read_csv("D://数模//美赛//排位赛//处理后data1.csv")
dates = pd.to_datetime(df['date'])

months, days = [], []
# 提取月份和日期信息，添加到新的DataFrame中
for date in dates:
    months.append(date.month)
    days.append(date.day)

# 创建一个新的DataFrame
df_date = pd.DataFrame()
df_date['month'] = months
df_date['day'] = days

# 使用pandas的get_dummies()函数转换为独热编码
df_encoded = pd.get_dummies(df_date, columns=['month', 'day'])

# 将独热编码添加到原始的df中
df =  pd.concat([df,df_encoded], axis=1)

# 显示前5行数据
df.to_excel("D://数模//美赛//2023校赛//1.xlsx")
