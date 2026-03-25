import matplotlib.pyplot as plt
import numpy as np

data = ((3, 10,2), (10, 3,2), (10, 5,5), (7, 8,6), (5, 1,3))

dim = len(data[0])
w = 0.75
dimw = w / dim

fig, ax = plt.subplots()
x = np.arange(len(data))
for i in range(len(data[0])):
    y = [d[i] for d in data]
    b = ax.bar(x + i * dimw, y, dimw, bottom=0.001)

ax.set_xticks(x + dimw )    #此处只是为了将刻度设置在几组数据的中心位置处
#ax.set_yscale('log')       #将y坐标用log计算

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(('A','B','C'),loc=0)
plt.show()