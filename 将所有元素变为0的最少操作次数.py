class Solution:
    def minOperations(self, nums: list[int]) -> int:
        # 一定可以按照从最小到大的顺序开始清零
        sequeue = nums
        length_nums = len(nums)
        for i in range(length_nums - 1):
            for j in range(0, i):
                if (sequeue[j] > sequeue[j+1]):
                    sequeue[j], sequeue[j+1] = sequeue[j+1], sequeue[j]
        sequeue_set = []
        for i in range(length_nums - 1):
            if sequeue[i] not in sequeue_set:
                sequeue_set.append(sequeue[i])
        print(sequeue_set)
        length_sequeue = len(sequeue_set)
        ans = 0
        for i in range(0, length_sequeue):
            curr_num = sequeue_set[i]
            for j in range(length_nums):
                if (nums[j] == 0):
                    ans = ans + 1
                elif (nums[j] == curr_num):
                    nums[j] = 0
                else:
                    continue
            

        return ans   

def main():
    s = Solution()
    nums = [1,2,1,2,1,2]
    print(s.minOperations(nums))

if __name__ == "__main__":
    main()