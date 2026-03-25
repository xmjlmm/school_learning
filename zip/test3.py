# 创建2个列表
m = [1, 2, 3]
n = [4, 5, 6]

print("*zip(m, n)返回:", *zip(m, n))
m2, n2 = zip(*zip(m, n))
print("m2和n2的值分别为:", m2, n2)
# 若相等，返回True；说明*zip为zip的逆过程
print(m == list(m2) and n == list(n2))
