'''class Solution:
    def nonSpecialCount(self, l: int, r: int) -> int:
        ans = 0
        for i in range(l, r+1, 1):
            count = 0
            for x in range(1, i, 1):
                if i % x == 0:
                    count += 1
            if count != 2:
                ans = ans + 1
        return ans'''

import math

class Solution:
    def nonSpecialCount(self, l: int, r: int) -> int:
        # 只有完全平方数才会是特殊数字
        min_sqrt = int(math.sqrt(l))
        max_sqrt = int(math.sqrt(r))
        if min_sqrt * min_sqrt != l:
            min_sqrt = min_sqrt + 1
        if min_sqrt > max_sqrt:
            return r - l + 1
        elif min_sqrt == max_sqrt:
            if max_sqrt == 1:
                return r - l + 1
            flag = 0
            # 判断是不是素数，0表示不是素数
            if max_sqrt < 1:
                flag = 0
            for i in range(2, int(math.sqrt(min_sqrt)+1)):
                if min_sqrt % i == 0:
                    flag = 1
                    break
            if flag == 1:
                return r - l + 1
            else:
                return r - l
        else:
            count = 0
            for i in range(min_sqrt, max_sqrt+1):
                if i == 1:
                    continue
                flag = 0
                # 判断是不是素数，0表示不是素数
                for j in range(2, int(math.sqrt(i))+1, 1):
                    if i % j == 0:
                        flag = 1
                        break
                if flag == 0:
                    count = count + 1
            return r - l - count + 1
def main():
    s = Solution()
    l = 4
    r = 16
    print(s.nonSpecialCount(l,r))

main()


