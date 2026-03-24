'''一张桌子上总共有 n 个硬币 栈 。每个栈有 正整数 个带面值的硬币。

每一次操作中，你可以从任意一个栈的 顶部 取出 1 个硬币，从栈中移除它，并放入你的钱包里。

给你一个列表 piles ，其中 piles[i] 是一个整数数组，分别表示第 i 个栈里 从顶到底 的硬币面值。

同时给你一个正整数 k ，请你返回在 恰好 进行 k 次操作的前提下，你钱包里硬币面值之和 最大为多少 。'''


memo = {}
# count表示当前进行了count次操作，heap表示当前是多少堆
def dfs(count, heap):
    # 记忆化剪枝
    if (count, heap) in memo:
        return memo[(count, heap)]
    # 终止条件判断达到最大操作次数或者已经遍历完所有堆
    if count == k or heap == length_piles:
        return 0 
    # ans表示全局最大值, res表示当前dfs计算的最终结果
    ans, res = dfs(count, heap+1), 0

    # 能够在当前堆里面遍历的最大次数不超过当前堆的容量以及可操作数
    for j in range(0, min(len(piles[heap]), k-count)):
        res = res + piles[heap][j]
        ans = max(ans, res + dfs(count+j+1, heap+1))
    memo[(count, heap)] = ans
    return ans

piles = [[100],[100],[100],[100],[100],[100],[1,1,1,1,1,1,700]]
k = 7
length_piles = len(piles)
print(dfs(0, 0))