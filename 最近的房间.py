# class Solution:
#     def closestRoom(self, rooms: list[list[int]], queries: list[list[int]]) -> list[int]:
#         ans = []
#         for a, b in queries:
#             # 满足条件的房间号以及差值绝对值
#             flag = {}
#             for c, d in rooms:
#                 # b, d用来比较容量, c来存储号码, a来判断最接近的地方
#                 # d是用来比较的，真实房间的容量
#                 if d >= b:
#                     tmp = abs(a - c)
#                     flag[c] = tmp
#
#             if not flag:
#                 ans.append(-1)
#
#                 continue
#
#             sorted_flag = sorted(flag.items(), key=lambda x: (x[1], x[0]))
#             ans.append(sorted_flag[0][0])
#         return ans
#
#
# def main():
#     s = Solution()
#     rooms = [[1,4],[2,3],[3,5],[4,1],[5,2]]
#     queries = [[2,3],[2,4],[2,5]]
#     print(s.closestRoom(rooms, queries))
#
# if __name__ == '__main__':
#     main()
#
#
#


class Solution:
    def closestRoom(self, rooms: list[list[int]], queries: list[list[int]]) -> list[int]:
        ans = []
        sorted_rooms = sorted(rooms, key=lambda x: (x[1], [0]))
        return sorted_rooms

def main():
    s = Solution()
    rooms = [[1,4],[2,3],[3,5],[4,1],[5,2]]
    queries = [[2,3],[2,4],[2,5]]
    print(s.closestRoom(rooms, queries))

if __name__ == '__main__':
    main()