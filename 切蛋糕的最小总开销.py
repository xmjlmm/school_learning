from typing import List  # 导入List用于类型提示

class Solution:
    def minimumCost(self, m: int, n: int, horizontalCut: List[int], verticalCut: List[int]) -> int:
        if m == 1:
            return sum(verticalCut)
        if n == 1:
            return sum(horizontalCut)
        verticalCut.sort(reverse=True)
        horizontalCut.sort(reverse=True)
        v_i, h_i, ans = 0, 0, 0
        while v_i < n - 1 and h_i < m - 1:
            if horizontalCut[h_i] >= verticalCut[v_i]:
                ans = ans + horizontalCut[h_i] * (v_i + 1)
                print(horizontalCut[h_i])
                h_i = h_i + 1
            else:
                ans = ans + verticalCut[v_i] * (h_i + 1)
                v_i = v_i + 1
        if v_i == n - 2:
            ans = ans + sum(verticalCut[v_i:]) * (h_i + 1)
        else:
            ans = ans + sum(horizontalCut[h_i:]) * (v_i + 1)
        return ans

def main():
    m = 5
    n = 8
    horizontalCut = [3,6,4,5]
    verticalCut = [1,1,2,2,3,4,5]
    solution = Solution()
    print(solution.minimumCost(m, n, horizontalCut, verticalCut))


if __name__ == '__main__':
    main()