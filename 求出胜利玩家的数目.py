class Solution:
    def winningPlayerCount(self, n: int, pick: list[list[int]]) -> int:
        pick.sort(key=lambda x: (x[1], x[0]))
        cur_play, cur_color, count = pick[0][0], pick[0][1], 0
        ls = []
        max_count = 0
        for dd in pick:
            play = dd[0]
            color = dd[1]
            if play == cur_play:
                if color == cur_color:
                    count = count + 1
                else:
                    max_count = max(max_count, count)
                    count = 1
                    cur_color = color
                if max_count >= play + 1:
                    ls.append(play)
            else:
                cur_play = play
                max_count = 0
                count = 0
                if color == cur_color:
                    count = count + 1
                else:
                    max_count = max(max_count, count)
                    count = 1
                    cur_color = color
                if max_count >= play + 1:
                    ls.append(play)

        ls = set(ls)
        return len(ls)
def main():
    s = Solution()
    n = 4
    pick = [[0,0],[1,0],[1,0],[2,1],[2,1],[2,0]]
    print(s.winningPlayerCount(n, pick))
main()