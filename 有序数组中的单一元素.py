'''
给你一个仅由整数组成的有序数组，其中每个元素都会出现两次，唯有一个数只会出现一次。
请你找出并返回只出现一次的那个数。
你设计的解决方案必须满足 O(log n) 时间复杂度和 O(1) 空间复杂度。
示例 1:
输入: nums = [1,1,2,3,3,4,4,8,8]
输出: 2
示例 2:
输入: nums =  [3,3,7,7,10,11,11]
输出: 10
'''

'''# 小米椒的暴力
class Solution:
    def singleNonDuplicate(self, nums: list[int]) -> int:
        length = len(nums)
        if length == 1:
            return nums[0]
        cur_du, count = nums[0], 0
        for i in range(1, length):
            print('cur_du', cur_du, 'count', count)
            if nums[i] == cur_du:
                count = count + 1
            elif nums[i] != cur_du and count:
                cur_du = nums[i]
                count = 0
            else:
                return nums[i-1]


def main():
    s = Solution()
    nums = [3,3,7,7,10,11,11]
    print(s.singleNonDuplicate(nums))

if __name__ == '__main__':
    main()'''


# 瞄了一眼while left 和 right 推测二分, 进行尝试
# 个数一定是奇数, 那么二分一定偶数位置，如果等于左侧，则单元素在左侧，如果等于右侧，则氮元素在右侧
class Solution:
    def singleNonDuplicate(self, nums: list[int]) -> int:
        length = len(nums)
        left, right = 0, length-1

        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == nums[mid - 1]:
                left = mid + 1

            else:
                right = mid
        return nums[left]



def main():
    s = Solution()
    nums = [3, 3, 7, 7, 10, 11, 11]
    print(s.singleNonDuplicate(nums))

if __name__ == '__main__':
    main()