class Solution:
    def sortSentence(self, s: str) -> str:
        s = s.split(' ')
        n, ans = len(s), ''
        # print(s)
        for i in range(0, n-1):
            for j in range(0, n-i-1):
                # print(s[j])
                if int(s[j][-1]) > int(s[j+1][-1]):
                    s[j], s[j+1] = s[j+1], s[j]
        for i in range(n):
            s[i] = s[i][:-1:1]
            ans = ans + s[i] + ' '
        ans = ans[:-1:1]
        return ans


def main():
    s = Solution()
    words = "is2 sentence4 This1 a3"
    print(s.sortSentence(words))

if __name__ == "__main__":
    main()