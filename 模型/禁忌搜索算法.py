import numpy as np
import random


def calculate_total_distance(route, distance_matrix):
    """计算给定路线的总距离"""
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i], route[i + 1]]
    total_distance += distance_matrix[route[-1], route[0]]
    return total_distance


def generate_initial_solution(num_cities):
    """生成初始解，即随机排列城市顺序"""
    route = list(range(num_cities))
    random.shuffle(route)
    return route


def get_neighbors(route):
    """生成邻居解，通过交换任意两个城市的位置"""
    neighbors = []
    for i in range(len(route)):
        for j in range(i + 1, len(route)):
            new_route = route[:]
            new_route[i], new_route[j] = new_route[j], new_route[i]
            neighbors.append(new_route)
    return neighbors


def tabu_search(distance_matrix, initial_solution, max_iterations, tabu_size, max_neighbors):
    """执行禁忌搜索算法"""
    best_solution = initial_solution
    best_cost = calculate_total_distance(best_solution, distance_matrix)
    current_solution = initial_solution
    current_cost = best_cost
    tabu_list = []

    for iteration in range(max_iterations):
        neighbors = get_neighbors(current_solution)
        best_neighbor = None
        best_neighbor_cost = float('inf')

        for neighbor in neighbors[:max_neighbors]:
            if neighbor not in tabu_list and calculate_total_distance(neighbor, distance_matrix) < best_neighbor_cost:
                best_neighbor = neighbor
                best_neighbor_cost = calculate_total_distance(neighbor, distance_matrix)

        if best_neighbor_cost < best_cost:
            best_cost = best_neighbor_cost
            best_solution = best_neighbor

        # 更新当前解和禁忌列表
        current_solution = best_neighbor
        tabu_list.append(best_neighbor)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        print(f"Iteration {iteration + 1}: Best Cost = {best_cost}")

    return best_solution, best_cost


# 定义城市间的距离矩阵
distance_matrix = np.array([
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
])

# 初始化参数
num_cities = 4
initial_solution = generate_initial_solution(num_cities)
max_iterations = 50
tabu_size = 10
max_neighbors = 20

# 运行禁忌搜索算法
best_route, best_distance = tabu_search(distance_matrix, initial_solution, max_iterations, tabu_size, max_neighbors)
print("Best Route:", best_route)
print("Best Distance:", best_distance)
