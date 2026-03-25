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
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
from datetime import datetime
# import wandb

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

    # 处理异常值（使用Z-score方法）
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
    plt.tight_layout()
    plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
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
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X_train.index, X_test.index

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

# -------------------- 可视化训练过程 --------------------
def plot_training_history(train_losses, test_losses):
    """绘制训练和测试损失曲线"""
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(train_losses, label='Training Loss', color='blue', alpha=0.7)
    plt.plot(test_losses, label='Test Loss', color='red', alpha=0.7)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Test Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    # 只显示最后100个epoch的损失，以便更清晰地观察收敛情况
    n_epochs = len(train_losses)
    start_idx = max(0, n_epochs - 100)
    plt.plot(range(start_idx, n_epochs), train_losses[start_idx:], 
             label='Training Loss', color='blue', alpha=0.7)
    plt.plot(range(start_idx, n_epochs), test_losses[start_idx:], 
             label='Test Loss', color='red', alpha=0.7)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Loss (Last 100 Epochs)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
    plt.show()

# -------------------- 预测结果可视化 --------------------
def plot_predictions(y_true, y_pred, model_name="Neural Network"):
    """绘制预测结果对比图"""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # 计算误差
    errors = y_pred - y_true
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. 预测值 vs 真实值散点图
    axes[0, 0].scatter(y_true, y_pred, alpha=0.6, color='blue')
    max_val = max(y_true.max(), y_pred.max())
    min_val = min(y_true.min(), y_pred.min())
    axes[0, 0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
    axes[0, 0].set_xlabel('True Values')
    axes[0, 0].set_ylabel('Predictions')
    axes[0, 0].set_title(f'{model_name} - Predictions vs True Values\nR² = {r2:.4f}')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. 误差分布直方图
    axes[0, 1].hist(errors, bins=50, alpha=0.7, color='green', edgecolor='black')
    axes[0, 1].axvline(x=0, color='red', linestyle='--', linewidth=2)
    axes[0, 1].set_xlabel('Prediction Error')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title(f'Error Distribution\nMAE = {mae:.2f}, RMSE = {rmse:.2f}')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. 残差图
    axes[1, 0].scatter(y_pred, errors, alpha=0.6, color='orange')
    axes[1, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
    axes[1, 0].set_xlabel('Predictions')
    axes[1, 0].set_ylabel('Residuals')
    axes[1, 0].set_title('Residual Plot')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. 预测值和真实值随时间/样本的变化
    sample_indices = range(len(y_true))
    axes[1, 1].plot(sample_indices, y_true, 'o-', alpha=0.7, label='True Values', markersize=3)
    axes[1, 1].plot(sample_indices, y_pred, 'o-', alpha=0.7, label='Predictions', markersize=3)
    axes[1, 1].set_xlabel('Sample Index')
    axes[1, 1].set_ylabel('Price')
    axes[1, 1].set_title('True vs Predicted Values (by Sample)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('prediction_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return rmse, r2, mae

# -------------------- 特征重要性分析 --------------------
def analyze_feature_importance(model, feature_names, X_test):
    """分析神经网络的特征重要性"""
    # 使用梯度信息估计特征重要性
    X_test_tensor = torch.FloatTensor(X_test)
    X_test_tensor.requires_grad = True
    
    model.eval()
    output = model(X_test_tensor)
    
    # 计算梯度
    gradient = torch.autograd.grad(outputs=output, inputs=X_test_tensor,
                                 grad_outputs=torch.ones_like(output),
                                 create_graph=False)[0]
    
    # 计算平均梯度绝对值作为特征重要性
    feature_importance = torch.mean(torch.abs(gradient), dim=0).detach().numpy()
    
    # 创建特征重要性DataFrame
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': feature_importance
    }).sort_values('Importance', ascending=False)
    
    # 绘制特征重要性图
    plt.figure(figsize=(10, 8))
    sns.barplot(data=importance_df, x='Importance', y='Feature', palette='viridis')
    plt.title('Feature Importance Analysis (Gradient-based)')
    plt.xlabel('Importance Score')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n特征重要性排名:")
    print(importance_df)
    
    return importance_df

# -------------------- 模型保存与加载 --------------------
def save_model(model, scaler, feature_names, metrics, model_dir='saved_models'):
    """保存模型和相关配置"""
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存模型权重
    model_path = os.path.join(model_dir, f'housing_model_{timestamp}.pth')
    torch.save(model.state_dict(), model_path)
    
    # 保存scaler
    scaler_path = os.path.join(model_dir, f'scaler_{timestamp}.pkl')
    joblib.dump(scaler, scaler_path)
    
    # 保存特征名称
    feature_path = os.path.join(model_dir, f'feature_names_{timestamp}.pkl')
    joblib.dump(feature_names, feature_path)
    
    # 保存评估指标
    metrics_path = os.path.join(model_dir, f'metrics_{timestamp}.txt')
    with open(metrics_path, 'w') as f:
        f.write(f"模型评估指标 (保存时间: {timestamp})\n")
        f.write("="*50 + "\n")
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    
    print(f"\n模型已保存到: {model_path}")
    print(f"Scaler已保存到: {scaler_path}")
    print(f"特征名称已保存到: {feature_path}")
    print(f"评估指标已保存到: {metrics_path}")
    
    return model_path, scaler_path

def load_model(model_path, scaler_path, feature_path, input_size):
    """加载模型和相关配置"""
    # 加载模型
    model = RobustHousingPredictor(input_size)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    
    # 加载scaler和特征名称
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(feature_path)
    
    return model, scaler, feature_names

# -------------------- 预测新数据 --------------------
def predict_new_data(model, scaler, new_data, feature_names):
    """使用训练好的模型预测新数据"""
    # 确保新数据包含所有必要的特征
    missing_features = set(feature_names) - set(new_data.columns)
    if missing_features:
        raise ValueError(f"缺少以下特征: {missing_features}")
    
    # 按正确的特征顺序排列数据
    new_data = new_data[feature_names]
    
    # 数据预处理
    new_data_scaled = scaler.transform(new_data)
    new_data_tensor = torch.FloatTensor(new_data_scaled)
    
    # 预测
    model.eval()
    with torch.no_grad():
        predictions_log = model(new_data_tensor).squeeze().numpy()
    
    # 逆变换（因为训练时对标签做了对数变换）
    predictions = np.exp(predictions_log)
    
    return predictions

# -------------------- 训练和评估模型 --------------------
def train_and_evaluate(X_train, X_test, y_train, y_test, feature_names):
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
        base_lr=1e-5,
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
            # 保存最佳模型
            torch.save(model.state_dict(), 'best_model.pth')
        else:
            trigger_times += 1
            if trigger_times >= patience:
                print("Early Stopping!")
                # 加载最佳模型
                model.load_state_dict(torch.load('best_model.pth'))
                break

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}')

    # 绘制训练历史
    plot_training_history(train_losses, test_losses)

    # 评估模型
    model.eval()
    with torch.no_grad():
        y_pred_tensor = model(X_test_tensor).squeeze()
        y_pred_log = y_pred_tensor.numpy()

    # 逆变换处理（因为对标签做了对数变换）
    y_test_orig = np.exp(y_test)
    y_pred_orig = np.exp(y_pred_log)

    # 添加异常值过滤
    valid_mask = (y_pred_orig < 1e6) & (y_test_orig < 1e6)
    y_pred_clean = y_pred_orig[valid_mask]
    y_test_clean = y_test_orig[valid_mask]

    # 计算评估指标
    rmse = np.sqrt(mean_squared_error(y_test_clean, y_pred_clean))
    r2 = r2_score(y_test_clean, y_pred_clean)
    mae = mean_absolute_error(y_test_clean, y_pred_clean)

    print(f"\n最终测试结果：")
    print(f"RMSE: {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")
    print(f"MAE: {mae:.2f}")

    # 绘制预测结果
    rmse_final, r2_final, mae_final = plot_predictions(y_test_clean, y_pred_clean)
    
    # 分析特征重要性
    importance_df = analyze_feature_importance(model, feature_names, X_test)
    
    metrics = {
        'RMSE': rmse_final,
        'R2_Score': r2_final,
        'MAE': mae_final,
        'Best_Epoch': epoch + 1 - patience if trigger_times >= patience else epoch + 1
    }
    
    return model, metrics, train_losses, test_losses

# -------------------- 主流程 --------------------
if __name__ == "__main__":
    # 数据路径
    data_path = 'F:\\PycharmProjects\\pythonProject\\housing\\housing.csv'

    # 完整处理流程
    print("=== 开始房屋价格预测项目 ===")
    
    # 1. 数据加载与检查
    print("\n1. 数据加载与检查...")
    raw_df = load_and_inspect_data(data_path)
    
    # 2. 数据清洗
    print("\n2. 数据清洗...")
    cleaned_df = clean_data(raw_df)
    
    # 3. 特征工程
    print("\n3. 特征工程...")
    feature_df = feature_engineering(cleaned_df)
    
    # 4. 相关性分析
    print("\n4. 相关性分析...")
    final_df = analyze_correlation(feature_df, 'median_house_value')
    
    # 5. 准备训练数据
    print("\n5. 准备训练数据...")
    X_train, X_test, y_train, y_test, scaler, train_idx, test_idx = prepare_data(
        final_df, 'median_house_value'
    )
    
    # 获取特征名称
    feature_names = final_df.drop('median_house_value', axis=1).columns.tolist()
    print(f"\n使用的特征数量: {len(feature_names)}")
    print("特征列表:", feature_names)
    
    # 6. 训练并评估模型
    print("\n6. 训练并评估模型...")
    model, metrics, train_losses, test_losses = train_and_evaluate(
        X_train, X_test, y_train, y_test, feature_names
    )
    
    # 7. 保存模型
    print("\n7. 保存模型...")
    model_path, scaler_path = save_model(model, scaler, feature_names, metrics)
    
    # 8. 示例：预测新数据
    print("\n8. 示例预测...")
    
    # 使用测试集中的一个样本作为示例
    sample_idx = 0
    sample_data = final_df.drop('median_house_value', axis=1).iloc[test_idx].iloc[sample_idx:sample_idx+1]
    
    try:
        predicted_price = predict_new_data(model, scaler, sample_data, feature_names)
        actual_price = final_df['median_house_value'].iloc[test_idx].iloc[sample_idx]
        
        print(f"\n示例预测结果:")
        print(f"预测价格: ${predicted_price[0]:.2f}")
        print(f"实际价格: ${actual_price:.2f}")
        print(f"预测误差: ${abs(predicted_price[0] - actual_price):.2f}")
        print(f"相对误差: {abs(predicted_price[0] - actual_price) / actual_price * 100:.2f}%")
        
    except Exception as e:
        print(f"预测过程中出现错误: {e}")
    
    print("\n=== 项目完成 ===")
    print("\n生成的文件:")
    print("- correlation_matrix.png: 特征相关性热力图")
    print("- training_history.png: 训练过程损失曲线")
    print("- prediction_analysis.png: 预测结果分析图")
    print("- feature_importance.png: 特征重要性分析图")
    print("- saved_models/: 保存的模型文件目录")