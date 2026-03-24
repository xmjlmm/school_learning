# 导入所需库
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 创建示例数据集
data = {
    'X1': [1, 4, 7, 10],
    'X2': [2, 5, 8, 11],
    'X3': [3, 6, 9, 12],
    'y': [10, 20, 30, 40]
}
df = pd.DataFrame(data)

# 描述性统计
print("描述性统计：")
print(df.describe())

# 绘制散点图
plt.figure(figsize=(12, 6))
sns.pairplot(df, x_vars=['X1', 'X2', 'X3'], y_vars=['y'], kind='scatter')
plt.show()

# 提取自变量和因变量
X = df[['X1', 'X2', 'X3']]
y = df['y']

# 添加常数项
X = sm.add_constant(X)

# 计算多元线性回归模型
model = sm.OLS(y, X).fit()

# 打印回归结果
print(model.summary())

# 异方差检验
print("\n异方差检验：")
print("Breusch-Pagan test p-value:", het_breuschpagan(model.resid, X)[1])
print("White test p-value:", het_white(model.resid, X)[1])

# 多重共线性检验
print("\n多重共线性检验：")
vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print("VIF:", vif)
