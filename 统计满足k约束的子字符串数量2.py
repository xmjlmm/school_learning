'''

# 时间复杂度过不去md
class Solution:
    def countKConstraintSubstrings(self, s: str, k: int, queries: list[list[int]]) -> list[int]:
        ans = []
        length = len(queries)
        for i in range(length):
            cur_query = queries[i]
            start = cur_query[0]
            end = cur_query[1]
            res = 0
            for j in range(start, end + 1, 1):
                for m in range(j, end + 1, 1):
                    cur_s = s[j:m+1:1]
                    print(' ', j, ' ', m, ' ', cur_s)
                    if cur_s.count('0') <= k or cur_s.count('1') <= k:
                        res = res + 1
            ans.append(res)
        return ans


def main():
    s = Solution()
    st = "010101"
    k = 1
    queries = [[0,5],[1,4],[2,3]]
    print(s.countKConstraintSubstrings(st, k, queries))
main()


'''






class Solution:
    def countKConstraintSubstrings(self, s: str, k: int, queries: list[list[int]]) -> list[int]:
        n = len(s)
        count = [0, 0]
        prefix = [0] * (n + 1)
        right = [n] * n
        i = 0
        for j in range(n):
            count[int(s[j])] += 1
            while count[0] > k and count[1] > k:
                count[int(s[i])] -= 1
                right[i] = j
                i += 1
            prefix[j + 1] = prefix[j] + j - i + 1

        res = []
        for l, r in queries:
            i = min(right[l], r + 1)
            part1 = (i - l + 1) * (i - l) // 2
            part2 = prefix[r + 1] - prefix[i]
            res.append(part1 + part2)
        return res


def main():
    s = Solution()
    st = "010101"
    k = 1
    queries = [[0,5],[1,4],[2,3]]
    print(s.countKConstraintSubstrings(st, k, queries))
main()