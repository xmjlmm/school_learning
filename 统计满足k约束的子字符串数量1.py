class Solution:
    def countKConstraintSubstrings(self, s: str, k: int) -> int:
        count = 0
        length = len(s)
        # 直接用起点和终点
        for i in range(0, length, 1):
            for j in range(i+1, length+1, 1):
                sub_s = s[i:j]
                print(sub_s)
                if sub_s.count('1') <= k or sub_s.count('0') <= k:
                    count = count + 1
        return count


def main():
    s = Solution()
    st = "11111"
    k = 1
    print(s.countKConstraintSubstrings(st, k))
main()




# n, m, k = map(int, input().split(' '))
# print(type(n))
# print(n, m, k)

# c = input().split(' ')
# print(c)
# for i in range(len(c)):
#     # cur_ele = c[i]
#     # cur_ele = int(cur_ele)
#     # print('c[i]', type(c[i]), 'cur_ele:', type(cur_ele))
#     c[i] = int(c[i])
#     print('c[i]', type(c[i]))
# c.sort()
# k = 3
# c_k = c[0:k:1]
#
# print(c)
#
# print(c_k)


# n=20241111
# print(int(bin(n)[2:]))
# x = ''
# while n:
#   y=n%2
#   n=n//2
#
#   # print(y)
#   x=str(y)+x
#   # print('n:', n)
# # print(x)
# print(int(x))
#
