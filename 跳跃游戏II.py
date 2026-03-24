class Solution:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0
        # count表示需要跳转的次数，初始化位置，以及初始化可跳转大小
        count, pos, end = 0, 0, 0
        # 记录当前能跳到的最远位置
        max_pos = 0
        while end < n - 1:
            # 遍历从当前位置到当前能跳到的最远位置
            for i in range(pos, end + 1):
                # 更新能跳到的最远位置
                max_pos = max(max_pos, i + nums[i])
            # 更新当前位置为之前记录的最远位置
            pos = end + 1
            # 更新当前能跳到的最远位置
            end = max_pos
            # 跳跃次数加1
            count += 1
        return count
    
def main():
    s = Solution()
    nums = [2,3,1,1,4]
    print(s.jump(nums))

if __name__ == '__main__':
    main()