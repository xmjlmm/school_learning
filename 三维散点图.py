from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 生成样本数据, 共1000个点，分布在5个簇中
# X的每个元素都是其所在坐标的列表(长度为3，因为数据三维)，y是其所在簇的索引
X, y = make_blobs(n_samples=1000, n_features=3, centers=5)

# 创建模型，指定簇的个数
model = KMeans(n_clusters=3)
# 对数据进行聚类
model.fit(X)
# 获得聚类效果的标签(实际上和y相同)
labels = model.labels_

# 创建一个新的matplotlib的figure
fig = plt.figure()

# 在figure上创建一个三维的axes
ax = fig.add_subplot(111, projection='3d')

# 将数据分别用三维坐标系表示
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels)

# 显示图形
plt.show()