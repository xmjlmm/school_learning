import pandas as pd


df = pd.read_excel("F:\\助人为乐\\第二单\\031922249（已处理）.xlsx",sheet_name="Sheet4")

# for i in range(len(df["您是否有以下现象"])):
#     if '没有手机会觉得很失落' in df['您是否有以下现象'][i]:
#         df['您是否有以下现象'][i] = 0
#     elif '会不自觉的想要刷视频' in df['您是否有以下现象'][i]:
#         df['您是否有以下现象'][i] = 1
#     else:
#         df['您是否有以下现象'][i] = 2
# print(df["您是否有以下现象"])


for i in range(len(df["您的年龄范围为"])):
    if df['您的年龄范围为'][i] == '18周岁~24周岁':
        df['您的年龄范围为'][i] = 21
    elif df['您的年龄范围为'] == '25周岁~35周岁':
        df['您的年龄范围为'][i] = 30
    else:
        df['您的年龄范围为'][i] = 40

print(df["您的年龄范围为"])
# df.to_excel('F:\\助人为乐\\第二单\\现象.xlsx"')