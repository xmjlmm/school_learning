class UnionFind:
    def __init__(self, size):
        # 初始化父节点和秩（rank）
        self.parent = list(range(size))
        self.rank = [1] * size

    def find_set(self, x):
        # 查找根节点，并进行路径压缩
        if self.parent[x] != x:
            self.parent[x] = self.find_set(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # 合并两个集合
        root_x = self.find_set(x)
        root_y = self.find_set(y)

        if root_x != root_y:
            # 按秩合并，较小的根指向较大的根
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

def main():
    # 输入人数和亲戚关系
    n, m, q = map(int, input().split())
    uf = UnionFind(n + 1)  # 创建并查集，索引从1到n

    # 处理亲戚关系
    for _ in range(m):
        a, b = map(int, input().split())
        uf.union(a, b)

    # 处理查询
    for _ in range(q):
        c, d = map(int, input().split())
        if uf.find_set(c) == uf.find_set(d):
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    main()
