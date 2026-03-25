'''coins = [1, 2, 5]
amount = 11
length = len(coins)

def coinChange(depth, amount, count):
    if amount == 0:
        return count
    if depth == length:
        return -1

    if coins[depth] <= amount:
        possible = amount % coins[depth]
        tep = []
        while possible >= 0:
            tep.append(coinChange(depth + 1, amount - possible * coins[depth], count + possible))
            possible = possible - 1
        tmp2 = coinChange(depth + 1, amount, count)
        ans = min(min(tep), tmp2)
    else:
        ans = coinChange(depth + 1, amount, count)

    return ans

res = coinChange(0, amount, 0)
print(res)'''


'''coins = [1, 2, 5]
amount = 11
length = len(coins)'''

'''coins = [1, 2, 5]
amount = 11
length = len(coins)

def coinChange(depth, amount, count):
    if amount == 0:
        return count
    if depth == length:
        return -1

    if coins[depth] <= amount:
        tmp1 = coinChange(depth, amount - coins[depth], count + 1)
        tmp2 = coinChange(depth + 1, amount, count)
        ans = min(tmp1, tmp2)
    else:
        ans = coinChange(depth + 1, amount, count)
    return ans

res = coinChange(0, amount, 0)
print(res)'''



import math
coins = [1, 2, 5]
# coins = [2]
# coins = [1]
amount = 11
# amount = 3
# amount = 0
dp = [0 for _ in range(amount+1)]

for i in range(1, amount+1):
    if i in coins:
        dp[i] = 1
    else:
        res = []
        for j in coins:
            if i - j >= 0:
                res.append(dp[i - j] + 1)
        if len(res) == 0:
            dp[i] = 0
        else:
            dp[i] = min(res)

print(dp[-1])






