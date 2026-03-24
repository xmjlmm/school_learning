# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
#
# # 数据收集与清洗
# # 假设已经从各个来源收集到了企业的ESG评分数据和财务绩效数据，并存储在数据框中
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
# # 假设esg_data是ESG评分数据框，financial_data是财务绩效数据框
# # 进行数据清洗，处理缺失值等
# esg_data_cleaned = esg_data.dropna()
# financial_data_cleaned = financial_data.dropna()
#
# # 合并数据
# merged_data = pd.merge(esg_data_cleaned, financial_data_cleaned, on='company_id')
#
# # 相关性分析
# # 对ESG评分数据和财务绩效数据进行相关性分析
# correlation_matrix = merged_data.corr()
#
# # 可视化相关性矩阵
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
# plt.title('ESG评分与财务绩效相关性矩阵')
# plt.show()
#
# # 变量选择与特征工程
# # 假设选择与财务绩效指标相关性较高的ESG评分指标作为自变量
# # 在实际情况中，可以根据业务背景和统计分析结果进行选择
# selected_features = ['esg_score', 'esg_factor1', 'esg_factor2']  # 选择了三个ESG评分指标
#
# # 提取特征和目标变量
# X = merged_data[selected_features]
# y = merged_data['financial_performance_metric']
#
# # 拆分数据集为训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # 回归分析建模
# # 使用线性回归模型建立ESG评分与财务绩效之间的关系模型
# model = LinearRegression()
# model.fit(X_train, y_train)
#
# # 模型评估
# # 在测试集上进行预测并评估模型性能
# y_pred = model.predict(X_test)
# mse = mean_squared_error(y_test, y_pred)
#
# # 输出模型评估结果
# print("模型评估结果：")
# print("均方误差 (MSE):", mse)
#
# # 解释模型系数
# # 探讨每个ESG评分指标对财务绩效的影响程度和方向
# coefficients = pd.DataFrame({'Feature': selected_features, 'Coefficient': model.coef_})
# print("\n模型系数：")
# print(coefficients)
#
# # 结果呈现与分析
# # 将建模过程和结果详细呈现在报告中
#
# # 可以进一步分析模型残差、模型的拟合优度等，并将结果详细记录在报告中



import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from matplotlib.font_manager import FontProperties
import matplotlib

font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)

matplotlib.rcParams["font.family"] = "Times New Roman"

# 生成随机的ESG评分数据和财务绩效数据
np.random.seed(0)  # 设置随机种子以确保可复现性

# 假设有100家公司，每家公司有3个ESG评分指标和1个财务绩效指标
num_companies = 100
esg_scores = np.random.uniform(low=0, high=100, size=(num_companies, 3))  # 生成ESG评分数据
financial_performance = np.random.uniform(low=0, high=100, size=num_companies)  # 生成财务绩效数据

# 创建数据框
esg_data = pd.DataFrame(esg_scores, columns=['esg_score', 'esg_factor1', 'esg_factor2'])
financial_data = pd.DataFrame({'financial_performance_metric': financial_performance})

# 假设数据中存在缺失值
# 随机将一部分数据设为缺失值
esg_data.iloc[::10, :] = np.nan
financial_data.iloc[::10, :] = np.nan

# 随机生成行业标准数据框
industry_data = pd.DataFrame({
    'company_id': range(1, num_companies + 1),  # 100家公司，与ESG评分数据框相同
    'industry_standard': np.random.randint(0, 11, size=num_companies)  # 随机生成0到10的行业标准数据
})

# 数据清洗
esg_data_cleaned = esg_data.dropna()
financial_data_cleaned = financial_data.dropna()

# 合并数据
merged_data = pd.merge(esg_data_cleaned, financial_data_cleaned, left_index=True, right_index=True)

# 相关性分析
correlation_matrix = merged_data.corr()

# 可视化相关性矩阵
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('ESG评分与财务绩效相关性矩阵')
plt.show()

# 变量选择与特征工程
selected_features = ['esg_score', 'esg_factor1', 'esg_factor2']
X = merged_data[selected_features]
y = merged_data['financial_performance_metric']

# 拆分数据集为训练集和测试集
if len(X) > 0 and len(y) > 0:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 回归分析建模
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 模型评估
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    # 输出模型评估结果
    print("模型评估结果：")
    print("均方误差 (MSE):", mse)

    # 解释模型系数
    coefficients = pd.DataFrame({'Feature': selected_features, 'Coefficient': model.coef_})
    print("\n模型系数：")
    print(coefficients)
else:
    print("数据集为空，无法进行拆分和建模。")



'''
# 首先，我们计算指标与ESG评分之间的相关系数，并生成热力图进行可视化。
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('data1.csv')  

# 计算相关性矩阵
correlation_matrix = data.corr()

# 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap between ESG and Financial Performance Indicators')
plt.show()

# 我们对数据进行清洗，处理缺失值和异常值。
# 处理缺失值
data_cleaned = data.dropna()

# 使用支持向量机进行回归分析
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 分割数据集为自变量和因变量
X = data_cleaned.drop(columns=['ESG_score'])  # 自变量
y = data_cleaned['ESG_score']  # 因变量

# 将数据集划分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化处理
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score

# 训练SVR模型
svr = SVR(kernel='rbf')  # 使用径向基核
svr.fit(X_train_scaled, y_train)

# 预测测试集
y_pred = svr.predict(X_test_scaled)

# 评估模型性能
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error (MSE):", mse)
print("R-squared (R2):", r2)

'''


