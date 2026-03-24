
# 首先，导入必要的库
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score, calinski_harabasz_score


# 使用make_blobs生成一个随机数据集
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# 使用k-means算法对数据集进行聚类
def cluster_with_kmeans(X, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    labels = kmeans.fit_predict(X)
    silhouette_avg = silhouette_score(X, labels)
    calinski_harabasz = calinski_harabasz_score(X, labels)
    return labels, silhouette_avg, calinski_harabasz

# 使用高斯混合模型(GMM)进行聚类
def cluster_with_gmm(X, n_components=3):
    gmm = GaussianMixture(n_components=n_components, random_state=0)
    gmm.fit(X)
    labels = gmm.predict(X)
    silhouette_avg = silhouette_score(X, labels)
    calinski_harabasz = calinski_harabasz_score(X, labels)
    return labels, silhouette_avg, calinski_harabasz

# 降维并可视化聚类效果
def visualize_clusters(X, labels):
    tsne = TSNE(n_components=2, random_state=0)
    X_tsne = tsne.fit_transform(X)
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels, cmap='viridis')
    plt.colorbar()
    plt.show()

# 对数据集进行k-means聚类
labels_kmeans, silhouette_avg_kmeans, calinski_harabasz_kmeans = cluster_with_kmeans(X)
# 可视化k-means聚类结果
visualize_clusters(X, labels_kmeans)

# 对数据集进行GMM聚类
labels_gmm, silhouette_avg_gmm, calinski_harabasz_gmm = cluster_with_gmm(X)
# 可视化GMM聚类结果
visualize_clusters(X, labels_gmm)

# 返回两种聚类方法的轮廓系数和Calinski-Harabasz指数
print((silhouette_avg_kmeans, calinski_harabasz_kmeans), (silhouette_avg_gmm, calinski_harabasz_gmm))


'''
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# 生成模拟数据集
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# 定义函数计算轮廓系数和Calinski-Harabasz指数
def calculate_metrics(X, cluster_labels):
    silhouette_avg = silhouette_score(X, cluster_labels)
    calinski_harabasz = calinski_harabasz_score(X, cluster_labels)
    return silhouette_avg, calinski_harabasz

# 聚类函数
def cluster_data(X, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
    return kmeans.labels_

# 聚类并计算指标
labels_3_clusters = cluster_data(X, 3)
silhouette_avg_3, calinski_harabasz_3 = calculate_metrics(X, labels_3_clusters)

labels_2_clusters = cluster_data(X, 2)
silhouette_avg_2, calinski_harabasz_2 = calculate_metrics(X, labels_2_clusters)

# 打印轮廓系数和Calinski-Harabasz指数
print("Silhouette Coefficient for 3 clusters:", silhouette_avg_3)
print("Calinski-Harabasz Index for 3 clusters:", calinski_harabasz_3)
print("Silhouette Coefficient for 2 clusters:", silhouette_avg_2)
print("Calinski-Harabasz Index for 2 clusters:", calinski_harabasz_2)

# TSNE 降维以可视化
tsne = TSNE(n_components=2, random_state=0)
X_tsne = tsne.fit_transform(X)

# 绘制散点图
def plot_tsne(X_tsne, labels, title):
    plt.figure(figsize=(10, 8))
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels, cmap='viridis')
    plt.title(title)
    plt.colorbar()
    plt.xlabel('TSNE_dimension1')
    plt.ylabel('TSNE_dimension2')
    plt.show()

# 绘制3个聚类的TSNE散点图
plot_tsne(X_tsne, labels_3_clusters, "Visualized 3 clusters projected on")'''
