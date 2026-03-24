class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        ans, records, n = [], [], len(edges)
        records.append(edges[0])
        for i in range(1, n):
            edge = edges[i]
            point_first = edge[0]
            point_second = edge[1]
            flag = 0
            for record in records:
                if point_first in record and point_second in record:
                    ans.append(edge)
                elif point_first in record and point_second not in record:
                    record.append(point_first)
                elif point_first not in record and point_second in record:
                    record.append(point_second)
                else:
                    records.append(edge)
        return ans[-1]

def main():
    s = Solution()
    edges = [[9,10],[5,8],[2,6],[1,5],[3,8],[4,9],[8,10],[4,10],[6,8],[7,9]]
    print(s.findRedundantConnection(edges))

if __name__ == "__main__":
    main()