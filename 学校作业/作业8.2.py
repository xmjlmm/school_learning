'''假设图G采用邻接表存储，设计一个算法，判断无向图G是否连通。
若连通则返回1，否则返回0。并设计主函数调用上述算法，输出判断结果。'''

class Graph:
    def __init__(self, v):
        self.v = v
        self.adj = [[] for _ in range(v)]

    def add_edge(self, s, e):
        self.adj[s].append(e)
        self.adj[e].append(s)

    def dfs(self, s, visited):
        visited[s] = True
        for e in self.adj[s]:
            if not visited[e]:
                self.dfs(e, visited)

    def is_connected(self):
        visited = [False] * self.v
        self.dfs(0, visited)
        return all(visited)

def main():
    n = int(input('请输入顶点的个数'))
    m = int(input('请输入边的个数'))
    g = Graph(n)
    for _ in range(m):
        a, b = map(int, input('请输入边的两个顶点：').split())
        g.add_edge(a, b)
    if g.is_connected():
        print("The graph is connected.")
    else:
        print("The graph is not connected.")

if __name__ == "__main__":
    main()
