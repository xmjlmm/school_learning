class Solution:
    def smallestNumber(self, n: int) -> int:
        count = 0

        while (n):
            count = count + 1
            n = n // 2
        
        print(count)

        ans = 0
        for i in range(count):
            ans = ans + 2 ** (i)
        
        return ans
    

def main():
    s = Solution()
    n = 3
    res = s.smallestNumber(n)
    print(res)

main()