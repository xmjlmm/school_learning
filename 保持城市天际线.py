# class Solution:
#     def maxIncreaseKeepingSkyline(self, grid: list[list[int]]) -> int:
#         # 简单分析一下，元素变化的就是这个元素所在每一行的最大值与每一列的最大值的最小值
#         # 如果当前值为某一行或者某一列的最值，则不进行操作
#         n, ans = len(grid[0]), 0
#         max_row_line = [0] * n
#         max_col_line = [0] * n
#         # 不用双循环，先找行的最值
#         for i in range(n):
#             max_row = max(grid[i])
#             max_row_line[i] = max_row
#         # 然后找列的最值
#         for i in range(n):
#             max_col = 0
#             for j in range(n):
#                 max_col = max(max_col, grid[j][i])
#             max_col_line[i] = max_col
#         print(max_col_line)
#         print(max_row_line)
#         # 第i行第j列的元素，如果比所在行的最值与所在列的最值都小，则可以增加
#         for i in range(0, n, 1):
#             for j in range(0, n, 1):
#                 if grid[i][j] == max_col_line[j] or grid[i][j] == max_row_line[i]:
#                     continue
#                 else:
#                     max_inc = min(max_col_line[j], max_row_line[i])
#                     ans = ans + max_inc - grid[i][j]
#         return ans
#
#
# def main():
#     s = Solution()
#     grid = [[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]]
#     print(s.maxIncreaseKeepingSkyline(grid))
#
# if __name__ == '__main__':
#     main()

class Solution:
    def maxIncreaseKeepingSkyline(self, grid: list[list[int]]) -> int:
        rowMax = list(map(max, grid))
        colMax = list(map(max, zip(*grid)))
        return sum(min(rowMax[i], colMax[j]) - h for i, row in enumerate(grid) for j, h in enumerate(row))

def main():
    s = Solution()
    grid = [[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]]
    print(s.maxIncreaseKeepingSkyline(grid))

if __name__ == '__main__':
    main()