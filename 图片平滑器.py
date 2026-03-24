class Solution:
    def imageSmoother(self, img: list[list[int]]) -> list[list[int]]:
        m, n = len(img), len(img[0])
        if m == 1 and n == 1:
            return img
        res = [[0] * n for _ in range(m)]
        if m == 1:
            for j in range(n):
                if j == 0:
                    ans = img[0][j] + img[0][j + 1]
                    chu = ans // 2
                elif j == n - 1:
                    ans = img[0][j] + img[0][j - 1]
                    chu = ans // 2
                else:
                    ans = img[0][j] + img[0][j + 1] + img[0][j - 1]
                    chu = ans // 3
                res[0][j] = chu
            return res
        if n == 1:
            for i in range(m):
                if i == 0:
                    ans = img[i][0] + img[i + 1][0]
                    chu = ans // 2
                elif i == m - 1:
                    ans = img[i][0] + img[i - 1][0]
                    chu = ans // 2
                else:
                    ans = img[i][0] + img[i + 1][0] + img[i - 1][0]
                    chu = ans // 3
                res[i][0] = chu
            return res
        for i in range(m):
            for j in range(n):
                ans = img[i][j]
                if i == 0:
                    if j == 0:
                        ans = ans + img[i + 1][j] + img[i][j + 1] + img[i + 1][j + 1]
                        chu = ans // 4
                    elif j == n - 1:
                        ans = ans + img[i][j - 1] + img[i + 1][j - 1] + img[i + 1][j]
                        chu = ans // 4
                    else:
                        ans = ans + img[i][j - 1] + img[i][j + 1] + img[i + 1][j] + img[i + 1][j - 1] + img[i + 1][
                            j + 1]

                        chu = ans // 6
                elif i == m - 1:
                    if j == 0:
                        ans = ans + img[i - 1][j] + img[i][j + 1] + img[i - 1][j + 1]
                        chu = ans // 4
                    elif j == n - 1:
                        ans = ans + img[i][j - 1] + img[i - 1][j - 1] + img[i - 1][j]
                        chu = ans // 4
                    else:
                        ans = ans + img[i][j - 1] + img[i][j + 1] + img[i - 1][j] + img[i - 1][j - 1] + img[i - 1][
                            j + 1]
                        chu = ans // 6
                else:
                    if j == 0:
                        ans = ans + img[i - 1][j] + img[i - 1][j + 1] + img[i][j + 1] + img[i + 1][j] + img[i + 1][
                            j + 1]
                        chu = ans // 6
                    elif j == n - 1:
                        ans = ans + img[i - 1][j - 1] + img[i - 1][j] + img[i + 1][j] + img[i + 1][j - 1] + img[i][
                            j - 1]
                        chu = ans // 6
                    else:
                        ans = ans + img[i - 1][j] + img[i - 1][j + 1] + img[i - 1][j - 1] + img[i][j + 1] + img[i][
                            j - 1] + img[i + 1][j] + img[i + 1][j - 1] + img[i + 1][j + 1]
                        chu = ans // 9
                res[i][j] = chu

        return res


def main():
    s = Solution()
    img = [[100, 200, 100], [200, 50, 200], [100, 200, 100]]
    print(s.imageSmoother(img))
main()