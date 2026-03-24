'''
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

# 设置随机数种子
np.random.seed(1)

# 生成一些随机数据
X = np.random.normal(0, 1, 1000)
Y = X + np.random.normal(0, 1, 1000)
Z = X + Y + np.random.normal(0, 1, 1000)

df = pd.DataFrame({'X': X, 'Y': Y, 'Z': Z})


# 执行线性回归得到残差
X_res = sm.OLS(df['X'], df['Z']).fit().resid
Y_res = sm.OLS(df['Y'], df['Z']).fit().resid

# 计算残差的皮尔逊相关系数，就是偏相关系数
pr, p_value = stats.pearsonr(X_res, Y_res)

print('在控制Z之后，X和Y的偏相关系数为：',pr)

'''

import numpy as np
import statsmodels.api as sm
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties
# np.random.seed(0)
data = pd.read_excel("F://数模//国赛//模型//相关系数//八年级女生体测数据.xlsx")
# data = pd.DataFrame(np.random.rand(100, 6), columns=['身高', '体重', '肺活量', '50米跑', '立定跳远', '坐位体前屈'])

font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# 计算每两个指标间的偏相关系数
# df = pd.DataFrame()
df = pd.DataFrame(index=data.columns, columns=data.columns)
for x in data.columns:
    for y in data.columns:
        if x != y: # 只计算不同指标间的偏相关系数
            other_vars = [var for var in data.columns if var != x and var != y]
            x_resid = sm.OLS(data[x], data[other_vars]).fit().resid
            y_resid = sm.OLS(data[y], data[other_vars]).fit().resid
            pr, pvalue = stats.pearsonr(x_resid, y_resid)
            df.loc[x, y] = pr
df.fillna(1, inplace=True)
print(df)

df.index = ['身高', '体重', '肺活量', '50米跑', '立定跳远', '坐位体前屈']

# 绘制热力图
plt.figure(figsize=(12,8))
sns.heatmap(df.astype('float64'), annot=True, fmt=".1f", linewidths=.5, cmap='YlGnBu')
# sns.heatmap(df, annot=True, fmt=".1f", linewidths=.5, cmap='coolwarm')

# 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu'
# 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'

# 添加标题和坐标轴标签
plt.title('heatmap')
# plt.title('数据热力图', fontproperties = font)

plt.show()