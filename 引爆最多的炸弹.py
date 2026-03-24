class Solution:
    def maximumDetonation(self, bombs: list[list[int]]) -> int:
        length = len(bombs)
        # 每两个炸弹之间的距离用distance保存
        distance = [[0 for _ in range(length)] for _ in range(length)]
        # print(distance)
        for i in range(0, length - 1, 1):
            for j in range(i+1, length):
                # print(i, j)
                cur_distance = (bombs[i][0] - bombs[j][0]) ** 2 + (bombs[i][1] - bombs[i][1]) ** 2
                cur_distance = cur_distance ** 0.5
                distance[i][j] = distance[j][i] = cur_distance
        for i in range(length):
            distance[i][i] = bombs[i][2]
        print(distance)
        # 接着需要有一个max来存放最大的引爆数目
        # 第i行表示第i个炸弹和其它的一个距离
        max_max = 0
        for i in range(length):
            cur_r = bombs[i][2]
            cur_max = 0
            for j in range(length):
                if distance[i][j] <= cur_r:
                    print(cur_r, distance[i][j])
                    cur_max += 1
            max_max = max(max_max, cur_max)

        return max_max

def main():
    s = Solution()
    bombs = [[1,1,100000],[100000,100000,1]]
    print(s.maximumDetonation(bombs))

if __name__ == '__main__':
    main()


