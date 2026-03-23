import numpy as np
import matplotlib.pyplot as plt

# 城市坐标（31个城市）
cities = np.array([
    [1304, 2312], [3639, 1315], [4177, 2244], [3712, 1399], [3488, 1535],
    [3326, 1556], [3238, 1229], [4196, 1044], [4312, 790], [4386, 570],
    [3007, 1970], [2562, 1756], [2788, 1491], [2381, 1676], [1332, 695],
    [3715, 1678], [3918, 2179], [4061, 2370], [3780, 2212], [3676, 2578],
    [4029, 2838], [4263, 2931], [3429, 1908], [3507, 2376], [3394, 2643],
    [3439, 3201], [2935, 3240], [3140, 3550], [2545, 2357], [2778, 2826],
    [2370, 2975]
])

num_cities = len(cities)


# 计算路径的总距离
def calculate_distance(path, cities):
    distance = 0
    for i in range(len(path) - 1):
        distance += np.linalg.norm(cities[path[i]] - cities[path[i + 1]])
    distance += np.linalg.norm(cities[path[-1]] - cities[path[0]])  # 回到起点
    return distance


# 禁忌搜索算法
def tabu_search(cities, max_iter, TabuL, Ca, CaNum):
    num_cities = len(cities)

    # 初始化路径，随机生成初始路径
    current_path = np.random.permutation(num_cities)
    best_path = current_path.copy()

    # 计算初始路径的距离
    current_distance = calculate_distance(current_path, cities)
    best_distance = current_distance

    # 初始化禁忌表
    Tabu = np.zeros((num_cities, num_cities), dtype=int)

    # 用于记录每次迭代的最佳值
    distances = []

    for iteration in range(max_iter):
        candidate_solutions = []

        # 生成候选解
        for _ in range(CaNum):
            # 随机交换路径中的两个城市
            new_path = current_path.copy()
            swap_idx = np.random.choice(num_cities, 2, replace=False)
            new_path[swap_idx[0]], new_path[swap_idx[1]] = new_path[swap_idx[1]], new_path[swap_idx[0]]

            # 计算新路径的距离
            new_distance = calculate_distance(new_path, cities)
            candidate_solutions.append((new_path, new_distance))

        # 按照路径长度从小到大排序候选解
        candidate_solutions = sorted(candidate_solutions, key=lambda x: x[1])

        # 选择前Ca/2个最好的候选解
        BestCa = candidate_solutions[:Ca // 2]

        # 选择最佳候选解
        best_candidate = None
        for path, dist in BestCa:
            # 判断候选解是否在禁忌表中
            swap_idx = tuple(sorted((path[0], path[1])))
            if Tabu[swap_idx[0], swap_idx[1]] == 0:  # 如果不在禁忌表
                best_candidate = (path, dist)
                break

        if best_candidate is None:
            best_candidate = BestCa[0]

        new_path, new_distance = best_candidate

        # 如果新解更优，更新当前解及最优解
        if new_distance < best_distance:
            best_path = new_path
            best_distance = new_distance

        # 更新禁忌表
        for i in range(len(new_path) - 1):
            Tabu[new_path[i], new_path[i + 1]] = TabuL  # 设置新的禁忌
            Tabu[new_path[i + 1], new_path[i]] = TabuL  # 对称更新禁忌表

        # 更新当前解
        current_path = new_path

        # 更新禁忌表并减少禁忌长度
        Tabu = np.maximum(Tabu - 1, 0)

        # 记录每次迭代的最佳距离
        distances.append(best_distance)

    # 输出最终结果
    print(f"Best Distance: {best_distance}")
    print(f"Best Path: {best_path}")

    # 绘制收敛曲线
    plt.plot(distances)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Convergence Curve of Tabu Search')
    plt.show()

    # 绘制最优路径
    path_coords = cities[best_path]
    plt.figure(figsize=(10, 8))
    plt.plot(path_coords[:, 0], path_coords[:, 1], '-o', markersize=6, color='b')
    plt.scatter(cities[:, 0], cities[:, 1], color='r', marker='x')
    plt.title('Best Path Found by Tabu Search')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    for i, txt in enumerate(best_path):
        plt.annotate(txt, (path_coords[i, 0], path_coords[i, 1]), textcoords="offset points", xytext=(0, 5),
                     ha='center')
    plt.grid(True)
    plt.show()


# 设置参数
max_iter = 50000  # 最大迭代次数
TabuL = 100  # 禁忌长度
Ca = 1000  # 候选解数目
CaNum = 1000  # 每次生成的候选解数目

# 调用禁忌搜索算法
tabu_search(cities, max_iter, TabuL, Ca, CaNum)
