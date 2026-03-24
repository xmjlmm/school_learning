import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 示例数据
data = {
    'X1': [2.5, 0.5, 2.2, 1.9, 3.1, 2.3, 2, 1, 1.5, 1.1],
    'X2': [2.4, 0.7, 2.9, 2.2, 3.0, 2.7, 1.6, 1.1, 1.6, 0.9],
    'X3': [2.2, 0.8, 2.5, 2.0, 2.8, 2.5, 1.8, 0.9, 1.4, 0.8]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 标准化数据
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# 创建PCA模型
pca = PCA(n_components=2)  # 使用2个主成分
pca.fit(scaled_data)

# 应用PCA模型
pca_results = pca.transform(scaled_data)

# 打印结果
print("原始数据:\n", df)
print("主成分得分:\n", pca_results)
print("解释的方差比:\n", pca.explained_variance_ratio_)
