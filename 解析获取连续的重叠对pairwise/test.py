'''pairwise函数，返回从输入迭代器获取的重叠对的迭代器，是Python3.10新特性，
表示一个迭代器从对象中获取连续的重叠对，在某些场景中可以优化代码运行效率。
pairwise函数是一种用于处理列表中元素之间配对操作的通用方法。
它将一个列表中的元素两两配对，并返回一个包含所有配对的新列表。
通过pairwise函数可以方便地处理多种操作，比如计算成绩差异、相似度计算等。
然而，在处理大型列表时，需要考虑到性能问题，并可能采取一些优化措施。'''



# pairwise 简单来说就是将一个列表相邻两个元素变成一个元组、 找相邻元素的相互关系


from itertools import pairwise
from typing import List

words = pairwise('ABCD')  # AB, BC, CD
for i in words:
    print("".join(i))


# 实例: 判断能否形成等差数列
# 给你一个数字数组 arr, 如果一个数列中，任意相邻两项的差总等于同一个常数，那么这个数列就称为等差数列 。如果可以重新排列数组形成等差数列，
# 请返回true ；否则，返回false 。
# 示例1：
# 输入：arr = [3, 5, 1]
# 输出：true
# 解释：对数组重新排序得到[1, 3, 5]或者[5, 3, 1] ，任意相邻两项的差分别为2或 - 2 ，可以形成等差数列。
# 示例2：
# 输入：arr = [1, 2, 4]
# 输出：false
# 解释：无法通过重新排序得到等差数列。

class Solution:
    def canMakeArithmeticProgression(self, arr: List[int]) -> bool:
        arr.sort()
        tmp = arr[1] - arr[0]
        for i in pairwise(arr):
            if i[1] - i[0] == tmp:
                continue
            else:
                return False
        return True


if __name__ == '__main__':
    s = Solution()
    decision_list = [1, 2, 3]
    r = s.canMakeArithmeticProgression(decision_list)
    print(r)




ls = [1, 2, 4]
l = pairwise(ls)
print(ls)