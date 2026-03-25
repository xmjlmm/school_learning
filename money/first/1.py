import pandas as pd


df = pd.read_excel("F:\\助人为乐\\第一单\\031922221可曦彤.xlsx", sheet_name="Sheet6")


print(df)

nation = df['您的民族']
for i in range(len(nation)):
    if nation[i] == '汉族':
        nation[i] = 0
    else:
        nation[i] = 1

possible = df['您认为自己在未来的 6 个月内失业的可能性有多大？']
for i in range(len(possible)):
    if possible[i] == '非常不可能':
        possible[i] = -2
    elif possible[i] == '不太可能':
        possible[i] = -1
    elif possible[i] == '不确定':
        possible[i] = 0
    elif possible[i] == '有可能':
        possible[i] = 1
    else:
        possible[i] = 2

education = df['您的教育程度']

for i in range(len(education)):
    if education[i] == '初中及以下':
        education[i] = 0
    elif education[i] == '高中/中专':
        education[i] = 1
    elif education[i] == '大学本科/大专':
        education[i] = 2
    elif education[i] == '硕士研究生':
        education[i] = 3
    else:
        education[i] = 4
