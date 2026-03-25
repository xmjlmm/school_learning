# t = int(input(''))
# for i in range(t):
#     str1 = input('')
#     a, b, c = str1.split(' ')
#     b = int(b)
#     # a表示打印形状， b表示个数， c表示符号
#     if(a=='T'):
#         lieshu = int((b+1)/2)
#         for i in range(lieshu):
#             print(' ' * (lieshu-1-i), end = "")
#             print(c*(2*i+1))
#     else:
#         lieshu = int((b+1)/2)
#         for i in range(lieshu):
#             print(' ' * (lieshu-1-i), end = "")
#             print(c*(2*i+1))
#         for i in range(lieshu-1):
#             print(' ' * (i+1), end = "")
#             print(c*(2*(lieshu-i-1)-1))


# n = int(input(''))
# str1 = input('')
# str1.split(' ')
# for i in range(n):
# 	str1[i] = int(str1[1])
# str2 = input('')
# list2 = list(map(int, str2.split(' ')))
# str3 = input('')
# list3 = list(map(int, str3.split(' ')))
# str4 = input('')
# list4 = list(map(int, str4.split(' ')))
# # list1表示定价，list2表示成本，list3表示制作多少份，list4表示卖出多少份
# max = list1[0] * list4[0] - list2[0] * list3[0]
# max_index = 1
# for i in range(1, n):
#     profit = list1[i] * list4[i] - list2[i] * list3[i]
#     if (profit > max):
#         max = profit
#         max_index = i + 1
# print(max_index)
# print(max)



# t = int(input())
# for i in range(t):
#     hash = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
#     count = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#     xiabiao = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
#     list_train = list(map(int, input().split(' ')))
#     list_test = list(map(int, input().split(' ')))
#     len_train = len(list_train)
#     for j in range(len_train):
#         yu = list_train[j] % 11
#         # print(list_train[j])
#         # print(yu)
#         if (hash[yu] == -1):
#             # print(list_train[j])
#             hash[yu] = list_train[j]
#
#             xiabiao[j] = yu
#         else:
#             for k in range(1, 5):
#                 pos = yu + k * k
#                 count[j] = count[j] + 1
#                 if(pos > 11):
#                     pos = pos - 11
#                 if(pos < 0):
#                     pos = pos + 11
#                 if (hash[pos] == -1):
#                     hash[pos] = list_train[j]
#                     xiabiao[j] = pos
#                     # print(list_train[j], pos)
#                     break
#                 count[j] = count[j] + 1
#                 pos = yu - k * k
#                 if(pos > 11):
#                     pos = pos - 11
#                 if(pos < 0):
#                     pos = pos + 11
#                 if (hash[pos] == -1):
#                     hash[pos] = list_train[j]
#                     xiabiao[j] = pos
#                     break
#         # for i in range(len_train):
#         #     print(list_train[j],  xiabiao[j])
#
#
#     print("HashTable=", end="")
#     for j in range(11):
#         print(hash[j], end=" ")
#     print('')
#     len_test = len(list_test)
#     for j in range(len_test):
#         for k in range(len_train):
#             if (list_test[j] == list_train[k]):
#                 print("{} at pos {}|compared {} times".format(list_train[k], xiabiao[k], count[k]))


n = int(input(''))
str1 = input('')
list1 = list(map(int, str1.split(' ')))
str2 = input('')
list2 = list(map(int, str2.split(' ')))
str3 = input('')
list3 = list(map(int, str3.split(' ')))
str4 = input('')
list4 = list(map(int, str4.split(' ')))
# list1表示定价，list2表示成本，list3表示制作多少份，list4表示卖出多少份
max = list1[0] * list4[0] - list2[0] * list3[0]
max_index = 1
for i in range(0, n):
    profit = list1[i] * list4[i] - list2[i] * list3[i]
    if (profit > max):
        max = profit
        max_index = i + 1
print(max_index)
print(max)
