import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, PULP_CBC_CMD, LpAffineExpression

A = range(0, 6)  # 平旱地
B = range(6, 20)  # 梯田
C = range(20, 26)  # 山坡地
D = range(26, 34)  # 水浇地
E = range(34, 50)  # 普通大棚
F = range(50, 54)  # 智慧大棚

# 亩产量
m = np.zeros((41, 54, 3), dtype=int)
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

j = 0
for crop in a:
    for i in A:
        m[crop, i, 0] = a_A[j]
    for i in B:
        m[crop, i, 0] = a_B[j]

    for i in C:
        m[crop, i, 0] = a_C[j]
    j += 1

j = 0
for crop in c:
    for i in D:
        m[crop, i, 1] = c_D[j]

    for i in E:
        m[crop, i, 1] = c_E[j]

    for i in F:
        m[crop, i, 2] = c_F[j]
    j += 1
j = 0
for crop in d:
    for i in D:
        m[crop, i, 0] = d_D[j]
    j += 1
j = 0
for crop in e:
    for i in E:
        m[crop, i, 2] = e_E[j]
    j += 1
for i in D:
    m[b, i, 2] = 500

########################### 成本
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

j = 0
for crop in a:
    for i in A:
        cc[crop, i, 0] = a_A[j]
    for i in B:
        cc[crop, i, 0] = a_B[j]
    for i in C:
        cc[crop, i, 0] = a_C[j]
    j += 1
j = 0
for crop in c:
    for i in D:
        cc[crop, i, 1] = c_D[j]
    for i in E:
        cc[crop, i, 1] = c_E[j]
    for i in F:
        cc[crop, i, 2] = c_F[j]
    j += 1
j = 0
for crop in d:
    for i in D:
        cc[crop, i, 0] = d_D[j]
    j += 1
j = 0
for crop in e:
    for i in E:
        cc[crop, i, 2] = e_E[j]
    j += 1
for i in D:
    cc[b, i, 2] = 680

###### 预期销量
ps = np.array([
    [57000, 0, 0],
    [21850, 0, 0],
    [22400, 0, 0],
    [33040, 0, 0],
    [9875, 0, 0],
    [170840, 0, 0],
    [132750, 0, 0],
    [71400, 0, 0],
    [30000, 0, 0],
    [12500, 0, 0],
    [1500, 0, 0],
    [35100, 0, 0],
    [36000, 0, 0],
    [14000, 0, 0],
    [10000, 0, 0],
    [21000, 0, 0],
    [0, 34320, 0],
    [0, 26880, 0],
    [0, 4320, 0],
    [0, 30000, 0],
    [0, 35400, 810],
    [0, 43200, 2160],
    [0, 1800, 810],
    [0, 2400, 0],
    [0, 2700, 0],
    [0, 4500, 0],
    [0, 34400, 1080],
    [0, 9000, 4050],
    [0, 1200, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 1800],
    [0, 0, 150000],
    [0, 0, 100000],
    [0, 0, 36000],
    [0, 0, 9000],
    [0, 0, 7200],
    [0, 0, 18000],
    [0, 0, 4200],
    [0, 0, 1350],
    [0, 0, 900]
])

###### 价格
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

# 复制并合并成形状为 (54, 41, 3) 的数组
p = np.tile(p, (54, 1, 1))

# 设置每种蔬菜的最小种植面积和每块地的最大种植面积
min_area_per_crops = np.ones(41) * 0.3

max_area_per_land = np.array([
    80, 55, 35, 72, 68, 55, 60, 46, 40, 28, 25, 86, 55, 44, 50, 25, 60, 45, 35, 20, 15, 13, 15,
    18, 27, 20, 15, 10, 14, 6, 10, 12, 22, 20, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6,
    0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6
])

######## 允许种植的0-1矩阵

# i: 蔬菜种类 j: 地块编号
allow_matrix = np.zeros((41, 54, 3), dtype=int)
# 粮食1-15可以在ABC地块种植
for crop in range(0, 15):
    temp = list(A) + list(B) + list(C)
    for land in temp:
        allow_matrix[crop, land, 0] = 1
# 水稻只能在D地块种植
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
# 豆类单季
must_select_0 = np.array([0, 1, 2, 3, 4])
# 豆类双季
must_select_12 = np.array([16, 17, 18])

# 创建优化模型
model = LpProblem(name="max_profit", sense=LpMaximize)

# 创建决策变量
x = LpVariable.dicts("x", (range(41), range(54), range(3), range(7)), lowBound=0, cat="Continuous")
z = LpVariable.dicts("z", (range(41), range(54), range(3), range(7)), cat="Binary")
y = LpVariable.dicts("y", (range(41), range(54), range(3), range(7)), lowBound=0, cat="Continuous")

m_init = m.copy()
cc_init = cc.copy()
p_init = p.copy()
ps_init = ps.copy()

sum_n_y = 0
iter_num = 750
for n in range(iter_num):
    m = m_init.copy()
    cc = cc_init.copy()
    p = p_init.copy()
    ps = ps_init.copy()

    for l in range(7):
        for k in range(3):
            for i in range(41):
                for j in range(54):
                    m[i, j, k] = m[i, j, k] * (1 + np.random.uniform(-0.1, 0.1))

        # 农作物的种植成本平均每年增长5%左右
        for k in range(3):
            for i in range(41):
                for j in range(54):
                    cc[i, j, k] = cc[i, j, k] * (1 + np.random.uniform(0.04, 0.06))

        # 粮食类作物的销售价格基本稳定，蔬菜类作物的销售价格有增长趋势，食用菌销售价格下降
        for k in range(3):
            for i in range(41):
                for j in range(54):
                    if i >= 16 and i < 37:
                        p[j, i, k] = p[j, i, k] * (1 + np.random.uniform(0.04, 0.06))
                    elif i >= 37 and i < 40:
                        p[j, i, k] = p[j, i, k] * (1 - np.random.uniform(0.01, 0.05))
                    elif i == 40:
                        p[j, i, k] = p[j, i, k] * (1 - 0.05)

                        # 小麦和玉米未来的预期销售量有增长的趋势，平均年增长率介于5%~10%之间，其他相对于2023年大约有 ±5%的 变化
        for k in range(3):
            for i in range(41):
                if i == 5 or i == 6:
                    ps[i, k] = ps[i, k] * (1 + np.random.uniform(0.05, 0.1))
                else:
                    ps[i, k] = ps_init[i, k] * (1 + np.random.uniform(-0.05, 0.05))

        ####### 不用年份来区分
        # 目标1
        # model += lpSum(y[i][j][k][l] * m[i, j, k] * p[j, i, k] - cc[i, j, k] * x[i][j][k][l] for i in range(41) for j in range(54) for k in range(3) for l in range(7))
        # 目标2
        sum_n_y += lpSum(y[i][j][k][l] * m[i, j, k] * p[j, i, k] - cc[i, j, k] * x[i][j][k][l] + (
                    m[i, j, k] * x[i][j][k][l] - y[i][j][k][l] * m[i, j, k]) * p[j, i, k] * 0.5 for i in range(41) for j
                         in range(54) for k in range(3))

model += sum_n_y

# 辅助变量   确保取min(ps,x*m)
for l in range(7):
    for i in range(41):
        for k in range(3):
            model += lpSum(y[i][j][k][l] * m[i][j][k] for j in range(54)) <= ps[i, k]
            model += lpSum(y[i][j][k][l] for j in range(54)) <= lpSum(x[i][j][k][l] for j in range(54))

# 确保y<=x
for i in range(41):
    for j in range(54):
        for k in range(3):
            for l in range(7):
                model += y[i][j][k][l] <= x[i][j][k][l]

            # 决策变量 z 的约束：确保种植面积与二进制变量 z 相关
for i in range(41):
    for j in range(54):
        for k in range(3):
            for l in range(7):
                model += x[i][j][k][l] <= 86 * z[i][j][k][l]

            # 23年种植数据
x_23 = np.array([
    [5, 0, 0],
    [6, 1, 0],
    [6, 2, 0],
    [0, 3, 0],
    [3, 4, 0],
    [7, 5, 0],
    [5, 6, 0],
    [1, 7, 0],
    [2, 8, 0],
    [3, 9, 0],
    [4, 10, 0],
    [7, 11, 0],
    [5, 12, 0],
    [7, 13, 0],
    [8, 14, 0],
    [9, 15, 0],
    [0, 16, 0],
    [6, 17, 0],
    [13, 18, 0],
    [14, 19, 0],
    [10, 20, 0],
    [11, 21, 0],
    [0, 22, 0],
    [12, 23, 0],
    [5, 24, 0],
    [2, 25, 0],
    [19, 26, 1],
    [35, 26, 2],
    [27, 27, 1],
    [34, 27, 2],
    [20, 28, 1],
    [34, 28, 2],
    [21, 29, 1],
    [34, 29, 2],
    [16, 30, 1],
    [35, 30, 2],
    [17, 31, 1],
    [36, 31, 2],
    [15, 32, 0],
    [15, 33, 0],
    [17, 34, 1],
    [37, 34, 2],
    [23, 35, 1],
    [37, 35, 2],
    [24, 36, 1],
    [37, 36, 2],
    [25, 37, 1],
    [38, 37, 2],
    [27, 38, 1],
    [38, 38, 2],
    [26, 39, 1],
    [38, 39, 2],
    [18, 40, 1],
    [39, 40, 2],
    [18, 41, 1],
    [39, 41, 2],
    [17, 42, 1],
    [39, 42, 2],
    [16, 43, 1],
    [40, 43, 2],
    [16, 44, 1],
    [40, 44, 2],
    [21, 45, 1],
    [40, 45, 2],
    [20, 46, 1],
    [40, 46, 2],
    [28, 47, 1],
    [40, 47, 2],
    [29, 48, 1],
    [26, 48, 1],
    [40, 48, 2],
    [30, 49, 1],
    [40, 49, 2],
    [31, 50, 1],
    [32, 50, 1],
    [23, 50, 2],
    [20, 50, 2],
    [24, 51, 1],
    [25, 51, 1],
    [21, 51, 2],
    [28, 51, 2],
    [16, 52, 1],
    [27, 52, 2],
    [29, 52, 2],
    [18, 53, 1],
    [33, 53, 2],
    [22, 53, 2]
])

z_23 = np.zeros((41, 54, 3), dtype=int)
for i, j, k in x_23:
    z_23[i, j, k] = 1
# 约束条件
############# cons1 : 豆类三次必须种一次
must_select = np.concatenate((must_select_0, must_select_12))
for j in range(54):
    for l in range(5):
        model += lpSum(
            z[i][j][k][ll] for k in range(3) for i in must_select for ll in range(l, l + 3) for k in range(3)) >= 1

for j in range(54):
    model += lpSum(z_23[i][j][k] for i in must_select for k in range(3)) + lpSum(
        z[i][j][k][l] for i in must_select for k in range(3) for l in range(2)) >= 1
############## cons2 : 每块地的种植面积不能超过最大种植面积
for l in range(7):
    for j in range(54):
        for k in range(3):
            model += lpSum(x[i][j][k][l] for i in range(41)) <= max_area_per_land[j]

############ cons3 : 同一块地不能连续种植同一种蔬菜
# 单季作物
danji = range(0, 16)
for l in range(6):
    for i in danji:
        for j in range(54):
            model += z[i][j][0][l] + z[i][j][0][l + 1] <= 1

for j in range(54):
    for i in danji:
        model += z_23[i][j][0] + z[i][j][0][0] <= 1

# 双季作物
shuangji = range(16, 41)
for k in range(1, 2):
    for l in range(6):  # 确保 l+1 不超出范围
        for i in shuangji:
            for j in range(54):
                # 前后两两相加小于1的约束条件
                model += z[i][j][k][l] + z[i][j][k + 1][l] <= 1
                model += z[i][j][k + 1][l] + z[i][j][k][l + 1] <= 1
                model += z[i][j][k][l + 1] + z[i][j][k + 1][l + 1] <= 1

for i in shuangji:
    for j in range(54):
        model += z_23[i][j][2] + z[i][j][1][0] + z[i][j][0][0] <= 1

######### cons4 : 每种蔬菜只能在允许的地块种植
for i in range(41):
    for j in range(54):
        for k in range(3):
            for l in range(7):
                if allow_matrix[i, j, k] == 0:
                    model += x[i][j][k][l] == 0
                    model += y[i][j][k][l] == 0

# ####### cons5 : 确保如果种植则种植的面积至少为0.3
for i in range(41):
    for j in range(54):
        for k in range(3):
            for l in range(7):
                model += x[i][j][k][l] >= 0.2 * z[i][j][k][l]

######## cons6 : 不能太分散

# for l in range(7):
#     for k in range(3):
#         for i in range(41):
#             sum_num = 0
#             for j in range(54):
#                 if z[i][j][k][l] >= 0.9:
#                     sum_num += 1
#             model += LpAffineExpression(sum_num) <= 5


# 求解模型
model.solve()

# 输出结果
print("状态:", model.status)

import numpy as np
import pandas as pd  # 导入 pandas 库

# 创建一个 ExcelWriter 对象
with pd.ExcelWriter(f'result2_{iter_num}.xlsx') as writer:
    yy = 2024
    for year in range(7):
        # 计算每一年的 re 数组的值
        re = np.zeros((82, 41))  # 每年重新初始化 re 数组
        for j in range(26):
            for i in range(41):
                k = 0
                if value(x[i][j][0][year]) > 0:
                    re[j, i] += value(x[i][j][0][year])

        for j in range(26, 54):
            for i in range(41):
                for k in range(1, 3):
                    if value(x[i][j][k][year]) > 0 and k == 1:
                        re[j, i] += value(x[i][j][k][year])
                    if value(x[i][j][k][year]) > 0 and k == 2:
                        re[j + 28, i] += value(x[i][j][k][year])
        df = pd.DataFrame(re)
        df.to_excel(writer, sheet_name=f'{yy}', index=False, header=False)
        yy += 1

print("最大七年总利润:", value(model.objective) / iter_num / 7, "元")
if model.status == 1:
    print("Optimal")
elif model.status == 0:
    print("Not Solved")

# re = np.zeros(7)
# # 累积目标函数
# for l in range(7):
#     yyyy = 0  # 初始化每年的利润
#     for k in range(3):
#         for i in range(41):
#             pps = ps[i][k]
#             cost_term = sum(cc[i][j][k] * value(x[i][j][k][l]) for j in range(54))
#             production_sum = sum(value(y[i][j][k][l]) * m[i][j][k] for j in range(54))
#
#             yyyy += production_sum * p[i][k] - cost_term
#     re[l] = yyyy  # 存储每年的利润
#
# # 打印每年的利润
# for year in range(7):
#     print(f"第 {2024 + year} 年的利润: {re[year]}")

