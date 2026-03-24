'''
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        front = []
        length = len(nums)
        sun = 0
        for i in range(length):
            sun = sun + nums[i]
            front.append(sun)
        for j in range(0, length):
            if j == 0 and front[-1] - front[0] == 0:
                return 0
            if front[-1] - front[j] == front[j-1]:
                return j
            if j == length-1 and front[length-1] - front[length-2] == 0:
                return length - 1
        return -1
        '''


# class Solution:
#     def pivotIndex(self, nums: List[int]) -> int:
#         total_sum = sum(nums)  # 计算整个数组的总和
#         left_sum = 0  # 初始化左侧和为0

#         for i, num in enumerate(nums):
#             # 如果左侧和等于右侧和（总和减去左侧和再减去当前元素），则当前索引即为轴心索引
#             if left_sum == total_sum - left_sum - num:
#                 return i
#             left_sum += num  # 更新左侧和

#         return -1  # 如果不存在这样的轴心索引，则返回-1


class Solution:
    def pivotIndex(self, nums: list[int]) -> int:
        length, sum_left, sum_right = len(nums), 0, 0
        # 表示下标开始遍历
        if sum(nums) == 0:
            return length - 1
        for i in range(0, length - 1, 1):
            print(sum(nums[0:i:1]), sum(nums[i + 1:length:1]))
            if sum(nums[0:i:1]) == sum(nums[i + 1:length:1]):

                return i
        return -1

def main():
    s = Solution()
    nums = [-1,-1,0,1,1,0]
    print(s.pivotIndex(nums))

if __name__ == '__main__':
    main()



