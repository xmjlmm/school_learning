class Solution:
    def temperatureTrend(self, temperatureA: list[int], temperatureB: list[int]) -> int:
        trendA, trendB = temperatureA[:], temperatureB[:]
        length = len(temperatureA)
        for i in range(1,length, 1):
            # 上升
            if temperatureA[i] > temperatureA[i-1]:
                trendA[i] = 1
            # 平稳
            if temperatureA[i] == temperatureA[i-1]:
                trendA[i] = 0
            # 下降
            if temperatureA[i] < temperatureA[i-1]:
                trendA[i] = -1

            # 上升
            if temperatureB[i] > temperatureB[i-1]:
                trendB[i] = 1
            # 平稳
            if temperatureB[i] == temperatureB[i-1]:
                trendB[i] = 0
            # 下降
            if temperatureB[i] < temperatureB[i-1]:
                trendB[i] = -1


        ans = 0
        equal_trend = []
        for i in range(1, length, 1):
            if trendA[i] == trendB[i]:
                ans = ans + 1
            else:
                equal_trend.append(ans)
                ans = 0
        equal_trend.append(ans)
        return max(equal_trend)


def main():
    solution = Solution()
    temperatureA = [1,-15,3,14,-1,4,35,36]
    temperatureB = [-15,32,20,9,33,4,-1,-5]
    print(solution.temperatureTrend(temperatureA, temperatureB))

if __name__ == '__main__':
    main()