import numpy as np  # type: ignore
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

A = range(0, 6)  # 平旱地
B = range(6, 20)  # 梯田
C = range(20, 26)  # 山坡地
D = range(26, 34)  # 水浇地
E = range(34, 50)  # 普通大棚
F = range(50, 54)  # 智慧大棚

m = np.zeros((41, 54, 3), dtype=int)
cc = np.zeros((41, 54, 3), dtype=int)
a = range(0, 15)
# 平旱地
a_A = np.array([
    400, 500, 400, 350, 415, 800, 1000, 400, 630, 525, 110, 3000, 2200, 420, 525
])

a_B = np.array([
    380, 475, 380, 330, 395, 760, 950, 380, 600, 500, 105, 2850, 2100, 400, 500
])

a_C = np.array([
    360, 450, 360, 315, 375, 720, 900, 360, 570, 475, 100, 2700, 2000, 380, 475
])

b = 15
c = range(16, 34)

# 第一季
c_D = np.array([
    3000, 2000, 3000, 2000, 2400, 6400, 2700, 2400, 3300, 3700, 4100, 3200,
    12000, 4100, 1600, 10000, 5000, 5500
])

# 第一季
c_E = np.array([
    3600, 2400, 3600, 2400, 3000, 8000, 3300, 3000, 4000, 4500, 5000, 4000,
    15000, 5000, 2000, 12000, 6000, 6600
])

# 第2季
c_F = np.array([
    3200, 2200, 3200, 2200, 2700, 7200, 3000, 2700, 3600, 4100, 4500, 3600,
    13500, 4500, 1800, 11000, 5400, 6000
])

d = range(34, 37)

# 第2季
d_D = np.array([
    5000, 4000, 3000
])

e = range(37, 41)

# 第2季
e_E = np.array([
    5000, 4000, 10000, 1000
])

for crop in a:
    j = 0
    for i in A:
        m[crop, i, 0] = a_A[j]

    for i in B:
        m[crop, i, 0] = a_B[j]

    for i in C:
        m[crop, i, 0] = a_C[j]
    j += 1

for crop in c:
    j = 0
    for i in D:
        m[crop, i, 1] = c_D[j]

    for i in E:
        m[crop, i, 1] = c_E[j]

    for i in F:
        m[crop, i, 2] = c_F[j]
    j += 1
for crop in d:
    j = 0
    for i in D:
        m[crop, i, 0] = d_D[j]
    j += 1
for crop in e:
    j = 0
    for i in E:
        m[crop, i, 2] = e_E[j]
    j += 1
for i in D:
    m[b, i, 2] = 500

cc = np.zeros((41, 54, 3), dtype=int)
a = range(0, 15)
# 平旱地
a_A = np.array([
    400, 400, 350, 350, 350, 450, 500, 360, 400, 360, 350, 1000, 2000, 400, 350
])
a_B = np.array([
    400, 400, 350, 350, 350, 450, 500, 360, 400, 360, 350, 1000, 2000, 400, 350
])
a_C = np.array([
    400, 400, 350, 350, 350, 450, 500, 360, 400, 360, 350, 1000, 2000, 400, 350
])
b = 15
c = range(16, 34)
# 第一季
c_D = np.array([
    2000, 1000, 2000, 2000, 2000, 2000, 2300, 1600, 2400, 2900, 1600, 1600, 2900, 1600, 1000, 4100, 2000, 900
])
# 第一季
c_E = np.array([
    2400, 1200, 2400, 2400, 2400, 2400, 2700, 2000, 3000, 3500, 2000, 2000, 3500, 2000, 1200, 5000, 2500, 1100
])
# 第2季
c_F = np.array([
    2640, 1320, 2640, 2640, 2640, 2640, 3000, 2200, 3300, 3850, 2200, 2200, 3850, 2200, 1300, 5500, 2750, 1200
])
d = range(34, 37)
# 第2季
d_D = np.array([
    2000, 500, 500
])

e = range(37, 41)
# 第2季
e_E = np.array([
    3000, 2000, 10000, 10000
])

for crop in a:
    j = 0
    for i in A:
        cc[crop, i, 0] = a_A[j]

    for i in B:
        cc[crop, i, 0] = a_B[j]

    for i in C:
        cc[crop, i, 0] = a_C[j]
    j += 1

for crop in c:
    j = 0
    for i in D:
        cc[crop, i, 1] = c_D[j]

    for i in E:
        cc[crop, i, 1] = c_E[j]

    for i in F:
        cc[crop, i, 2] = c_F[j]
    j += 1
for crop in d:
    j = 0
    for i in D:
        cc[crop, i, 0] = d_D[j]
    j += 1
for crop in e:
    j = 0
    for i in E:
        cc[crop, i, 2] = e_E[j]
    j += 1
for i in D:
    cc[b, i, 2] = 680

ps = np.array([
    [147, 0, 0],
    [46, 0, 0],
    [60, 0, 0],
    [96, 0, 0],
    [25, 0, 0],
    [222, 0, 0],
    [135, 0, 0],
    [185, 0, 0],
    [50, 0, 0],
    [25, 0, 0],
    [15, 0, 0],
    [13, 0, 0],
    [18, 0, 0],
    [35, 0, 0],
    [20, 0, 0],
    [42, 0, 0],
    [0, 11.8, 0],
    [0, 13.2, 0],
    [0, 1.8, 0],
    [0, 15, 0],
    [0, 14.6, 0.3],
    [0, 6.6, 0.3],
    [0, 0.6, 0.3],
    [0, 0.9, 0.3],
    [0, 0.9, 0],
    [0, 0.9, 0],
    [0, 10.6, 0],
    [0, 0.6, 0.3],
    [0, 0.3, 0.3],
    [0, 0.6, 0.3],
    [0, 0.3, 0],
    [0, 0.3, 0],
    [0, 0, 0],
    [0, 0, 0.3],
    [0, 0, 30],
    [0, 0, 25],
    [0, 0, 12],
    [0, 0, 1.8],
    [0, 0, 1.8],
    [0, 0, 1.8],
    [0, 0, 4.2]
])

p = np.array([
    [3.25, 0, 0],
    [7.5, 0, 0],
    [8.25, 0, 0],
    [7, 0, 0],
    [6.75, 0, 0],
    [3.5, 0, 0],
    [3, 0, 0],
    [6.75, 0, 0],
    [6, 0, 0],
    [7.5, 0, 0],
    [40, 0, 0],
    [1.5, 0, 0],
    [3.25, 0, 0],
    [5.5, 0, 0],
    [3.5, 0, 0],
    [7, 0, 0],
    [0, 8, 9.600000381],
    [0, 6.75, 8.100000381],
    [0, 6.5, 7.800000191],
    [0, 3.75, 4.5],
    [0, 6.25, 7.5],
    [0, 5.5, 6.599999905],
    [0, 5.75, 6.900000095],
    [0, 5.25, 6.800000191],
    [0, 5.5, 6.599999905],
    [0, 6.5, 7.800000191],
    [0, 5, 6],
    [0, 5.75, 6.900000095],
    [0, 7, 8.399999619],
    [0, 5.25, 6.300000191],
    [0, 7.25, 8.699999809],
    [0, 4.5, 5.400000095],
    [0, 4.5, 5.400000095],
    [0, 4, 4.800000191],
    [0, 0, 2.5],
    [0, 0, 2.5],
    [0, 0, 3.25],
    [0, 0, 57.5],
    [0, 0, 19],
    [0, 0, 16],
    [0, 0, 100]
])
for i in range(41):
    for j in range(54):
        for k in range(3):
            print(m[i][j][k])

# 复制并合并成形状为 (54, 41, 3) 的数组
p = np.tile(p, (54, 1, 1))
# 设置每种蔬菜的最小种植面积和每块地的最大种植面积
min_area_per_crops = np.ones((41, 54, 3)) * 0.3

max_area_per_land = np.array([
    80, 55, 35, 72, 68, 55, 60, 46, 40, 28, 25, 86, 55, 44, 50, 25, 60, 45, 35, 20, 15, 13, 15,
    18, 27, 20, 15, 10, 14, 6, 10, 12, 22, 20, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6,
    0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6
])

# 随机生成每种蔬菜可以种植的地块
# i: 蔬菜种类 j: 地块编号
allow_matrix = np.zeros((41, 54, 3), dtype=int)

for crop in range(0, 15):
    temp = list(A) + list(B) + list(C)
    for land in temp:
        allow_matrix[crop, land, 0] = 1

for land in D:
    allow_matrix[15, land, 0] = 1

for crop in range(16, 34):
    temp = list(D) + list(E) + list(F)
    for land in temp:
        allow_matrix[crop, land, 1] = 1
    for land in F:
        allow_matrix[crop, land, 2] = 1

for crop in range(34, 37):
    for land in list(D):
        allow_matrix[crop, land, 2] = 1

for crop in range(37, 41):
    for land in list(E):
        allow_matrix[crop, land, 2] = 1

min_area_per_crops = min_area_per_crops * allow_matrix
# print(min_area_per_crops)

# cc= np.random.randint(400, 1000, (41, 54, 3))
# 创建优化模型
model = LpProblem(name="max_profit")

# 创建决策变量
x = LpVariable.dicts("x", (range(41), range(54), range(3), range(7)), lowBound=0, upBound=120 , cat = "Continuous")

# 创建辅助变量
y = LpVariable.dicts("y", (range(41), range(54), range(3), range(7)), lowBound=0, upBound=120, cat="Continuous")

# 目标函数: 最大化7年的总利润
model += lpSum(
    y[i][j][k][l] * p[j, i, k] * m[i, j, k] - cc[i, j, k] * x[i][j][k][l] for i in range(41) for j in range(54) for k in range(3) for
    l in range(7))

# # 添加约束条件，使辅助变量等于较小值
for i in range(41):
    for k in range(3):
        for l in range(7):
            # 约束1: y <= x * m
            for j in range(54):
                model += y[i][j][k][l] <= x[i][j][k][l] * m[i, j, k]
            # 约束2: y <= ps
            model += lpSum(y[i][j][k][l] for j in range(54)) <= ps[i, k]

            # model += lpSum( y[i][j][k][l] for j in range(54)) <= lpSum(x[i][j][k][l] * m[i, j, k] for j in range(54))
            # model += lpSum( y[i][j][k][l] for j in range(54)) <= ps[i, k]

# # 约束1: y <= x * m
# for i in range(41):
#     for k in range(3):
#         for l in range(7):
#             for j in range(54):
#                 model += y[i][j][k][l] <= x[i][j][k][l] * m[i, j, k]
#
# # 约束2: y <= ps
# for i in range(41):
#     for k in range(3):
#         model += lpSum(y[i][j][k][l] for j in range(54)) <= ps[i, k]

# 约束条件
# 每块地每年最大种植面积
for l in range(7):
    for j in range(54):
        model += lpSum(x[i][j][k][l] for i in range(41) for k in range(3)) <= max_area_per_land[j]

# 每种蔬菜的最小种植面积
for l in range(7):
    for i in range(41):
        model += lpSum(x[i][j][k][l] for j in range(54) for k in range(3)) >= min_area_per_crops[i]

# 每种蔬菜只能在允许的地块种植
for i in range(41):
    for j in range(54):
        for k in range(3):
            for l in range(7):
                if allow_matrix[i, j, k] == 0:
                    model += x[i][j][k][l] == 0

# 求解模型
model.solve()

# 输出结果
print("状态:", model.status)

for i in range(41):
    for j in range(54):
        for k in range(3):
            for l in range(7):
                if value(x[i][j][k][l]) > 0:
                    print(f"在第{(k + 1)}年，第{i + 1}块地种植第{j + 1}种蔬菜的面积: {value(x[i][j][k][l])}")
print("最大七年总利润:", value(model.objective))