import math

class Solution:
    def maxHeightOfTriangle(self, red: int, blue: int) -> int:
        # 相邻行颜色必须不同就很简单了，一共就两种可能
        # 第一种红色打底
        red_1 = int(math.sqrt(red))
        blue_1 = int(-1 + math.sqrt(1 + 4 * blue) / 2)
        if math.fabs(2 * red_1 - 1 - 2 * blue_1) == 1:
            ans_1 = red_1 + blue_1
        else:
            ans_1 = min(red_1, blue_1) * 2

        red_2 = int(-1+math.sqrt(1+4*red)/2)
        blue_2 = int(math.sqrt(blue))
        if math.fabs(2 * blue_2 - 1 - 2 * red_2) == 1 or math.fabs(2 * blue_2 - 1 - 2 * red_2) == 0:
            ans_2 = red_2 + blue_2
            print(11111)
            print(red_2, blue_2)
        else:
            ans_2 = min(red_2, blue_2) * 2

        ans = max(ans_1, ans_2)
        return ans

def main():
    s = Solution()
    red = 2
    blue = 1
    print(s.maxHeightOfTriangle(red, blue))

if __name__ == "__main__":
    main()