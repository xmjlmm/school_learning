import math
# 贪心+动态规划



# class Solution:
#     def minimumDistance(self, points: list[list[int]]) -> int:
#         delete_index, length, ans = 0, len(points), math.inf
#         for delete_index in range(length):
#             new_point, min_distance = points[0:delete_index:1] + points[delete_index + 1:length:1], 0
#
#             for i in range(0, length - 1, 1):
#                 for j in range(i + 1, length - 1, 1):
#
#                     cur_distance = abs(new_point[i][0] - new_point[j][0]) + abs(new_point[i][1] - new_point[j][1])
#                     if cur_distance > min_distance:
#                         min_distance = cur_distance
#             ans = min(ans, min_distance)
#
#         return ans

def main():
    s = Solution()
    nums = [[3,10],[5,15],[10,2],[4,4]]
    print(s.minimumDistance(nums))


if __name__ == '__main__':
    main()





