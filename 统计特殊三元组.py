class Solution:
    def specialTriplets(self, nums: list[int]) -> int:
        mod = 10**9+7
        num_cnt, num_partial_cnt = {}, {}

        for i in nums:
            if i not in num_cnt:
                num_cnt[i] = 1
            else:
                num_cnt[i] = num_cnt[i] + 1
        print(num_cnt)
        ans = 0

        for i in nums:
            target = i * 2
            
        

        return ans
    
def main():
    s = Solution()
    nums = [0,1,0,0]
    print(s.specialTriplets(nums))

if __name__ == "__main__":
    main()