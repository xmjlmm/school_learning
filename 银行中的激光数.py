class Solution:
    def numberOfBeams(self, bank: list[str]) -> int:
        # m表示有多少行, n表示有多少列
        m, n = len(bank), len(bank[0])
        count_ji = [0] * m
        for i in range(m):
            count = 0
            for j in range(n):
                if (bank[i][j]=='1'):
                    count = count + 1
            count_ji[i] = count
        ans = 0
        # print(count_ji)
        # 去除0
        count_ji_uneq = [0] * m
        j = 0
        for i in range(m):
            if (count_ji[i] != 0):
                count_ji_uneq[j] = count_ji[i]
                j = j + 1
        for i in range(m-1):
            ans = ans + count_ji_uneq[i] * count_ji_uneq[i+1]
        # print(count_ji_uneq)
        return ans 
                    

def main():
    s = Solution()
    bank = ["011001","000000","010100","001000"]
    print(s.numberOfBeams(bank))
main()
