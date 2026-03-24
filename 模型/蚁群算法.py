import numpy as np

# 设置距离矩阵，假设是对称的，对角线为0
distance_matrix = np.array([
    [0, 2, 9, np.inf],
    [1, 0, 6, 4],
    [np.inf, 7, 0, 8],
    [6, 3, np.inf, 0]
])

# 参数设置
num_ants = 4
num_cities = distance_matrix.shape[0]
num_iterations = 100
decay = 0.1
alpha = 1
beta = 2

# 初始化信息素矩阵
pheromone_matrix = np.ones((num_cities, num_cities))
pheromone_matrix = pheromone_matrix / num_cities

for iteration in range(num_iterations):
    all_paths = []
    all_distances = []

    # 每个蚂蚁构建一条路径
    for ant in range(num_ants):
        path = [np.random.randint(0, num_cities)]  # 随机选择起点
        while len(path) < num_cities:
            current_city = path[-1]
            # 计算转移概率
            probabilities = pheromone_matrix[current_city] ** alpha * ((1 / distance_matrix[current_city]) ** beta)
            probabilities[path] = 0  # 已经访问过的城市概率设置为0
            probabilities /= probabilities.sum()  # 归一化
            next_city = np.random.choice(num_cities, p=probabilities)
            path.append(next_city)

        distance = sum([distance_matrix[path[i - 1], path[i]] for i in range(1, num_cities)])
        all_paths.append(path)
        all_distances.append(distance)

    # 更新信息素
    shortest_distance = min(all_distances)
    shortest_path = all_paths[all_distances.index(shortest_distance)]
    for i in range(1, num_cities):
        from_city = shortest_path[i - 1]
        to_city = shortest_path[i]
        pheromone_matrix[from_city, to_city] += 1.0 / shortest_distance

    # 信息素挥发
    pheromone_matrix *= (1 - decay)

# 输出找到的最短路径和距离
print("最短路径:", shortest_path)
print("最短距离:", shortest_distance)