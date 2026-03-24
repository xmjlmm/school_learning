# # 时间复杂度超了，我想到改进了，等一下
# class Solution:
#     def minimumLevels(self, possible: list[int]) -> int:
#         # 保证至少A有一个元素，B有一个元素
#         length = len(possible)
#         if length < 2:
#             return -1
#         # A最大是0:length:1
#         max_index = length - 1
#         # 保证A至少一个元素
#         for mid_index in range(0, max_index, 1):
#             sum_Alice, sum_Bob = 0, 0
#             for i in range(0, mid_index+1, 1):
#                 if possible[i] == 0:
#                     sum_Alice = sum_Alice - 1
#                 else:
#                     sum_Alice = sum_Alice + 1
#             for j in range(mid_index+1, max_index+1, 1):
#                 if possible[j] == 0:
#                     sum_Bob = sum_Bob - 1
#                 else:
#                     sum_Bob = sum_Bob + 1
#             print('mid_index', mid_index, 'sum_Alice', sum_Alice, 'sum_Bob', sum_Bob)
#             if sum_Alice > sum_Bob:
#                 return mid_index+1
#         return -1
#
# def main():
#     s = Solution()
#     nums = [1,1,1,1,1]
#     print(s.minimumLevels(nums))
#
# if __name__ == "__main__":
#     main()




# 时间复杂度超了，我想到改进了，等一下
class Solution:
    def minimumLevels(self, possible: list[int]) -> int:
        length = len(possible)
        if length < 2:
            return -1

        sum_Alice, sum_Bob = 1 if possible[0] == 1 else -1, 0

        for i in range(1, length, 1):
            if possible[i] == 1:
                sum_Bob = sum_Bob + 1
            else:
                sum_Bob = sum_Bob - 1

        if sum_Alice > sum_Bob:
            return 1
        print('sum_Alice', sum_Alice, 'sum_Bob', sum_Bob)
        for mid_index in range(1, length-1, 1):
            if sum_Alice > sum_Bob:
                return mid_index
            if possible[mid_index] == 1:
                sum_Alice = sum_Alice + 1
                sum_Bob = sum_Bob - 1
            else:
                sum_Alice = sum_Alice - 1
                sum_Bob = sum_Bob + 1
        if sum_Alice > sum_Bob:
            return mid_index+1
        return -1



def main():
    s = Solution()
    nums = [0,1,0]
    print(s.minimumLevels(nums))

if __name__ == "__main__":
    main()