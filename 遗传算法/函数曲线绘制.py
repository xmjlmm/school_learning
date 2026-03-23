# 0≤x≤10
# f(x)=x+10sin(5x)+7cos(4x)

import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return x + 10 * np.sin(5 * x) + 7 * np.cos(4 * x)

def main():
    x = np.linspace(0, 10, 400)
    y = f(x)
    # 绘制曲线
    plt.plot(x, y)

    # 设置标题和轴标签
    plt.title('Function Curve: f(x) = x + 10sin(5x) + 7cos(4x)')
    plt.xlabel('x')
    plt.ylabel('f(x)')

    # 显示图形
    plt.show()

main()
