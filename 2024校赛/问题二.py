# import pandas as pd
# import numpy as np
# from sklearn.decomposition import PCA
#
# # 数据收集与清洗
# # 假设已经从各个来源收集到了ESG评分数据和相关行业标准等数据，并存储在数据框中
#
# # 生成随机的ESG评分数据和财务绩效数据
# np.random.seed(0)  # 设置随机种子以确保可复现性
#
# # 假设有100家公司，每家公司有3个ESG评分指标和1个财务绩效指标
# num_companies = 100
# esg_scores = np.random.uniform(low=0, high=100, size=(num_companies, 3))  # 生成ESG评分数据
# financial_performance = np.random.uniform(low=0, high=100, size=num_companies)  # 生成财务绩效数据
#
# # 创建数据框
# esg_data = pd.DataFrame(esg_scores, columns=['esg_score', 'esg_factor1', 'esg_factor2'])
# financial_data = pd.DataFrame({'financial_performance_metric': financial_performance})
#
# # 假设数据中存在缺失值
# # 随机将一部分数据设为缺失值
# esg_data.iloc[::10, :] = np.nan
# financial_data.iloc[::10, :] = np.nan
#
# # 输出部分数据
# print("ESG评分数据示例：")
# print(esg_data.head())
# print("\n财务绩效数据示例：")
# print(financial_data.head())
#
# # 随机生成行业标准数据框
# industry_data = pd.DataFrame({
#     'company_id': range(1, 101),  # 100家公司，与ESG评分数据框相同
#     'industry_standard': np.random.randint(0, 11, size=100)  # 随机生成0到10的行业标准数据
# })
#
#
# # 假设esg_data是ESG评分数据框，industry_data是行业标准数据框
# # 进行数据清洗，处理缺失值等
# esg_data_cleaned = esg_data.dropna()
# industry_data_cleaned = industry_data.dropna()
#
# # 多变量分析
# # 使用主成分分析（PCA）从多种数据中提取主要风险因子
#
# # 合并数据
# merged_data = pd.merge(esg_data_cleaned, industry_data_cleaned, on='company_id')
#
# # 提取特征和目标变量
# X = merged_data.drop(columns=['company_id', 'esg_score'])
# y = merged_data['esg_score']
#
# # 初始化PCA模型
# pca = PCA(n_components=3)  # 假设提取3个主成分
#
# # 拟合PCA模型并转换数据
# X_pca = pca.fit_transform(X)
#
# # 主要风险因子提取
# # 主成分分析提取的主成分即为主要风险因子
#
# # 构建风险度量指标
# # 假设这里简单地将主成分加总作为风险度量指标
# risk_measure = np.sum(X_pca, axis=1)
#
# # 结果呈现与分析
# # 将提取的主要风险因子和构建的风险度量指标详细呈现在报告中
#
# # 输出风险度量指标
# print("风险度量指标：", risk_measure)
#
# # 分析每个主要风险因子对ESG投资绩效的影响
#
# # 提取主成分对应的特征向量，解释主成分
# component_names = [f"PC{i+1}" for i in range(pca.n_components_)]
# components_df = pd.DataFrame(pca.components_, columns=X.columns, index=component_names)
#
# # 打印主成分对应的特征向量
# print("主成分对应的特征向量：")
# print(components_df)


# import pandas as pd
# import numpy as np
# from sklearn.decomposition import PCA
#
# # 随机生成ESG评分数据框
# esg_data = pd.DataFrame({
#     'company_id': range(1, 101),  # 100家公司
#     'esg_score': np.random.randint(0, 101, size=100)  # 随机生成0到100的ESG评分
# })
#
# # 随机生成行业标准数据框
# industry_data = pd.DataFrame({
#     'company_id': range(1, 101),  # 100家公司，与ESG评分数据框相同
#     'industry_standard': np.random.randint(0, 11, size=100)  # 随机生成0到10的行业标准数据
# })
#
# # 打印ESG评分数据框的前5行
# print("ESG评分数据框：")
# print(esg_data.head())
#
# # 打印行业标准数据框的前5行
# print("\n行业标准数据框：")
# print(industry_data.head())
#
# # 数据收集与清洗
# # 假设已经从各个来源收集到了ESG评分数据和相关行业标准等数据，并存储在数据框中
#
# # 进行数据清洗，处理缺失值等
# esg_data_cleaned = esg_data.dropna()
# industry_data_cleaned = industry_data.dropna()
#
# # 多变量分析
# # 使用主成分分析（PCA）从多种数据中提取主要风险因子
#
# # 合并数据
# merged_data = pd.merge(esg_data_cleaned, industry_data_cleaned, on='company_id')
#
# # 提取特征和目标变量
# X = merged_data.drop(columns=['company_id', 'esg_score'])
# y = merged_data['esg_score']
#
# # 初始化PCA模型
# pca = PCA(n_components=3)  # 假设提取3个主成分
#
# # 拟合PCA模型并转换数据
# X_pca = pca.fit_transform(X)
#
# # 主要风险因子提取
# # 主成分分析提取的主成分即为主要风险因子
#
# # 构建风险度量指标
# # 假设这里简单地将主成分加总作为风险度量指标
# risk_measure = np.sum(X_pca, axis=1)
#
# # 结果呈现与分析
# # 将提取的主要风险因子和构建的风险度量指标详细呈现在报告中
#
# # 输出风险度量指标
# print("\n风险度量指标：", risk_measure)
#
# # 分析每个主要风险因子对ESG投资绩效的影响
#
# # 提取主成分对应的特征向量，解释主成分
# component_names = [f"PC{i+1}" for i in range(pca.n_components_)]
# components_df = pd.DataFrame(pca.components_, columns=X.columns, index=component_names)
#
# # 打印主成分对应的特征向量
# print("\n主成分对应的特征向量：")
# print(components_df)

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

# 随机生成ESG评分数据框
esg_data = pd.DataFrame({
    'company_id': range(1, 101),  # 100家公司
    'esg_score': np.random.randint(0, 101, size=100)  # 随机生成0到100的ESG评分
})

# 随机生成行业标准数据框
industry_data = pd.DataFrame({
    'company_id': range(1, 101),  # 100家公司，与ESG评分数据框相同
    'industry_standard': np.random.randint(0, 11, size=100)  # 随机生成0到10的行业标准数据
})

# 打印ESG评分数据框的前5行
print("ESG评分数据框：")
print(esg_data.head())

# 打印行业标准数据框的前5行
print("\n行业标准数据框：")
print(industry_data.head())

# 数据收集与清洗
# 假设已经从各个来源收集到了ESG评分数据和相关行业标准等数据，并存储在数据框中

# 进行数据清洗，处理缺失值等
esg_data_cleaned = esg_data.dropna()
industry_data_cleaned = industry_data.dropna()

# 多变量分析
# 使用主成分分析（PCA）从多种数据中提取主要风险因子

# 合并数据
merged_data = pd.merge(esg_data_cleaned, industry_data_cleaned, on='company_id')

# 提取特征和目标变量
X = merged_data.drop(columns=['company_id', 'esg_score'])
y = merged_data['esg_score']

# 初始化PCA模型
n_components = min(X.shape[0], X.shape[1])  # 确保主成分数量不超过样本数和特征数的较小值
pca = PCA(n_components=n_components)

# 拟合PCA模型并转换数据
X_pca = pca.fit_transform(X)

# 主要风险因子提取
# 主成分分析提取的主成分即为主要风险因子

# 构建风险度量指标
# 假设这里简单地将主成分加总作为风险度量指标
risk_measure = np.sum(X_pca, axis=1)

# 结果呈现与分析
# 将提取的主要风险因子和构建的风险度量指标详细呈现在报告中

# 输出风险度量指标
print("\n风险度量指标：", risk_measure)

# 分析每个主要风险因子对ESG投资绩效的影响

# 提取主成分对应的特征向量，解释主成分
component_names = [f"PC{i+1}" for i in range(pca.n_components_)]
components_df = pd.DataFrame(pca.components_, columns=X.columns, index=component_names)

# 打印主成分对应的特征向量
print("\n主成分对应的特征向量：")
print(components_df)
