class Solution:
    def numRookCaptures(self, board: list[list[str]]) -> int:
        m, n = len(board), len(board[0])
        ans = 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'R':
                    tmp_i, tmp_j = i, j
                    break
        for i in range(tmp_i, -1, -1):
            print(board[i][tmp_j])
            if board[i][tmp_j] == 'B':
                break
            elif board[i][tmp_j] == 'p':
                ans = ans + 1
                break
                print(ans)
            else:
                continue
        for i in range(tmp_i, m, 1):
            if board[i][tmp_j] == 'B':
                break
            elif board[i][tmp_j] == 'p':
                ans = ans + 1
                break
            else:
                continue
        for j in range(tmp_j, -1, -1):
            if board[tmp_i][j] == 'B':
                break
            elif board[tmp_i][j] == 'p':
                ans = ans + 1
                break
            else:
                continue
        for j in range(tmp_j, n, 1):
            if board[tmp_i][j] == 'B':
                break
            elif board[tmp_i][j] == 'p':
                ans = ans + 1
                break
            else:
                continue
        return ans



def main():
    s = Solution()
    board = [[".",".",".",".",".",".",".","."],[".",".",".","p",".",".",".","."],[".",".",".","p",".",".",".","."],["p","p",".","R",".","p","B","."],[".",".",".",".",".",".",".","."],[".",".",".","B",".",".",".","."],[".",".",".","p",".",".",".","."],[".",".",".",".",".",".",".","."]]
    print(board)
    print(s.numRookCaptures(board))

if __name__ == '__main__':
    main()