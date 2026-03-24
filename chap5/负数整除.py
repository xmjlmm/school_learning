# class Solution:
#     def findSmallestInteger(self, nums: list[int], value: int) -> int:
#         n = len(nums)
#         ls = [0] * value
#         for i in range(n):
#             tmp = nums[i]
#             yu = tmp % value
#             ls[yu] = ls[yu] + 1
#         print(ls)
#         for j in range(value):
#             if (ls[j] == 0):
#                 print(j+1)
#                 break

# s = Solution()
# s.findSmallestInteger([1,-10,7,13,6,8], 5)



a = 0.2 * 1
b = a * 0.6 * 0.5
c = b * 0.6 * 0.5
d = c * 0.6 * 0.5
e = b * 0.4 * 1
f = 0.018 * 0.4 + 0.024 * 0.8
print(f)