# class Solution:
#     def findMaximumNumber(self, k: int, x: int) -> int:
#         total_price = 0
#         for i in range(1, 100000000000, 1):
#             cur_bin = bin(i).split('b')[1]
#             cur_len = len(cur_bin)
#             flag = 0
#             print(cur_bin, end = " ")
#             if cur_len >= 3 * x:
#                 cur_price = int(cur_bin[x-1]) + int(cur_bin[2*x-1]) + int(cur_bin[3*x-1])
#                 flag = 1
#                 # print(3, end = " ")
#             elif cur_len >= 2 * x and flag == 0:
#                 cur_price = int(cur_bin[x-1]) + int(cur_bin[2*x-1])
#                 flag = 1
#                 # print(2, end = " ")
#             elif cur_len >= x and flag == 0:
#                 cur_price = int(cur_bin[x-1])
#                 print(x, end = " ")
#                 print(int(cur_bin[1]), end = " ")
#                 print(1, end = " ")
#             else:
#                 cur_price = 0
#                 # print(0, end = " ")
#             # print(cur_price)
#             total_price += cur_price
#             print(total_price)
#             if total_price > k:
#                 return i - 1
#
#
#
#
# def main():
#     k, x = 7, 2
#     s = Solution()
#     print(s.findMaximumNumber(k, x))
#
# if __name__ == "__main__":
#     main()
#




class Solution:
    def findMaximumNumber(self, k: int, x: int) -> int:
        total_price = 0
        for i in range(1, 100000000000, 1):
            cur_bin = bin(i).split('b')[1]
            cur_len = len(cur_bin)

            if cur_len <= 3 * x:

                cur_bin = '0' * (3 * x - cur_len) + cur_bin
                cur_bin = cur_bin[::-1]
                cur_price = int(cur_bin[x-1]) + int(cur_bin[2*x-1]) + int(cur_bin[3*x-1])

            else:
                plu_len = cur_len - 3 * x
                print(cur_bin, end = "     ")
                cur_bin = cur_bin[plu_len:cur_len:1][::-1]
                print(cur_bin, end = " ")
                cur_price = int(cur_bin[x-1]) + int(cur_bin[2*x-1]) + int(cur_bin[3*x-1])
                print(cur_price)
            total_price += cur_price
            print(i, total_price)
            if total_price > k:
                return i - 1


def main():
    k, x = 83, 1
    s = Solution()
    print(s.findMaximumNumber(k, x))

if __name__ == "__main__":
    main()





class Solution:
    def findMaximumNumber(self, k: int, x: int) -> int:
        l, r = 1, (k + 1) << x
        while l < r:
            m = (l + r + 1) // 2
            if self.accumulatedPrice(x, m) > k:
                r = m - 1
            else:
                l = m
        return l

    def accumulatedPrice(self, x: int, num: int) -> int:
        res = 0
        length = len(bin(num)) - 2
        for i in range(x, length + 1, x):
            res += self.accumulatedBitPrice(i, num)
        return res

    def accumulatedBitPrice(self, x: int, num: int) -> int:
        period = 1 << x
        res = (period // 2) * (num // period)
        if num % period >= (period // 2):
            res += num % period - ((period // 2) - 1)
        return res

def main():
    k, x = 83, 1
    s = Solution()
    print(s.findMaximumNumber(k, x))

if __name__ == "__main__":
    main()







