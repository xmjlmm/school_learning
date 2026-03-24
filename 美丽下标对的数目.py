class Solution:
    def countBeautifulPairs(self, nums: list[int]) -> int:
        length = len(nums)
        # 初始化
        ans = 0
        for i in range(0, length-1, 1):
            for j in range(i+1, length, 1):
                num1 = int(str(nums[i])[0])
                num2 = int(str(nums[j])[-1])
                if num1 == 0 or num2 == 0:
                    continue
                # 将较大的数放在num1
                if num1 < num2:
                    num1, num2 = num2, num1
                # 辗转相除法
                yushu = num1 % num2
                while yushu:
                    num1 = num2
                    num2 = yushu
                    yushu = num1 % num2
                if num2 == 1:
                    ans = ans + 1
        return ans
def main():
    solution = Solution()
    nums = [11,21,12]
    print(solution.countBeautifulPairs(nums))

if  __name__ == "__main__":
    main()







# 调试


# # 现在写一个哈希表的代码
# class Solution:
#     def countBeautifulPairs(self, nums: list[int]) -> int:
#         ans = 0
#         cnt = [0] * 10
#
#
#
# def main():
#     solution = Solution()
#     nums = [31,25,72,79,74]
#     print(solution.countBeautifulPairs(nums))
#
#
# if __name__ == '__main__':
#     main()