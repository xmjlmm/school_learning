import math
import itertools
class Solution:
    def f(self, n, length, cuts, visit, permutations_list):
        if n == length:
            permutations_list.append(visit[:])
            return
        for j in range(length):
            if cuts[j] not in visit:
                visit.append(cuts[j])
                self.f(n+1, length, cuts, visit, permutations_list)
                visit.remove(cuts[j])



    def minCost(self, n: int, cuts: list[int]) -> int:
        length = len(cuts)
        min_ans = math.inf
        permutations_list = []
        self.f(0, length, cuts, visit=[], permutations_list=permutations_list)
        for p in permutations_list:
            print(p)
            ans, ls = 0, [0, n]
            # print('1111111111111111111111111111111111111')
            for i in range(0, length):
                cur_ele = p[i]
                print('cur_ele', cur_ele)
                ls.append(cur_ele)
                ls.sort()
                # print(ls)
                j = ls.index(cur_ele)
                # print('j', j)
                ans = ans + (ls[j+1] - ls[j-1])
                print('ans', ans)
                print('ls[j]',ls[j+1], 'ls[j-1]', ls[j-1])
            print(ans)
            if ans < min_ans:
                min_ans = ans
        return min_ans


def main():
    s = Solution()
    n = 7
    lists = [1,3,4,5]
    print(s.minCost(n, lists))

if __name__ == '__main__':
    main()