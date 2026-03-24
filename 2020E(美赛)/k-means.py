import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 示例数据
data = {
    'X1': [1.0, 1.5, 3.0, 5.0, 3.5, 4.5, 3.5],
    'X2': [1.0, 2.0, 4.0, 7.0, 5.0, 5.0, 4.5]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 使用KMeans进行聚类
kmeans = KMeans(n_clusters=2)  # 设定要形成的聚类数为2
kmeans.fit(df)

# 获取聚类中心和标签
centroids = kmeans.cluster_centers_
labels = kmeans.labels_

# 绘制结果
colors = ["g.", "r.", "c.", "y."]  # 不同聚类的颜色

for i in range(len(df)):
    plt.plot(df['X1'][i], df['X2'][i], colors[labels[i]], markersize=10)

plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=150, linewidths=5)
plt.title('K-Means Clustering')
plt.xlabel('X1')
plt.ylabel('X2')
plt.show()
