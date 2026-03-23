'''
题目：求1+2!+3!+...+10!的和

提醒：需要实现一个函数 f(n)来完成n!，从而用f(1)+f(2)+...+f(10)完成求和'''
'''
def frac(n):
    tmp = 1
    for i in range(1,n+1):
        tmp = tmp * i
    return tmp

def main():
    sum = 0
    for n in range(1,11):
        sum = sum + frac(n)
    print(sum)
main()
'''

'''
s = input('')
length = len(s)
for i in range(length):
    st = s[i:length] + s[0:i]
    print(st)
'''


import matplotlib.pyplot as plt


# 定义层（layers）中的节点数
n_layers = [4, 6, 6, 1]

# 定义颜色
layer_colors = ['red', 'cyan', 'cyan', 'green']

fig, ax = plt.subplots(1,1)

#对于每层
for i in range(len(n_layers)):
    # 绘制节点
    nodes = list(range(1,n_layers[i]+1))
    for n in nodes:
        ax.plot(i,n,'o',color=layer_colors[i], markersize=30)

    # 如果不是最后一层，画连线（weights）
    if i!=len(n_layers)-1:
        next_nodes = list(range(1,n_layers[i+1]+1))
        for n in nodes:
            for nn in next_nodes:
                ax.plot([i,i+1],[n,nn], 'black')

# 隐藏坐标轴
ax.axis('off')

plt.show()
