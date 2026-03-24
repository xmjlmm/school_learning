# class Solution:
#     def minEnd(self, n: int, x: int) -> int:
#         if n == 1:
#             return x
#         init_ele, n = x, n-1
#         init_ele = bin(init_ele).split('b')[1]
#         count_zero = init_ele.count('0')
#         able = 2 ** count_zero - 1
#
#
#         while n:
#             if able < n:
#                 n = n - 1
#                 init_ele = '1' + init_ele
#                 ans = init_ele
#             else:
#                 lel_n = bin(n).split('b')[1]
#                 lel_n = (count_zero - len(lel_n)) * '0' + lel_n
#                 ans, flag, n = '', 0, 0
#                 for i in init_ele:
#                     if i == '1':
#                         ans = ans + i
#                     else:
#                         ans = ans + lel_n[flag]
#                         flag = flag + 1
#         # return int(ans, 2)
#         # return ans
#
#
# def main():
#     s = Solution()
#     n, x = 3, 1
#     print(s.minEnd(n, x))
#
# if __name__ == '__main__':
#     main()








# class Solution:
#     def minEnd(self, n: int, x: int) -> int:
#         if n == 1:
#             return x
#         init_ele, n = x, n-1
#         init_ele = bin(init_ele).split('b')[1][::-1]
#         bin_n = bin(n).split('b')[1][::-1]
#         ans, flag, length_bin_n, ele_flag = '', 0, len(bin_n), 0
#         for i in init_ele:
#             if flag == length_bin_n:
#                 break
#             ele_flag += 1
#             if i == '1':
#                 ans = ans + i
#             else:
#                 ans = ans + bin_n[flag]
#                 flag += 1
#         if flag != length_bin_n:
#             ans = ans + bin_n[flag:]
#         if ele_flag != len(init_ele):
#             ans = ans + init_ele[ele_flag:]
#         ans = ans[::-1]
#         return int(ans, 2)
#
#
#
# def main():
#     s = Solution()
#     n, x = 2, 4
#     print(s.minEnd(n, x))
#
# if __name__ == '__main__':
#     main()
#



class Solution:
    def minEnd(self, n: int, x: int) -> int:
        bitCount = n.bit_length() + x.bit_count()
        res, j = x, 0
        m = n - 1
        for i in range(bitCount):
            if ((res >> i) & 1) == 0:
                if ((m >> j) & 1) != 0:
                    res |= (1 << i)
                j += 1
        return res

def main():
    s = Solution()
    n, x = 2, 4
    print(s.minEnd(n, x))

if __name__ == '__main__':
    main()