class Solution:
    def isSubstringPresent(self, s: str) -> bool:
        h = [0] * 26
        for i in range(len(s) - 1):
            x = ord(s[i]) - ord('a')
            y = ord(s[i + 1]) - ord('a')
            print(x, y)
            h[x] |= 1 << y
            print(h, h[x])
            print(h[y] >> x & 1)
            if h[y] >> x & 1:
                return True
        return False


def main():
    s = Solution()
    word = 'abc'
    print(s.isSubstringPresent(word))

if __name__ == '__main__':
    main()