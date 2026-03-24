# class Solution:
#     def duplicateNumbersXOR(self, nums: list[int]) -> int:
#         d, ans = {}, 0
#         for i in (nums):
#             if i in d:
#                 d[i] += 1
#             else:
#                 d[i] = 1
#         for i in d:
#             if d[i] == 2:
#                 ans = ans ^ i
#         return i
#
#
#
# def main():
#     nums = [1,2,1,3]
#     s = Solution()
#     print(s.duplicateNumbersXOR(nums))
#
# if __name__ == "__main__":
#     main()











class Solution:
    def duplicateNumbersXOR(self, nums: list[int]) -> int:
        cnt, ans = set(), 0
        for i in nums:
            if i in cnt:
                ans = ans ^ i
            else:
                cnt.add(i)
        return ans

def main():
    nums = [1,2,1,2]
    s = Solution()
    print(s.duplicateNumbersXOR(nums))

if __name__ == "__main__":
    main()





