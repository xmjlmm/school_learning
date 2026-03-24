# 下一个更大的元素
# 可循环列表

class Solution:
    def nextGreaterElements(self, nums: list[int]) -> list[int]:
        length = len(nums)
        flag_count_visit = [-1] * length
        for cur_index in range(0, length, 1):
            next_index = (cur_index + 1) % length
            while next_index != cur_index:
                if nums[next_index] > nums[cur_index]:
                    flag_count_visit[cur_index] = nums[next_index]
                    break
                else:
                    next_index = (next_index + 1) % length

        return flag_count_visit


def main():
    s = Solution()
    print(s.nextGreaterElements([100,1,11,1,120,111,123,1,-1,-100]))

if __name__ == "__main__":
    main()

