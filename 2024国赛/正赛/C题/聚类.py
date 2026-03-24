# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# # 1. 读取数据
# data = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理单价(已处理).xlsx",sheet_name="Sheet1")  # 替换为你的数据文件名
#
# # 2. 数据预处理
# # 去除重复的作物名称（保留第一个出现的）
# data = data.drop_duplicates(subset=['作物名称'])
#
# # 选择聚类的特征
# features = ['种植面积/亩', '亩产量/斤', '种植成本/(元/亩)', '销售单价(最小值)', '销售单价(最大值)', '预期销售量']
#
# # 选择用于聚类的列
# cluster_data = data[features]
#
# # 处理缺失值
# # 可以选择删除缺失值行
# cluster_data_clean = cluster_data.dropna()
# data_clean = data.loc[cluster_data_clean.index]  # 保留对应的行
#
# # 或者用均值填补缺失值（不推荐删除）
# # cluster_data_clean = cluster_data.fillna(cluster_data.mean())
# # data_clean = data
#
# # 确保所有聚类特征都是数值类型
# for col in features:
#     cluster_data_clean[col] = pd.to_numeric(cluster_data_clean[col], errors='coerce')
#
# # 处理因转换而产生的NaN值
# cluster_data_clean = cluster_data_clean.dropna()
# data_clean = data.loc[cluster_data_clean.index]
#
# # 数据标准化
# scaler = StandardScaler()
# scaled_data = scaler.fit_transform(cluster_data_clean)
#
# # 3. 确定聚类数量
# # 使用肘部法则（Elbow Method）来选择合适的K值
# inertia = []
# K_range = range(1, 11)  # 测试1到10个聚类
# for k in K_range:
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(scaled_data)
#     inertia.append(kmeans.inertia_)
#
# # 绘制肘部法则图
# plt.figure(figsize=(8, 5))
# plt.plot(K_range, inertia, marker='o')
# plt.xlabel('Number of Clusters (K)')
# plt.ylabel('Inertia')
# plt.title('Elbow Method for Optimal K')
# plt.show()
#
# # 选择K值，例如假设从图中选择K=3
# optimal_k = 3
#
# # 4. 聚类
# kmeans = KMeans(n_clusters=optimal_k, random_state=42)
# clusters = kmeans.fit_predict(scaled_data)
#
# # 将聚类结果添加到数据中
# data_clean['Cluster'] = clusters
#
# # 5. 结果分析和可视化
# # 聚类结果概述
# print(data_clean.groupby('Cluster').mean(numeric_only=True))
#
# # 可视化
# plt.figure(figsize=(10, 8))
# sns.scatterplot(data=data_clean, x='种植面积/亩', y='亩产量/斤', hue='Cluster', palette='tab10')
# plt.title('Clustering of Crops')
# plt.xlabel('种植面积/亩')
# plt.ylabel('亩产量/斤')
# plt.legend(title='Cluster')
# plt.show()
#
# # 可视化其他特征与聚类结果
# # 你可以使用类似的方式对其他特征进行可视化分析


import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties

# 用宋体
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=16)

# 1. 读取数据
data = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理单价(已处理).xlsx", sheet_name="Sheet1")  # 替换为你的数据文件名

# 2. 数据预处理
# 去除重复的作物名称（保留第一个出现的）
data = data.drop_duplicates(subset=['作物名称'])

# 选择聚类的特征
features = ['种植成本/(元/亩)', '销售单价(最大值)', '预期销售量']

# 选择用于聚类的列
cluster_data = data[features]

# 处理缺失值
cluster_data_clean = cluster_data.dropna()
data_clean = data.loc[cluster_data_clean.index]  # 保留对应的行

# 确保所有聚类特征都是数值类型
for col in features:
    cluster_data_clean[col] = pd.to_numeric(cluster_data_clean[col], errors='coerce')

# 处理因转换而产生的NaN值
cluster_data_clean = cluster_data_clean.dropna()
data_clean = data.loc[cluster_data_clean.index]

# 数据标准化
scaler = StandardScaler()
scaled_data = scaler.fit_transform(cluster_data_clean)

# 3. 确定聚类数量
# 使用肘部法则（Elbow Method）来选择合适的K值
inertia = []
K_range = range(1, 11)  # 测试1到10个聚类
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

# 绘制肘部法则图
plt.figure(figsize=(8, 5))
plt.plot(K_range, inertia, marker='o')
plt.xlabel('聚类个数', font = font)
plt.ylabel('聚合系数', font = font)
plt.title('肘部图', font = font)
plt.show()

# 选择K值，例如假设从图中选择K=3
optimal_k = 3

# 4. 聚类
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# 将聚类结果添加到数据中
data_clean['Cluster'] = clusters

# 5. 结果分析和可视化
# 聚类结果概述
print(data_clean.groupby('Cluster').mean(numeric_only=True))

# 绘制三维聚类分布图
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 提取聚类特征
x = data_clean['种植成本/(元/亩)']
y = data_clean['销售单价(最大值)']
z = data_clean['预期销售量']

# 绘制散点图
scatter = ax.scatter(x, y, z, c=data_clean['Cluster'], cmap='tab10', s=50, edgecolor='k')

# 添加标签
ax.set_xlabel('种植成本/(元/亩)', font = font)
ax.set_ylabel('销售单价', font = font)
ax.set_zlabel('预期销售量', font = font)
ax.set_title('3D Clustering of Crops')

# 添加图例
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=plt.get_cmap('tab10')(i/optimal_k), markersize=10, label=f'Cluster {i}') for i in range(optimal_k)]
ax.legend(handles=handles, title='Cluster')

plt.show()
