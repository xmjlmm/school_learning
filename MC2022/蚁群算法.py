import numpy as np

# 假设的距离矩阵，4个城市之间的距离
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

# 蚁群算法
for iteration in range(num_iterations):
    all_paths = []
    all_distances = []

    for ant in range(num_ants):
        path = [np.random.randint(0, num_cities)]  # 随机选择起点
        while len(path) < num_cities:
            current_city = path[-1]
            probabilities = np.zeros(num_cities)

            # 计算到各城市的转移概率
            for next_city in range(num_cities):
                if next_city not in path and distance_matrix[current_city, next_city] != np.inf:
                    pheromone = pheromone_matrix[current_city, next_city] ** alpha
                    heuristic = (1 / distance_matrix[current_city, next_city]) ** beta
                    probabilities[next_city] = pheromone * heuristic

            # 防止分母为0
            if np.sum(probabilities) == 0:
                break

            probabilities /= np.sum(probabilities)  # 归一化概率
            next_city = np.random.choice(num_cities, p=probabilities)
            path.append(next_city)

        # 计算路径总距离
        if len(path) == num_cities:
            path_distance = sum(distance_matrix[path[i], path[(i + 1) % num_cities]] for i in range(num_cities))
            all_paths.append(path)
            all_distances.append(path_distance)

    # 更新信息素
    pheromone_matrix *= (1 - decay)
    if all_distances:
        shortest_distance = min(all_distances)
        shortest_path = all_paths[np.argmin(all_distances)]
        for i in range(num_cities):
            from_city = shortest_path[i]
            to_city = shortest_path[(i + 1) % num_cities]
            pheromone_matrix[from_city, to_city] += 1 / shortest_distance

# 输出找到的最短路径和距离
if all_distances:
    print("最短路径:", shortest_path)
    print("最短距离:", shortest_distance)
