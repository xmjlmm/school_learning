'''
import pandas as pd

# 假设 df 是包含州和市政当局数据的 DataFrame
# 这里创建一个示例 DataFrame

# 原始数据
df = pd.read_csv("D://数模//美赛//2023校赛//处理后data1.csv")
cantion = df['canton']

df = pd.DataFrame({
    'State': ['A州', 'B州', 'C州', 'A州'],
    'Municipality': ['市1', '市2', '市3', '市1']
})

# 使用独热编码（One-Hot Encoding）转换州和市政当局的分类变量
# get_dummies 是 pandas 中用于生成独热编码的函数
df_encoded = pd.get_dummies(df, columns=['State', 'Municipality'])

# 展示处理后的数据
print(df_encoded)

'''

import pandas as pd

# 加载数据
df = pd.read_csv("D://数模//美赛//排位赛//处理后data1.csv")

# 假设 df 是您的数据集，其中包含 'State' 和 'Municipality' 这两列分类变量
# 下面是对这些分类变量进行独热编码的代码

# 使用 pandas 的 get_dummies 函数对分类变量进行独热编码
# 这会为每个类别创建一个新的列
df_encoded = pd.get_dummies(df, columns=['canton', 'municipality'])

# 展示处理后的数据
print(df_encoded.head())

# 如果需要，可以将处理后的数据保存回文件
df_encoded.to_excel("D://数模//美赛//2023校赛//1.xlsx")
