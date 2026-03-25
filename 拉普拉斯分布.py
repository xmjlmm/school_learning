# 拉普拉斯的概率密度函数和正态分布的概率密度函数
from scipy.stats import laplace, norm
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(laplace.ppf(0.01), laplace.ppf(0.99), 100)
plt.plot(x, laplace.pdf(x), 'r-', lw=2, alpha=0.6, label='laplace pdf')
plt.plot(x, norm.pdf(x), lw=2, label="norm pdf")
plt.legend()
plt.show()