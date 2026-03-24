import numpy as np
import matplotlib.pyplot as plt

"""

在示例用法中，
随机生成了100个三维特征的数据样本，
然后创建了一个大小为$10 \times 10$的SOM模型，
进行数据训练和预测。最后打印出预测的BMU位置，
并通过可视化展示了SOM的权重映射。

使用SOM算法可以实现数据的降维可视化、聚类、异常检测等多种任务。
通过训练SOM模型，
可以观察数据样本在地图上的分布情况，
帮助理解数据的结构和特征之间的关系。"""


class SOM:
    def __init__(self, input_len, map_size, learning_rate=0.1, sigma=None, max_iter=100):
        """
        初始化SOM参数
        :param input_len: 输入特征的维度
        :param map_size: 自组织映射的大小 (宽, 高)
        :param learning_rate: 学习率
        :param sigma: 初始邻域范围
        :param max_iter: 最大迭代次数
        """
        self.input_len = input_len  # 输入数据的维度
        self.map_size = map_size      # SOM的大小
        self.learning_rate = learning_rate  # 学习率
        self.sigma = sigma if sigma is not None else map_size[0] / 2  # 邻域范围，如果没有指定则初始化为地图的一半
        self.max_iter = max_iter      # 最大迭代次数
        self.weights = np.random.rand(map_size[0], map_size[1], input_len)  # 初始化权重

    def _find_bmu(self, x):
        """
        找到最佳匹配单元（BMU）
        :param x: 输入样本
        :return: (bmu_x, bmu_y): BMU的坐标
        """
        bmu_idx = np.argmin(np.linalg.norm(self.weights - x, axis=2))  # 计算输入与权重间的欧几里得距离
        bmu_x, bmu_y = np.unravel_index(bmu_idx, self.map_size)  # 获取BMU的坐标
        return bmu_x, bmu_y

    def _update_weights(self, x, bmu):
        """
        更新权重
        :param x: 输入样本
        :param bmu: BMU的坐标
        """
        bmu_x, bmu_y = bmu  # 解构BMU坐标
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                # 计算到BMU的距离
                dist = np.sqrt((bmu_x - i) ** 2 + (bmu_y - j) ** 2)
                # 计算邻域函数
                theta = np.exp(-dist**2 / (2 * self.sigma**2))
                # 更新权重
                self.weights[i, j, :] += self.learning_rate * theta * (x - self.weights[i, j, :])

    def fit(self, data):
        """
        训练自组织映射
        :param data: 输入数据 (样本数, 特征数)
        """
        for iteration in range(self.max_iter):
            # 逐步降低学习率和邻域范围
            self.learning_rate = self.learning_rate * (1 - iteration / self.max_iter)
            self.sigma = self.sigma * (1 - iteration / self.max_iter)
            for x in data:
                bmu = self._find_bmu(x)  # 找到BMU
                self._update_weights(x, bmu)  # 更新权重

    def predict(self, data):
        """
        预测输入数据的BMU
        :param data: 输入数据 (样本数, 特征数)
        :return: 答案 (样本数, 2)，对应于地图中的BMU坐标
        """
        bmus = []
        for x in data:
            bmu = self._find_bmu(x)
            bmus.append(bmu)
        return np.array(bmus)

    def plot_map(self):
        """
        可视化SOM的权重
        """
        plt.imshow(self.weights.reshape(self.map_size[0], self.map_size[1], self.input_len), aspect='auto')
        plt.title('SOM Weights Map')
        plt.colorbar()
        plt.show()

# 示例用法
if __name__ == '__main__':
    # 生成一些随机数据点
    data = np.random.rand(100, 3)  # 100个样本，3个特征
    som = SOM(input_len=3, map_size=(10, 10), learning_rate=0.3, max_iter=200)
    som.fit(data)  # 训练SOM
    bmus = som.predict(data)  # 预测BMU
    print("预测的BMU位置:\n", bmus)
    som.plot_map()  # 显示权重映射
