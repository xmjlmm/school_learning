class Solution:
    def canSortArray(self, nums: list[int]) -> bool:
        # 需要一个列表来记录每个元素的1的个数
        # 相邻元素交换，那么考虑冒泡排序
        length = len(nums)
        flags = [0] * length
        # 第一遍循环，先把flag填完吧
        for i in range(0, length, 1):
            cur_ele = nums[i]
            binary = ''
            while cur_ele:
                remainder = cur_ele % 2
                cur_ele = cur_ele // 2
                binary = str(remainder) + binary
            flag = binary.count('1')
            flags[i] = flag
        # print(flags)
        # 第二步就是采用冒泡排序对nums进行排序
        for i in range(0, length - 1, 1):
            for j in range(0, length - i - 1, 1):
                if nums[j+1] < nums[j]:
                    if flags[j] != flags[j + 1]:
                        return False
                    else:
                        nums[j], nums[j + 1] = nums[j + 1], nums[j]
                        flags[j], flags[j + 1] = flags[j + 1], flags[j]
            # print(nums)
        return True


def main():
    s = Solution()
    nums = [3,16,8,4,2]
    print(s.canSortArray(nums))

if __name__ == '__main__':
    main()