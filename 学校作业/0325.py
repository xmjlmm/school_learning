# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import mean_squared_error, r2_score


# -------------------- 数据加载与初步检查 --------------------
def load_and_inspect_data(filepath):
    """加载数据并执行初步检查"""
    df = pd.read_csv(filepath)
    # 过滤无效房价
    df = df[df['median_house_value'] > 0].copy()

    print("数据概览:")
    print(df.info())

    print("\n数值字段统计描述:")
    print(df.describe())

    print("\n缺失值统计:")
    print(df.isnull().sum())

    print("\n前5条数据示例:")
    print(df.head())

    return df


# -------------------- 数据清洗 --------------------
def clean_data(df):
    """执行数据清洗操作"""
    # 处理缺失值
    if df['total_bedrooms'].isnull().sum() > 0:
        df['total_bedrooms'].fillna(df['total_bedrooms'].median(), inplace=True)

    # 删除重复值
    df = df.drop_duplicates()

    # 处理异常值（使用Z - score方法）
    numeric_cols = ['housing_median_age', 'total_rooms', 'total_bedrooms',
                    'population', 'households', 'median_income', 'median_house_value']

    z_scores = np.abs(stats.zscore(df[numeric_cols]))
    df_clean = df[(z_scores < 3).all(axis=1)]

    print(f"\n原始数据量: {len(df)}")
    print(f"清洗后数据量: {len(df_clean)}")
    print(f"移除异常值数量: {len(df) - len(df_clean)}")

    return df_clean


# -------------------- 特征工程 --------------------
def feature_engineering(df):
    """执行特征工程操作"""
    # 创建新特征
    df['rooms_per_household'] = df['total_rooms'] / df['households']
    df['bedrooms_per_room'] = df['total_bedrooms'] / df['total_rooms']
    df['population_per_household'] = df['population'] / df['households']

    # 处理分类变量
    df = pd.get_dummies(df, columns=['ocean_proximity'], prefix='area', drop_first=True)

    # 删除冗余特征
    cols_to_drop = ['total_rooms', 'total_bedrooms', 'population']
    df = df.drop(cols_to_drop, axis=1)

    return df


# -------------------- 相关性分析 --------------------
def analyze_correlation(df, target_col):
    """执行相关性分析并可视化"""
    plt.figure(figsize=(15, 10))
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix,
                annot=True,
                cmap='coolwarm',
                fmt=".2f",
                linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.show()

    # 获取与目标变量相关性最高的特征
    target_corr = corr_matrix[target_col].sort_values(ascending=False)
    print("\n与房价相关性最高的特征:")
    print(target_corr)

    return df


# -------------------- 数据准备 --------------------
def prepare_data(df, target_col):
    """准备最终数据集"""
    # 分离特征和标签
    X = df.drop(target_col, axis=1)
    y = df[target_col].values

    # 对标签进行对数变换（解决右偏分布）
    y = np.log(y)

    # 数据集拆分
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # 特征标准化
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test, scaler


# -------------------- 定义神经网络模型 --------------------
class RobustHousingPredictor(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.LayerNorm(128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 64),
            nn.LayerNorm(64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.net(x)


# -------------------- 训练和评估模型 --------------------
def train_and_evaluate(X_train, X_test, y_train, y_test):
    # 将数据转换为张量
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.FloatTensor(y_test)

    # 创建数据集和数据加载器
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

    # 初始化模型、损失函数和优化器
    input_size = X_train.shape[1]
    model = RobustHousingPredictor(input_size)
    criterion = nn.MSELoss()
    optimizer = optim.AdamW(model.parameters(), lr=1e-5, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CyclicLR(
        optimizer,
        base_lr=1e-6,
        max_lr=1e-4,
        step_size_up=500,
        cycle_momentum=False
    )

    train_losses = []
    test_losses = []
    num_epochs = 1000
    best_loss = float('inf')
    patience = 20
    trigger_times = 0

    # 训练模型
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(inputs).squeeze()
            loss = criterion(outputs, labels)
            loss.backward()
            torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=0.5)
            optimizer.step()
            scheduler.step()
            running_loss += loss.item()

        train_loss = running_loss / len(train_loader)
        train_losses.append(train_loss)

        model.eval()
        test_running_loss = 0.0
        with torch.no_grad():
            for inputs, labels in test_loader:
                outputs = model(inputs).squeeze()
                loss = criterion(outputs, labels)
                test_running_loss += loss.item()
        test_loss = test_running_loss / len(test_loader)
        test_losses.append(test_loss)

        if test_loss < best_loss:
            best_loss = test_loss
            trigger_times = 0
        else:
            trigger_times += 1
            if trigger_times >= patience:
                print("Early Stopping!")
                break

        print(f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}')

    # 评估模型
    model.eval()
    with torch.no_grad():
        y_pred_tensor = model(X_test_tensor).squeeze()
        y_pred = y_pred_tensor.numpy()

    # 逆变换处理（因为对标签做了对数变换）
    y_test_orig = np.exp(y_test)
    y_pred_orig = np.exp(y_pred)

    # 添加异常值过滤
    valid_mask = (y_pred_orig < 1e6) & (y_test_orig < 1e6)
    y_pred_clean = y_pred_orig[valid_mask]
    y_test_clean = y_test_orig[valid_mask]

    # 计算评估指标
    rmse = np.sqrt(mean_squared_error(y_test_clean, y_pred_clean))
    r2 = r2_score(y_test_clean, y_pred_clean)

    print(f"\n最终测试结果：")
    print(f"RMSE: {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")

    # 可视化结果
    plt.figure(figsize=(12, 5))

    # 绘制训练曲线
    plt.subplot(1, 2, 1)
    plt.plot(train_losses, label='Train Loss')
    plt.plot(test_losses, label='Test Loss')
    plt.title('Training History')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # 绘制预测结果
    plt.subplot(1, 2, 2)
    plt.scatter(y_test_clean, y_pred_clean, alpha=0.3)
    plt.plot([y_test_clean.min(), y_test_clean.max()],
             [y_test_clean.min(), y_test_clean.max()], 'r--')
    plt.title('Actual vs Predicted')
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')

    plt.tight_layout()
    plt.show()

    return model


# -------------------- 主流程 --------------------
if __name__ == "__main__":
    # 数据路径
    data_path = 'F:\\PycharmProjects\\pythonProject\\深度学习\\学校作业\\housing\\housing.csv'

    # 完整处理流程
    raw_df = load_and_inspect_data(data_path)  # 数据加载与检查
    cleaned_df = clean_data(raw_df)  # 数据清洗
    feature_df = feature_engineering(cleaned_df)  # 特征工程
    final_df = analyze_correlation(feature_df, 'median_house_value')  # 相关性分析

    # 准备训练数据
    X_train, X_test, y_train, y_test, scaler = prepare_data(final_df, 'median_house_value')

    # 训练并评估模型
    model = train_and_evaluate(X_train, X_test, y_train, y_test)
    