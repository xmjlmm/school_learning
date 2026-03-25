import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['100', '200', '300', '400']

plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

x = np.arange(len(labels))
width = 0.15
fig, ax = plt.subplots()

color_my = ['C2','C3','C1','C6','C5','C7']


def huizhi(ax, data, x):
    bottom = 0
    for j in range(len(data)):
        height = data[j]
        ax.bar(x, height, width, bottom=bottom, color=color_my[j])
        bottom += height


data1 = [[29, 14, 2, 1, 2, 0],
            [5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]

data2 = [[12, 58, 21, 7, 4, 2],
            [45, 16, 7, 1, 3, 2],
            [26, 3, 1, 0, 2, 0],
            [10, 0, 0, 0, 0, 0]]

data3 = [[23, 19, 42, 17, 5, 4],
            [53, 38, 27, 1, 3, 2],
            [32, 8, 19, 0, 2, 0],
            [19, 0, 0, 10, 0, 0]]

data4 = [[260, 29, 54, 33, 9, 6],
            [180, 67, 33, 4, 5, 3],
            [257, 21, 19,10, 2, 0],
            [210, 0, 0, 0, 0, 0]]

para=[-1.5, -0.5, 0.5, 1.5]
def draw_each_bar(data_num, x, labels = ['d<=10','10<d<=50','50<d<=100','100<d<=200','200<d<=400','d>400']):
    print(x)
    for i in range(len(data_num)):
        bottom = 0
        for j in range(len(data_num[i])):
            height = data_num[i][j]
            if i==3 and x == 3:
                print('运行1')
                ax.bar(x + para[i] * width, height, width, bottom=bottom,facecolor= color_my[j],alpha = 0.9,label=labels[j])
            else:
                print('运行2')
                ax.bar(x + para[i] * width, height, width, bottom=bottom, facecolor=color_my[j], alpha=0.9)
            plt.axvline(x=x + (para[i] -0.5)* width, ls="-", c="white")  # 添加垂直直线
            bottom += height



draw_each_bar(data1, x[0])
draw_each_bar(data2, x[1])
draw_each_bar(data3, x[2])
draw_each_bar(data4, x[3])
ax.legend(loc=2)

ax.set_ylabel('Y轴标题/个')
ax.set_xlabel('X轴标题/个')
ax.set_xticks(x)
ax.set_xticklabels(labels)

#保存图片
fig.tight_layout()
plt.savefig("测试数据.png",dpi=300)
plt.show()