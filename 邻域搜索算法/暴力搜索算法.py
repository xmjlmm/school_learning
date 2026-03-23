import numpy as np
import math
# 城市坐标和需求量
cities = np.array([
    [1304, 2312], [3639, 1315], [4177, 2244], [3712, 1399], [3488, 1535],
    [3326, 1556], [3238, 1229], [4196, 1044], [4312, 790], [4386, 570],
    [3007, 1970], [2562, 1756], [2788, 1491], [2381, 1676], [1332, 695],
    [3715, 1678], [3918, 2179], [4061, 2370], [3780, 2212], [3676, 2578],
    [4029, 2838], [4263, 2931], [3429, 1908], [3507, 2376], [3394, 2643],
    [3439, 3201], [2935, 3240], [3140, 3550], [2545, 2357], [2778, 2826],
    [2370, 2975]
])

demands = np.array([20, 90, 90, 60, 70, 70, 40, 90, 90, 70, 60, 40, 40, 20, 80, 80, 90, 70, 100,
                    50, 50, 80, 70, 50, 40, 40, 70, 40, 60, 50, 40, 30])
def d(a,b):
    c_a = cities[a]
    c_b = cities[b]
    return math.sqrt((c_a[0] - c_b[0]) ** 2 + (c_a[1] - c_b[1]) ** 2)

# 6个城市
max_ans = np.inf
length = len(cities)
for i in range(length-5):
    cur_i = cities[i]
    for j in range(i+1, length-4):
        cur_j = cities[j]
        for k in range(j+1, length-3):
            cur_k = cities[k]
            for m in range(k+1, length-2):
                cur_m = cities[m]
                for n in range(m+1, length - 1):
                    cur_n = cities[n]
                    for c in range(n+1, length):
                        cur_c = cities[c]
                        ans = 0
                        for e in range(length):
                            if e != i and e != j and e != k and e != m and e != n and e !=c:
                                ans = ans + min(d(i,e),d(j,e),d(k,e),d(m,e),d(n,e),d(c,e)) * demands[e]
                        if (ans < max_ans):
                            max_ans = ans


print(max_ans)


