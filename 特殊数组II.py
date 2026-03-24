from itertools import pairwise

# 时间复杂度来不及
# class Solution:
#     def isArraySpecial(self, nums: list[int], queries: list[list[int]]) -> list[bool]:
#         ans = []
#         for query in queries:
#             any = nums[query[0]:query[1]:1]
#             print(any)
#             pair_any = pairwise(any)
#             flag = 0
#             print(pair_any)
#             for se in pair_any:
#                 if se[0] % 2 == se[1] % 2:
#                     ans.append('false')
#                     flag = 1
#                     print('111')
#                     break
#             if flag == 0:
#                 ans.append('true')
#
#         return ans




class Solution:
    def isArraySpecial(self, nums: list[int], queries: list[list[int]]) -> list[bool]:
        ans, n = [], len(nums)
        dp = [0 for _ in range(n+1)]
        for i in range(n-1):
            if nums[i] % 2 != nums[i+1] % 2:
                dp[i] = 1
            else:
                dp[i] = 0
        for p in queries:
            if sum(dp[p[0]:p[1]:1]) == p[1] - p[0]:
                ans.append(True)
            else:
                ans.append(False)
        return ans

def main():
    s = Solution()
    nums = [4,3,1,6]
    queries = [[0,2],[2,3]]
    print(s.isArraySpecial(nums, queries))

if __name__ == '__main__':
    main()