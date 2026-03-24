class Solution:
    def minChanges(self, n: int, k: int) -> int:
        bin_n = (bin(n)[::-1])[:-2:]
        bin_k = (bin(k)[::-1])[:-2:]
        count = 0
        length_k, length_n = len(bin_k), len(bin_n)
        for i in range(length_k):
            if bin_n[i] == '0' and bin_k[i] == '1':
                return -1
            if bin_n[i] == '1' and bin_k[i] == '0':
                count = count + 1
        print(length_k, length_n)
        print(bin_n[length_k:length_n:1])
        count = count + bin_n[length_k:length_n:1].count('1')
        return count

def main():
    n = 13
    k = 4
    s = Solution()
    print(s.minChanges(n, k))

if __name__ == "__main__":
    main()