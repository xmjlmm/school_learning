import numpy as np
import matplotlib.pyplot as plt
import math
"""
人工势能场避免陷入局部最优解
自适应信息素类比遗传算法的变异系数
蚁群算法类比遗传算法的交叉概率
"""
class AntColonyOptimizer:
    """ 人工势能场自适应信息素蚁群算法的实现，用于解决TSP问题 """
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        初始化蚁群算法
        :param distances: 城市间的距离矩阵
        :param n_ants: 蚂蚁的数量
        :param n_best: 每代留下的最佳蚂蚁数量
        :param n_iterations: 迭代次数
        :param decay: 信息素的蒸发率
        :param alpha: 信息素重要程度的参数
        :param beta: 势能重要程度的参数
        """
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        """ 运行蚁群算法，返回最短路径和其长度 """
        shortest_path = None
        shortest_path_len = float('inf')
        for i in range(self.n_iterations):
            all_paths = self.generate_all_paths()
            self.spread_pheromone(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path, shortest_path_len = self.find_shortest_path(all_paths, shortest_path, shortest_path_len)
        return shortest_path, shortest_path_len

    def generate_all_paths(self):
        """ 生成所有蚂蚁的路径 """
        all_paths = []
        for _ in range(self.n_ants):
            path = [np.random.randint(len(self.distances))]  # 随机选择起点
            while len(path) < len(self.distances):
                move_probs = self.move_probability(path[-1], path)
                next_city = self.roulette_wheel_selection(move_probs)
                path.append(next_city)
            all_paths.append((path, self.path_length(path)))
        return all_paths

    def move_probability(self, current_city, path):
        """ 计算从当前城市到其他城市的转移概率 """
        pheromone = np.copy(self.pheromone[current_city, :])
        pheromone[list(path)] = 0  # 已访问的城市设置为0

        distance = self.distances[current_city, :]
        attractiveness = 1 / (distance + 1e-10)  # 避免除以0

        return pheromone ** self.alpha * attractiveness ** self.beta

    def roulette_wheel_selection(self, probs):
        """ 轮盘赌选择 """
        cumulative_sum = np.cumsum(probs)
        r = sum(probs) * np.random.rand()
        city = np.where(cumulative_sum >= r)[0][0]
        return city

    def spread_pheromone(self, all_paths, n_best, shortest_path):
        """ 信息素的弥散和蒸发 """
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        self.pheromone *= self.decay  # 信息素蒸发
        for path, length in sorted_paths[:n_best]:
            for move in zip(path[:-1], path[1:]):
                self.pheromone[move[0], move[1]] += 1.0 / self.distances[move[0], move[1]]

    def find_shortest_path(self, all_paths, shortest_path, shortest_path_len):
        """ 查找最短路径 """
        for path, length in all_paths:
            if length < shortest_path_len:
                shortest_path_len = length
                shortest_path = path
        return shortest_path, shortest_path_len

    def path_length(self, path):
        """ 计算路径长度 """
        return sum([self.distances[path[i], path[i + 1]] for i in range(-1, len(path) - 1)])


# 假设有一个距离矩阵
distances = np.random.rand(10, 10)
np.fill_diagonal(distances, 0)
aco = AntColonyOptimizer(distances, n_ants=20, n_best=5, n_iterations=100, decay=0.80, alpha=1, beta=2)
shortest_path, length = aco.run()

print("最短路径：", shortest_path)
print("最短路径长度：", length)

# 可视化路径
plt.figure(figsize=(5, 5))
for i, (fro, to) in enumerate(zip(shortest_path[:-1], shortest_path[1:])):
    plt.plot([fro, to], [distances[fro], distances[to]], 'o-')
plt.show()
