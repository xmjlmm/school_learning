class Solution:
    def countAlternatingSubarrays(self, nums: list[int]) -> int:
        # 我觉得找连续的会更容易一点，然后数组的子集的个数应该也好算
        # n + n-1 + n-2 + ... + 1 + 0
        length, adj, flag = len(nums), [], 1
        sum_continue= length

        # sum_child = (length + 0) * (length + 1) // 2
        for i in range(1, length, 1):
            if nums[i] != nums[i-1]:
                flag = flag + 1
            else:
                adj.append(flag)
                flag = 1
        adj.append(flag)
        for i in adj:
            if i > 1:
                sum_continue = i * (i - 1) // 2 + sum_continue

        return sum_continue


def main():
    s = Solution()
    nums = [0,1,1,1]
    print(s.countAlternatingSubarrays(nums))

if __name__ == '__main__':
    main()