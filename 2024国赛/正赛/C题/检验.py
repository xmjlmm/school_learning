import pandas as pd

df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\result.xlsx")
df1 = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件1.xlsx")
# df2 = pd.read_excel()
print(df)
s = df1['地块面积/亩']
# 每一行进行求和
sum_df = df.sum(axis=1)
print(sum_df)
# print(s)
n, flag, m = len(s), 0, len(sum_df)
# print(m)
for i in range(81):
    if i >= n:
        break
    else:
        print(sum_df[i])
        if sum_df[i] > s[i]:
            # print(i)
            flag = 1

print(flag)

