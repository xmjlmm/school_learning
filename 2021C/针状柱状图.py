import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 假设数据集已经加载到一个 DataFrame 中
# 示例数据生成，50个供应商，100个数据点
np.random.seed(0)
data = pd.DataFrame(np.random.rand(100, 50) * 10000, columns=[f'供应商{i+1}' for i in range(50)])

# 将所有供应商的供应量求和
total_supply = data.sum(axis=0)

# 绘制柱状图
plt.figure(figsize=(15, 6))
total_supply.plot(kind='bar', color='blue')

# 添加图表标题和标签
plt.title('50家供应商供应量总览', fontsize=16)
plt.xlabel('供应商', fontsize=14)
plt.ylabel('供应量', fontsize=14)
plt.xticks(rotation=90)
plt.show()
