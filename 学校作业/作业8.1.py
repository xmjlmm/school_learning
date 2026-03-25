'''1. 假设图G采用邻接表存储，
设计一个程序，建立图G的邻接表存储结构，利用图的遍历算法，
分别求出图的深度优先遍历和广度优先遍历的顶点序列。
'''

class Graph(object):
    def __init__(self):
        self.adj = {}

    def add_edge(self, v1, v2):
        if v1 in self.adj:
            self.adj[v1].append(v2)
        else:
            self.adj[v1] = [v2]

        # 确保每个顶点都在邻接表中出现，即使它没有邻接顶点
        if v2 not in self.adj:
            self.adj[v2] = []

    def dfs(self, v, visited=None):
        if visited is None:
            visited = set()
        visited.add(v)
        # print(v)
        for neighbor in self.adj.get(v, []):  # 使用 get 方法，若顶点不存在则返回空列表
            if neighbor not in visited:
                self.dfs(neighbor, visited)
        return visited

    def bfs(self, v, visited=None):
        if visited is None:
            visited = set()
        queued = [v]
        visited.add(v)
        while queued:
            v = queued.pop(0)
            # print(v)
            for neighbor in self.adj.get(v, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queued.append(neighbor)
        return visited

def main():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 4)
    g.add_edge(3, 5)
    g.add_edge(4, 5)

    print("DFS:", g.dfs(1))
    print("BFS:", g.bfs(1))

if __name__ == "__main__":
    main()
