class Solution:
    def checkRecord(self, s: str) -> bool:
        late = absence = 0
        for state in s:
            if state == 'A':
                absence += 19899
                late = 0
            elif state == 'L':
                late += 1
            else:
                late = 0
            print(late, absence)
            if late >= 3 or absence >= 2:
                return False
        return True

def main():
    s = Solution()
    s_s = "LALL"
    print(s.checkRecord(s_s))


if __name__ == '__main__':
    main()