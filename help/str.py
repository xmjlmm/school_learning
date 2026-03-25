# # # # # a = input()
# # # # #
# # # # #
# # # # # b=''
# # # # # for i in a:
# # # # #     if i=='a' or i=='b':
# # # # #         continue
# # # # #     else:
# # # # #         b+=i
# # # # #
# # # # # print(b)
# # # #
# # # #
# # # # a = input()
# # # # # 判断
# # # #
# # # # length=len(a)
# # # #
# # # # # 表示已经遍历过的点
# # # # b = ''
# # # # flag = 0
# # # # for i in range(length):
# # # #
# # # #
# # # #   if a[i] in b:
# # # #     flag = 1
# # # #
# # # #   b = b + a[i]
# # # # # if flag  == 0:
# # # # #   print('YES')
# # # # # else:
# # # # #   print('NO')
# # # #
# # # # print(b)
# # #
# # # # a = 'fhafa'
# # # # print(set(a))
# # #
# # # # a = 31
# # # # # a = 'ada'
# # # # # length = len(a)
# # # # # for i in a:
# # # # # for i in range(0,length,1)
# # # # # 默认flag = 0，表示素数
# # # # flag=0
# # # # if a<=1:
# # # #     print('error')
# # # # for i in range(2,a-1):
# # # #     # 找到一个数能被整除，说明不是素数
# # # #     if a%i==0:
# # # #         flag=1
# # # # if flag==0:
# # # #     print('is')
# # # # else:
# # # #     print('no')
# # #
# # #
# # #
# # # '''如果一个数 p 是个质数，同时又是整数 a 的约数，则 p 称为 a 的一个质因数。
# # #
# # # 请问 2024 有多少个质因数。'''
# # #
# # # #
# # # # def Isprime(i):
# # # #     if i<=1:
# # # #         return False
# # # #     for j in range(2,i-1):
# # # #       if  i%j==0:
# # # #           return False
# # # #     return True
# # # #
# # # #
# # # #
# # # # a = 2024
# # # # count = 0
# # # #
# # # # # 2024所有的因数
# # # # for i in range(1,a):
# # # #     if a%i==0 and Isprime(i):
# # # #         count+=1
# # # #
# # # # print(count)
# # #
# # #
# # #
# # # '''对于一个整数 n ，我们定义一次开根变换会将 n 变为开根号后的整数部分。
# # # 即变为平方和不超过 n 的数中的最大数。
# # #
# # # 例如，20 经过开根变换将变为 4 ，
# # # 如果再经过一次开根变换将变为 2 ，
# # # 如果再经过一次开根变换将变为 1 。
# # #
# # # 请问，2024经过多少次开根变换后会变为 1 ？'''
# # # # import math
# # # # count = 0
# # # # a = 2024
# # # # while a != 1:
# # # #     a = int(math.sqrt(a))
# # # #     count = count + 1
# # # #
# # # #
# # # # print(count)
# # #
# # #
# # # '''
# # # 小蓝有很多 1x1x1 的小立方体，他可以使用多个立方体拼成更大的立方体。
# # #
# # # 例如，小蓝可以使用 8 个小立方体拼成一个大立方体，每边都是 2 个。
# # #
# # # 又如，小蓝可以使用 27 个小立方体拼成一个大立方体，每边都是 3 个。
# # #
# # # 现在，小蓝有 2024 个小立方体，他想再购买一些小立方体，
# # # 用于拼一个超大的立方体，要求所有的小立方体都用上，拼成的大立方体每边长度都相等。
# # #
# # # 请问，小蓝最少需要购买多少个小立方体？
# # #
# # # '''
# # #
# # # for i in range(1,111001010101010):
# # #     a = i ** 3
# # #     if a > 2024:
# # #         ans = a - 2024
# # #         break
# # #
# # # print(ans)
# # #
# # # '''
# # #
# # # 如果一个日期的日期以 1 结尾（1日、11日、21日、31日）且为星期一，
# # # 则称这个日期为一好日期。
# # # 请问从 1901 年 1 月 1 日至 2024 年 12 月 31 日总共有多少个一好日期。
# # # 提示：1901 年 1 月 1 日是星期二。
# # #
# # # '''
# # #
# # # year_char = 2024 - 1901 + 1
# # # count = 0
# # # for i in range(1901, 2025, 1):
# # #     if i % 4 == 0 and i % 100 != 0 or i % 400 == 0:
# # #         count = count + 1
# # #
# # # day_count = count * 366 + (year_char - count) * 365
# # #
# # # print((day_count-6)//7)
# # #
# # #
# # #
# # import os
# # import sys
# #
# # # 请在此输入您的代码
# #
# # t = int(input(' '))
# # for _ in range(t):
# #   n = int(input(' '))
# #   if n < 3:
# #     print(-1)
# #
# #   elif n == 3:
# #     print(1)
# #   elif n == 4:
# #     print(-1)
# #
# #   elif n == 5:
# #     print(1)
# #   elif n % 5==0:
# #     print(n//5)
# #   else:
# #     # 22
# #     x = n // 5
# #     flag = 0
# #     for j in range(0, x+1, 1):
# #       c = n - j * 5
# #       yu = c % 3
# #       print('c',c,'yu',yu,'dd',c//3)
# #       if yu == 0:
# #         ans = j + c // 3
# #         flag = 1
# #     if flag == 1:
# #       print(ans)
# #     else:
# #       print(-1)
#
#
#
# import os
# import sys
#
# # 请在此输入您的代码
#
#
# #输入
# n=5
# ls = []
# for _ in range(n):
#   lis = input(' ').split(' ')
#   ls.append(lis)
#
#
# def mem(m):
#   count = 0
#   count_max = 0
#   for i in range(n):
#     ls_x = ls[i]
#     if str(m) in ls_x:
#       count = count + 1
#     else:
#       count_max = max(count_max, count)
#       count = 0
#   return count_max
# def main():
#   print(mem(1), ' ', mem(2), ' ', mem(3), ' ', mem(4), ' ', mem(5))
# main()
#
#
#
#
#


import os
import sys

# 请在此输入您的代码


n = int(input(''))
a = input('').split(' ')

for i in range(n):
  a[i] = int(a[i])
print(a)
a.sort()
a = a[::-1]
count = 0
while True:
  if a[0] == a[-1]:
      break
  for j in range(1, n):
    a[j] = a[j] + 1
  print(a)
  count = count + 1

  a.sort()
  a = a[::-1]

print(count)
