class Solution:
    def removeTrailingZeros(self, num: str) -> str:
        num_int = int(num)
        while num_int % 10 == 0:
            num_int = num_int // 10
            print(num_int)
        return str(num_int)


def main():
    s = Solution()
    print(s.removeTrailingZeros("10500"))

if __name__ == '__main__':
    main()