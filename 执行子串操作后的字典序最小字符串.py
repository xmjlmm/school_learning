class Solution:
    def smallestString(self, s: str) -> str:
        # 这样吧,用两个矩阵
        list_a, list_na, length = [], [], len(s)
        for i in range(length):
            if s[i] == 'a':
                list_a.append(i)
            else:
                list_na.append(i)
        print(list_a, list_na)

        if len(list_na) == 0:
            ans = s[0:-1:1] + chr(ord(s[-1]) + 25)
            return ans

        begin = list_na[0]

        if begin == 0:
            ans = ''
        else:
            ans = s[:begin:1]
        flag = 0
        for c in list_a:
            if c > begin:
                stop = c
                flag = 1
                break
        if flag == 0:
            stop = length
        for i in range(begin, stop, 1):
            ans_s = chr(ord(s[i])-1)
            ans += ans_s

        ans = ans + s[stop:]

        return ans

def main():
    s = Solution()
    st = "aa"
    print(s.smallestString(st))

if __name__ == "__main__":
    main()