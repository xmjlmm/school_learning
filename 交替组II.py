# # class Solution:
# #     def numberOfAlternatingGroups(self, colors: list[int], k: int) -> int:
# #         length = len(colors)
# #         # 如果是3就需要添加2个下标为0和1
# #         for i in range(k - 1):
# #             colors.append(i)
# #         print(colors)
# #         ans = 0
# #         for i in range(length):
# #             cur_ele, flag = colors[i], 0
# #             for j in range(i + 1, i + k):
# #                 if colors[j] != cur_ele:
# #                     cur_ele = colors[j]
# #                 else:
# #                     flag = 1
# #                     break
# #             if flag == 0:
# #                 ans = ans + 1
# #         return ans
#
#
# class Solution:
#     def numberOfAlternatingGroups(self, colors: list[int], k: int) -> int:
#         # 如果是3就需要添加2个下标为0和1
#         for i in range(k-1):
#             colors.append(colors[i])
#         length = len(colors)
#         ans = 0
#         cur_ele = colors[0]
#         count = 1
#         for i in range(1, length):
#             if colors[i] != cur_ele:
#                 count = count + 1
#             else:
#                 print(count)
#                 if count >= k:
#                     ans = ans + count - k + 1
#                 count = 1
#             cur_ele = colors[i]
#         return ans
#
#
#
# def main():
#     s = Solution()
#     ls = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
#     k = 31623
#     print(s.numberOfAlternatingGroups(ls, k))
#
# main()



a = 'dfhaldha'
a = list(a)
print(a)
print(a[0])
tmp = a.pop(1)

print(tmp)
