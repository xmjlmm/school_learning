from collections import deque

def topological_sort(graph):
    # 计算所有顶点的入度
    in_degree = {u: 0 for u in graph}  # 初始化入度为0
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    # 找到所有入度为0的顶点
    queue = deque([u for u in graph if in_degree[u] == 0])

    # 初始化排序结果列表
    order = []

    while queue:
        u = queue.popleft()  # 从队列中取出一个顶点
        order.append(u)  # 将其加入排序结果中
        for v in graph[u]:
            in_degree[v] -= 1  # 将该顶点指向的所有顶点的入度减1
            if in_degree[v] == 0:
                queue.append(v)  # 如果入度变为0，则加入队列

    # 如果排序结果中顶点的数量不等于图中顶点的数量，说明图中存在环，返回空列表
    if len(order) != len(graph):
        return []

    return order

def main():
    graph = {
        "A": ["C"],
        "B": ["C", "D"],
        "C": ["E"],
        "D": ["F"],
        "E": ["F"],
        "F": []
    }
    print("图中的顶点按拓扑排序的结果:", topological_sort(graph))

# 使用案例
if __name__ == "__main__":
    main()