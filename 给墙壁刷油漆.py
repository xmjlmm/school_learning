# class Solution:
#     def paintWalls(self, cost: list[int], time: list[int]) -> int:
#         length = len(cost)
#         new_cost, new_time, new_average = [], [], []
#         average_cost = [cost[i] / time[i] for i in range(length)]
#         # 免费的工匠刷任意一堵墙为1，那么最长的时间为墙的个数
#         time_fee, time_free, total_fee = 0, length, 0
#         while time_fee < time_free:
#             # 每次从cost里面选开销最小的，加入到付费的工匠里面
#             min_cost = min(average_cost)
#             print(min_cost)
#             min_index = average_cost.index(min_cost)
#             total_fee = total_fee + cost[min_index]
#             time_fee = time_fee + time[min_index]
#             time_free = time_free - 1
#             # 添加已经加入的元素
#             new_cost.append(cost[min_index])
#             new_time.append(time[min_index])
#
#             # 需要删除列表中这个元素
#             del average_cost[min_index]
#             del cost[min_index]
#             del time[min_index]
#
#         # 开始删付费的工匠，直到付费的工匠时间恰好大于等于免费工匠的时间
#         excessive = time_fee - time_free
#
#
#         return total_fee
#
# def main():
#     s = Solution()
#     cost = [42,8,28,35,21,13,21,35]
#     time = [2,1,1,1,2,1,1,2]
#     print(s.paintWalls(cost, time))
#
# if __name__ == '__main__':
#     main()

class Solution:
    def paintWalls(self, cost: list[int], time: list[int]) -> int:
        n = len(cost)
        f = [inf] * (n * 2 + 1)
        f[n] = 0
        for (cost_i, time_i) in zip(cost, time):
            g = [inf] * (n * 2 + 1)
            for j in range(n * 2 + 1):
                # 动态规划的递推式
                # 付费
                # 付费时间大于等于免费时间
                g[min(j + time_i, n * 2)] = min(g[min(j + time_i, n * 2)], f[j] + cost_i)
                # 免费
                if j > 0:
                    g[j - 1] = min(g[j - 1], f[j])
            f = g
        return min(f[n:])

def main():
    s = Solution()
    cost = [42,8,28,35,21,13,21,35]
    time = [2,1,1,1,2,1,1,2]
    print(s.paintWalls(cost, time))

if __name__ == '__main__':
    main()