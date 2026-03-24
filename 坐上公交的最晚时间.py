class Solution:
    def latestTimeCatchTheBus(self, buses: list[int], passengers: list[int], capacity: int) -> int:
        buses.sort()
        passengers.sort()
        i, j = 0, 0
        n, m = len(buses), len(passengers)

        while i < n:
            cur_car = buses[i]
            count = 0

            while count < capacity and j < m and passengers[j] <= cur_car:
                count += 1
                j += 1

            i += 1

        # 处理最后一班车的情况
        if j > 0 and (i == 0 or buses[i - 1] != buses[i - 1]):
            ans = min(buses[i - 1], passengers[j - 1] - 1)
        else:
            ans = buses[i - 1]

        return ans


def main():
    s = Solution()
    buses = [10, 20]
    passengers = [2, 17, 18, 19]
    capacity = 2
    print(s.latestTimeCatchTheBus(buses, passengers, capacity))


if __name__ == "__main__":
    main()
