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


# 模拟退火算法
def simulated_annealing(cities, initial_temp, L, K, final_temp):
    num_cities = len(cities)

    # 初始化路径，随机生成初始路径
    current_path = np.random.permutation(num_cities)
    best_path = current_path.copy()

    # 计算初始路径的距离
    current_distance = calculate_distance(current_path, cities)
    best_distance = current_distance

    # 记录每次迭代的最佳值
    distances = []

    # 初始温度
    T = initial_temp

    # 迭代直到温度降低到终止温度
    while T > final_temp:
        for _ in range(L):
            # 随机交换路径中的两个城市
            new_path = current_path.copy()
            swap_idx = np.random.choice(num_cities, 2, replace=False)
            new_path[swap_idx[0]], new_path[swap_idx[1]] = new_path[swap_idx[1]], new_path[swap_idx[0]]

            # 计算新路径的距离
            new_distance = calculate_distance(new_path, cities)

            # 如果新解更优，接受新解
            if new_distance < current_distance:
                current_path = new_path
                current_distance = new_distance

                # 更新最佳路径
                if new_distance < best_distance:
                    best_path = new_path
                    best_distance = new_distance
            else:
                # 如果新解较差，根据Metropolis准则决定是否接受
                deltaE = new_distance - current_distance
                if np.random.rand() < np.exp(-deltaE / T):
                    current_path = new_path
                    current_distance = new_distance

        # 降温
        T = K * T
        distances.append(best_distance)  # 记录每次迭代的最佳距离

    # 输出最终结果
    print(f"Best Distance: {best_distance}")
    print(f"Best Path: {best_path}")

    # 绘制收敛曲线
    plt.plot(distances)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Convergence Curve of Simulated Annealing')
    plt.show()

    # 绘制最优路径
    path_coords = cities[best_path]
    plt.figure(figsize=(10, 8))
    plt.plot(path_coords[:, 0], path_coords[:, 1], '-o', markersize=6, color='b')
    plt.scatter(cities[:, 0], cities[:, 1], color='r', marker='x')
    plt.title('Best Path Found by Simulated Annealing')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    for i, txt in enumerate(best_path):
        plt.annotate(txt, (path_coords[i, 0], path_coords[i, 1]), textcoords="offset points", xytext=(0, 5),
                     ha='center')
    plt.grid(True)
    plt.show()


# 设置参数
initial_temp = 10000  # 初始温度
L = 1000  # 每轮迭代次数
K = 0.995  # 温度衰减参数
final_temp = 1  # 终止温度

# 调用模拟退火算法
simulated_annealing(cities, initial_temp, L, K, final_temp)
