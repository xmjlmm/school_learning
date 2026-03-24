import math

class Solution:
    def maximumPrimeDifference(self, nums: list[int]) -> int:
        left_index, right_index = 0, len(nums) - 1
        left_num, right_num = nums[left_index], nums[right_index]
        while not self.isPrime(left_num) or not self.isPrime(right_num):
            if not self.isPrime(left_num):
                left_index = left_index + 1
                left_num = nums[left_index]
            if not self.isPrime(right_num):
                right_index = right_index - 1
                right_num = nums[right_index]
        print(left_index, right_index)
        return right_index - left_index

    def isPrime(self, n):
        if n == 1 or n == 0:
            return 0
        for i in range(2, int(math.sqrt(n)+1)):
            if n % i == 0:
                return 0
        return 1


def main():
    s = Solution()
    nums = [4,8,2,8]
    print(s.maximumPrimeDifference(nums))

if __name__ == '__main__':
    main()