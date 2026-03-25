'''
import seaborn as sns
import numpy as np

# 生成随机数据
data = np.random.rand(10, 10)

# 调用heatmap函数绘制热力图
sns.heatmap(data)
sns.show()
'''
'''
import matplotlib.pyplot as plt
import numpy as np

# 生成随机数据
x = np.random.rand(10)
y = np.random.rand(10)
z = np.random.rand(10) * 100

# 绘制散点图
plt.scatter(x, y, c=z, cmap='coolwarm')
plt.colorbar()

# 设置坐标轴标签和标题
plt.xlabel('x')
plt.ylabel('y')
plt.title('基于坐标轴的热力图')
plt.show()
'''
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 生成随机数据
x = np.linspace(0, 10, 50)
y = np.linspace(0, 5, 25)
x, y = np.meshgrid(x, y)
z = np.sin(x) + np.cos(y)

# 创建三维画布和坐标轴
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制三维热力图
ax.plot_surface(x, y, z, cmap='coolwarm')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('三维热力图')
plt.show()
'''
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 生成示例数据
x = np.linspace(-5, 5, 50)  # X 范围
y = np.linspace(-5, 5, 50)  # Y 范围
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))  # 示例函数

# 创建三维热力图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
heatmap = ax.plot_surface(X, Y, Z, cmap='viridis')  # 你可以选择其他的颜色映射

# 添加颜色条
fig.colorbar(heatmap, ax=ax, shrink=0.5, aspect=10)

# 设置标签和标题
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_zlabel('Z轴')
ax.set_title('三维热力图示例')

# 显示图像
plt.show()
'''
'''    
d = {}
for i in range(26):
    d[chr(i+ord('A'))] = chr((i+13)%26+ord('A'))
    for c in 'python':
        print(d.get(c,c),end='')
'''

# import seaborn as sns
# import matplotlib.pyplot as plt
# import pandas as pd
# from matplotlib.font_manager import FontProperties
# import matplotlib
#
# # 设置中文显示
# font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)
#
# matplotlib.rcParams["font.family"] = "Times New Roman"
#
# # 建立一个DataFrame示例数据
# data = {'ecology': [1/3, 1/3, 1, 1/2, 1/3],
#         'technology': [3/8, 3/1, 1/2, 1/2, 1/3],
#         'science': [1, 1/5, 1, 2, 1],
#         'biology': [1/3, 1/4, 1, 1, 1],
#         'class': [1/5, 1/5, 1/4, 1, 1]}
# df = pd.DataFrame(data)
#
# df.index = ['class', 'biology', 'science', 'technology', 'ecology']
#
# # 绘制热力图
# plt.figure(figsize=(12,8))
# sns.heatmap(df, annot=True, fmt=".1f", linewidths=.5, cmap='YlGnBu')
# # sns.heatmap(df, annot=True, fmt=".1f", linewidths=.5, cmap='coolwarm')
#
# # 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu'
# # 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'
#
# # 添加标题和坐标轴标签
# plt.title('heatmap')
# plt.title('数据热力图', fontproperties = font)
#
# plt.show()


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
import matplotlib

# 设置中文显示
font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)

matplotlib.rcParams["font.family"] = "Times New Roman"

# 建立一个DataFrame示例数据
data = {'ESG':[1,	-0.00721967908862746,	-0.500824996891885,	0.127525419851499],
        'Increasing':[-0.00721967908862746,	1,	-0.310738479416047,	0.0337926373475762],
        'ROE':[-0.500824996891885,	-0.310738479416047,	1,	0.569166758078173],
        'ROA':[0.127525419851499,	0.0337926373475762,	0.569166758078173,	1]}
df = pd.DataFrame(data)

df.index = ['ESG', 'Increasing', 'ROE', 'ROA']


# 绘制热力图
plt.figure(figsize=(12,8))
# sns.heatmap(df, annot=True, fmt=".3f", linewidths=.5, cmap='YlGnBu')
# sns.heatmap(df, annot=True, fmt=".3f", linewidths=.5, cmap='coolwarm')
# sns.heatmap(df, annot=True, fmt=".3f", linewidths=.5, cmap='PuBu')
# sns.heatmap(df, annot=True, fmt=".3f", linewidths=.5, cmap='OrRd')
# sns.heatmap(df, annot=True, fmt=".3f", linewidths=.5, cmap='GnBu')
# sns.heatmap(df, annot=True, fmt=".3f", linewidths=.5, cmap='RdPu')
# sns.heatmap(df, annot=True, fmt=".3f", linewidths=.5, cmap='PuBuGn')
sns.heatmap(df, annot=True, fmt=".3f", linewidths=.5, cmap='YlGn')
# 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu'
# 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'

# 添加标题和坐标轴标签
plt.title('heatmap')
plt.title('数据热力图', fontproperties = font)

plt.show()





