import numpy as np
import geatpy as ea
import pandas as pd
df_1 = pd.read_excel('/df1.xlsx',sheet_name="df1")
df_2= pd.read_excel('/df1.xlsx',sheet_name="df2")
a = df_1["损耗率"] # 填入实际数据
c = df_1["批发均价"] # 填入实际数据
beta_0 = df_1["beta0"] # 填入实际数据
beta_1 = df_1["beta1"]
d = df_2["品类需求"]
class MyProblem(ea.Problem): # 继承 Problem 父类
    def __init__(self):
        name = 'MyProblem' # 初始化 name（函数名称，可以随意设置）
        M = 1 # 初始化 M（目标维数）
        # 初始化 maxormins（目标最小最大化标记列表，1：最小化；-1：最大化）
        maxormins = [-1]
        Dim = 58*2+6 # 初始化 Dim（决策变量维数）
        # 初始化决策变量的类型，元素为 0 表示变量是连续的；1 为离散的

        varTypes = [1]*58 + [0]*58+[1]*6+[1]*6
        lb = [0]*58+[c[i] for i in range(0,58)]+[0]*6+[0]*6 # 决策变量下界
        ub = [1]*58+[50]*58+[1]*6 +[1]*6 # 决策变量上界
        lbin = [1] * Dim # 决策变量下边界
        ubin = [1] * Dim # 决策变量上边界
        # 调用父类构造方法完成实例化
        print(1)
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
    def aimFunc(self, pop): # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵
        x = [0] * 58
        y = [0] * 58
        u = [0] * 6
        v = [0] * 6
        for i in range(0, 58):
            x[i] = Vars[:, [i]]
        for i in range(0, 58):
            y[i] = Vars[:, [i + 58]]
        for i in range(0, 6):
            u[i] = Vars[:, [i + 58 + 6]]
        for i in range(0, 6):
            u[i] = Vars[:, [i + 58 + 6 * 2]]
        pop.ObjV = sum([(1 - a[i] / 100) * ((y[i] - beta_0[i]) / beta_1[i] - c[i]) * y[i] * x[i] for i in range(0, 58)])
        pop.CV = np.hstack(
            [(27 - sum(x)), (sum(x) - 33)] + [(2.5 * x[i] - y[i]) for i in range(0, 58)] + [(y[i] - 100 * x[i] - 1) for i in range(0, 58)] + [
                5 - sum(u)] + [5 - sum(v)] + [u[0] * (0.6 * d[5] - sum(y[0:7])), u[1] * (0.6 * d[4] - sum(y[7:17])),
                                              u[2] * (0.6 * d[3] - sum(y[17:22])), u[3] * (0.6 * d[2] - sum(y[22:36])),
                                              u[4] * (0.6 * d[1] - sum(y[36:55])),
                                              u[5] * (0.6 * d[0] - sum(y[55:58]))] + [v[0] * (sum(y[0:7]) - 8 * d[5]),
                                                                                      v[1] * (sum(y[7:17]) - 8 * d[4]),
                                                                                      v[2] * (sum(y[17:22]) - 8 * d[3]),
                                                                                      v[3] * (sum(y[22:36]) - 8 * d[2]),
                                                                                      v[4] * (sum(y[36:55]) - 8 * d[1]),
                                                                                      v[5] * (sum(y[55:58]) - 8 * d[0])])

#[(27-sum(x))]
#+[(2.5*x[i]-y[i]) for i in range(0, 58)]
# +[(sum(y[0:7])-2*d[5]),(sum(y[7:17])-2*d[4]),(sum(y[17:22])-2*d[3]),
# (sum(y[22:36])-2*d[2]),(sum(y[36:55])-2*d[1]),(sum(y[55:58])-2*d[0])])

#实例化问题对象
problem = MyProblem()
Encoding = "RI" #实整数编码，还有"BG":二进制/格雷码， "P":排列编码
NIND = 200 #种群规模
Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) #创建区域描述器
population = ea.Population(Encoding, Field, NIND)
#算法参数设置
myAlgorithm = ea.soea_DE_best_1_L_templet(problem, population) #算法模板，这里使用差分进化 DE/best/1/L
myAlgorithm.MAXGEN = 2000 #最大进化次数
myAlgorithm.mutOper.F = 0.5 #突变概率
myAlgorithm.recOper.XOVR = 0.7 #交叉概率
myAlgorithm.logTras = 0 #打印日志， 0 表示不打印
myAlgorithm.verbose = False
myAlgorithm.drawing = 1 #绘图
#种群进化
[BestIndi, population] = myAlgorithm.run() # 执行算法模板，得到最优个体以及最后一代种群
#输出结果
print('评价次数：%s'%(myAlgorithm.evalsNum))
print('花费时间 %s 秒'%(myAlgorithm.passTime))
if BestIndi.sizes != 0:
    print("最优的目标函数值为 %s" % BestIndi.ObjV[0][0])
    print("最优决策变量:")
for i in range(BestIndi.Phen.shape[1]):
    print(BestIndi.Phen[0, i])
else:
    print("未找到解")