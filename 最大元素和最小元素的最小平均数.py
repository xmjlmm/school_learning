class Solution:
    def minimumAverage(self, nums: list[int]) -> float:
        nums.sort()
        print(nums)
        n, aver, i, mid = len(nums), [], 0, len(nums) // 2 - 1
        for i in range(0, mid + 1, 1):
            print(nums[i], '  ', nums[n-i-1], '   ', )
            aver.append((nums[i] + nums[n - i - 1]) / 2)
        print(aver)
        return min(aver)


def main():
    s = Solution()
    nums = [7,8,3,4,15,13,4,1]
    print(s.minimumAverage(nums))

if __name__ == "__main__":
    main()