import pandas as pd

# 加载数据
file_path = "D://数模//美赛//排位赛//中文版.xlsx"
data = pd.read_excel(file_path)

# 数据清洗
# 删除无效或缺失的数据行
data.dropna(inplace=True)

# 格式化日期
data['日期'] = pd.to_datetime(data['日期'])

# 数值化分类数据（例如，活动类型）
activity_encoded = pd.get_dummies(data['活动'])
data = pd.concat([data, activity_encoded], axis=1)

# 处理缺失值
# 假设我们用平均值填充缺失的海拔数据
data['起始区域海拔'].fillna(data['起始区域海拔'].mean(), inplace=True)

# 数据标准化
# 假设我们需要标准化海拔数据
data['起始区域海拔'] = (data['起始区域海拔'] - data['起始区域海拔'].mean()) / data['起始区域海拔'].std()

# 特征工程
# 创建新的特征或转换现有特征（这里仅为示例）
data['高海拔'] = data['起始区域海拔'] > data['起始区域海拔'].median()

# 结果展示
print(data.head())
