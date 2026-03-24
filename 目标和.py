# # 深度搜索，时间复杂度来不及，淦，放弃了，深度搜索就是垃圾
# class Solution:
#     def findTargetSumWays(self, nums: list[int], target: int) -> int:
#         nums.sort()  # 排序数组
#         self.ans = 0
#         self.length = len(nums)
#
#         def dfs(index = 0, sum_now = 0):
#             # 判断dfs结束条件
#             if index == self.length:
#                 if sum_now == target:
#                     self.ans += 1
#                 return
#
#             # 要剪枝，否则时间复杂度来不及
#             # 计算剩余元素的和
#             remaining_sum = sum(nums[index:])
#
#             # 剪枝：如果当前 sum_now 加上剩余元素的和仍小于 target，则不必继续递归
#             if sum_now + remaining_sum < target:
#                 return
#
#             # 剪枝：如果当前 sum_now 减去剩余元素的和仍大于 target，则不必继续递归
#             if sum_now - remaining_sum > target:
#                 return
#
#             dfs(index + 1, sum_now + nums[index])
#             dfs(index + 1, sum_now - nums[index])
#
#         dfs()
#         return self.ans
#
# def main():
#     s = Solution()
#     nums = [2,7,9,13,27,31,37,3,2,3,5,7,11,13,17,19,23,29,47,53]
#     target = 37
#     print(s.findTargetSumWays(nums, target))
#
#
# if __name__ == '__main__':
#     main()

# # 现在是动态规划实现这一问题
# class Solution:
#     def findTargetSumWays(self, nums: list[int], target: int) -> int:
#         # 计算数组的总和
#         total_sum = sum(nums)
#
#         # 如果总和不能满足条件，直接返回 0
#         if abs(target) > total_sum or (target + total_sum) % 2 != 0:
#             return 0
#
#         # 目标和
#         subset_sum = (target + total_sum) // 2
#
#         # 初始化 dp 数组，dp[j] 表示达到和 j 的方法数
#         dp = [0] * (subset_sum + 1)
#         dp[0] = 1  # 初始和为 0 的方法数为 1
#
#         # 动态规划更新 dp 数组
#         for num in nums:
#             for j in range(subset_sum, num - 1, -1):
#                 dp[j] += dp[j - num]
#
#         return dp[subset_sum]
#
#
# def main():
#     s = Solution()
#     nums = [1, 1, 1, 1, 1]
#     target = 3
#     print(s.findTargetSumWays(nums, target))
#
#
# if __name__ == '__main__':
#     main()



# 现在是动态规划实现这一问题
class Solution:
    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        sum_nums, length = sum(nums), len(nums)
        diff = (sum_nums - target)
        if diff < 0 or diff % 2 != 0:
            return 0
        neg = diff // 2
        dp = [[0] * (neg + 1) for _ in range(length+1)]
        dp[0][0] = 1
        for i in range(1, length+1):
            num = nums[i-1]
            for j in range(0, neg+1, 1):
                dp[i][j] = dp[i-1][j]
                if j >= num:
                    dp[i][j] = dp[i-1][j] + dp[i-1][j-num]
                else:
                    dp[i][j] = dp[i-1][j]
        # print(dp)
        return dp[length][neg]


def main():
    s = Solution()
    nums = [1, 1, 1, 1, 1]
    target = 3
    print(s.findTargetSumWays(nums, target))


if __name__ == '__main__':
    main()