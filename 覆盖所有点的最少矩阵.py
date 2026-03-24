class Solution:
    def minRectanglesToCoverPoints(self, points: list[list[int]], w: int) -> int:
        ans = 0
        first = points[0][0]
        first_min = first + w
        ans = ans + 1
        points = points[1::1]
        for cur_point in points:
            cur_x = cur_point[0]
        if cur_x > first_min:
            ans = ans + 1
            first_min = cur_x + w

        return ans


def main():
    s = Solution()
    points = [[2,1],[1,0],[1,4],[1,8],[3,5],[4,6]]
    w = 1
    print(s.minRectanglesToCoverPoints(points, w))

if __name__ == '__main__':
    main()