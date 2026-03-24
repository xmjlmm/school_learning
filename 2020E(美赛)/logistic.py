'''
import numpy as np
import pandas as pd
import csv
from scipy.stats import lognorm
import math
import matplotlib.pyplot as plt
D = [0.1, 3, 7, 2, 1, 3, 1.5, 1.5] # plastic lifetime standard deviation
E = [0.5, 13, 35, 8, 3, 20, 5, 5] # plastic lifetime expectation
b = 0.359
def use_age(kind, year):
    d = D[kind] ** 2
    s = math.log((1 + d / (E[kind] ** 2))) ** 0.5
    mu = math.log(E[kind]) - 0.5 * math.log((1 + D[kind] / (E[kind] ** 2)))
    res = lognorm.cdf(year, s, scale=math.exp(mu)) - lognorm.cdf(year-1,
    s, scale=math.exp(mu))
    return res
class Plastic(object):
    def __init__(self, total, year, discard=100, inc=0, rec=0):
        self.Total = total
        self.Year = year
        self.Trans = total * 0.066
        self.Pack = total * b
        self.Bui_Cons = total * 0.160
        self.Elect = total * 0.044
        self.Cons_Indus = total * 0.103
        self.IndMach = total * 0.007
        self.Other = total * 0.145
        self.Tef = total * 0.115
        self.DisRatio = discard / 100
        self.Inc = inc / 100
        self.Rec = rec / 100
        def Recycle(self, rec):
        self.Total += rec
        self.Trans += rec * 0.067
        self.Pack += rec * 0.448
        self.Bui_Cons += rec * 0.188
        self.Elect += rec * 0.038
        self.Cons_Indus += rec * 0.008
        self.Other += rec * 0.132

# Read the annual plastic productions
Global_plastics_production_file = 'global-plastics-production.csv'
df_AP = pd.read_csv(Global_plastics_production_file, usecols=[2, 3])
df_AP_list = np.array(df_AP)
Ap_list = df_AP_list.tolist()
AP = list(Plastic(item[1], item[0]) for item in Ap_list)
# Read the ratios
G_P_F = 'global-plastic-fate.csv'
df_R = pd.read_csv(G_P_F, usecols=[0, 2, 3])
df_R_list = np.array(df_R)
R_list = df_R_list.tolist()
for item in R_list:
    if item[0] == 'Discarded':
        AP[item[1] - 1950].DisRatio = item[2] / 100
    elif item[0] == 'Incinerated':
        AP[item[1] - 1950].Inc = item[2] / 100
    elif item[0] == 'Recycled':
        AP[item[1] - 1950].Rec = item[2] / 100
        AW_s = np.zeros(66)
        AW_o = np.zeros(66)
        AW = np.zeros(66)
        Plt = np.zeros(66)
for t in range(1, 66):
    AW_s[t] += AP[t-1].Pack * use_age(0, 1)
    AW_s[t] += AP[t-2].Pack * use_age(0, 2) # calculate the annual waste
    #of single-use plastic
    for j in range(1, t+1):
        AW_o[t] += AP[t - j].Trans * use_age(1, j)
        AW_o[t] += AP[t - j].Bui_Cons * use_age(2, j)
        AW_o[t] += AP[t - j].Elect * use_age(3, j)
        AW_o[t] += AP[t - j].Cons_Indus * use_age(4, j)
        AW_o[t] += AP[t - j].IndMach * use_age(5, j)
        AW_o[t] += AP[t - j].Other * use_age(6, j)
        AW_o[t] += AP[t - j].Tef * use_age(7, j)
        AW[t] = AW_s[t] + AW_o[t]
        AP[(t+1) % 66].Recycle(AW_o[t] * AP[t].Rec)
        Plt[t] = AW_s[t] * (1 - AP[t].Inc) + AW_o[t] * (1 - AP[t].Inc - AP[t].Rec)
    with open('data_1951-2015.csv', 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Year", "AW_s", "AW_o", "AW", "Pollution"])
        for i in range(1, 66):
            writer.writerow([i+1950, AW_s[i], AW_o[i], AW[i], Plt[i]])
x = np.arange(1951, 2016, 1)
plt.subplot(121)
plt.plot(x, AW_o[1:], label='AW_o', color='r')
plt.plot(x, AW_s[1:], label='AW_s', color='b')
plt.plot(x, AW[1:], label='Total', color='g')
plt.legend()
plt.subplot(122)
plt.plot(x, Plt[1:], label='Pollution', color='y')
plt.legend()
plt.show()
'''


# logistic模型
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# 示例数据集
features = np.array([[2, 3], [3, 5], [5, 8], [7, 10], [4, 5], [6, 9], [8, 10]])
target = np.array([0, 0, 1, 1, 0, 1, 1])

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# 创建逻辑回归模型
model = LogisticRegression()

# 训练模型
model.fit(X_train, y_train)

# 预测
predictions = model.predict(X_test)

# 评估模型
print("分类报告:")
print(classification_report(y_test, predictions))
print("混淆矩阵:")
print(confusion_matrix(y_test, predictions))



