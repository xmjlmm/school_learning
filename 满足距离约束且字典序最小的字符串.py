class Solution:
    def getSmallestString(self, s: str, k: int) -> str:
        if k == 0:
            print(12345678)
            return s
        ans, n = '', len(s)
        while k != 0:
            for i in range(n):
                cur_ele = s[i]
                cur_dict_num = ord(cur_ele) - 97
                if cur_dict_num - k <= 0 or cur_dict_num + k >= 26:
                    ans = ans + 'a'
                    k = k - min(cur_dict_num - 0, 26 - cur_dict_num)
                    print(k)
                else:
                    cur_ele = chr(ord(cur_ele) - k)
                    ans = ans + cur_ele
            if i != n:
                ans = ans + s[i + 1::1]

            if ans == 'a' * n:
                return 'a' * n
        return ans


def main():
    s = Solution()
    str1 = "lol"
    k = 0
    print(s.getSmallestString(str1, k))

if __name__ == '__main__':
    main()