import xalpha as xa
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.dates as mdates
from datetime import timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

def create_simplified_indicators(df):
    """创建简化的技术指标 - 避免过度特征工程"""
    df = df.copy()
    
    # 基础价格变化
    df['price_change'] = df['netvalue'].diff()
    df['price_pct_change'] = df['netvalue'].pct_change()
    
    # 只保留最关键的移动平均线
    df['MA_5'] = df['netvalue'].rolling(window=5).mean()
    df['MA_10'] = df['netvalue'].rolling(window=10).mean()
    
    # 价格动量（简化）
    df['momentum_3'] = df['netvalue'] - df['netvalue'].shift(3)
    
    # 波动率指标
    df['volatility_5'] = df['price_pct_change'].rolling(window=5).std()
    
    # 相对位置指标
    df['price_ratio_MA5'] = df['netvalue'] / df['MA_5']
    
    return df

def prepare_robust_features(df, lookback_days=7):
    """准备稳健的机器学习特征"""
    df = df.copy()
    
    # 创建技术指标
    df = create_simplified_indicators(df)
    
    # 有限的滞后特征（防止过度参数化）
    max_lags = min(lookback_days, len(df) // 5)  # 更保守的滞后数量
    for i in range(1, max_lags + 1):
        df[f'lag_{i}'] = df['netvalue'].shift(i)
    
    # 目标变量：未来1天的净值
    forecast_days = 1
    df['target'] = df['netvalue'].shift(-forecast_days)
    
    # 删除包含NaN的行并重置索引（关键修复）
    df_clean = df.dropna().reset_index(drop=True)
    
    if len(df_clean) == 0:
        return pd.DataFrame(), []
    
    # 特征列（排除目标列和日期列）
    feature_columns = [col for col in df_clean.columns 
                      if col not in ['target', 'date', 'netvalue'] 
                      and not df_clean[col].isnull().any()]
    
    # 如果特征仍然太多，进行相关性筛选
    if len(feature_columns) > 5:  # 进一步减少特征数量
        X_temp = df_clean[feature_columns]
        y_temp = df_clean['target']
        correlations = X_temp.apply(lambda x: x.corr(y_temp))
        # 选择与目标变量相关性最高的5个特征
        top_features = correlations.abs().nlargest(5).index.tolist()
        feature_columns = top_features
    
    return df_clean, feature_columns

def safe_index_access(df, indices, column='date'):
    """安全索引访问函数 - 修复索引越界问题"""
    try:
        # 使用loc而不是iloc，因为loc基于标签索引
        return df.loc[indices, column]
    except (IndexError, KeyError) as e:
        print(f"索引访问警告: {e}")
        # 找出有效的索引
        valid_indices = [idx for idx in indices if idx in df.index]
        if valid_indices:
            print(f"使用有效索引范围: {min(valid_indices)} 到 {max(valid_indices)}")
            return df.loc[valid_indices, column]
        else:
            print("没有有效的索引可用")
            return pd.Series([], name=column)

def train_conservative_model(X, y, test_size=0.3):
    """训练保守的随机森林模型（防止过拟合）"""
    # 按时间顺序分割（金融数据的重要原则）
    split_idx = int(len(X) * (1 - test_size))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    print(f"训练集大小: {len(X_train)}, 测试集大小: {len(X_test)}")
    
    if len(X_train) == 0 or len(X_test) == 0:
        raise ValueError("训练集或测试集为空，请调整test_size参数")
    
    # 标准化特征
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 使用更保守的模型参数（针对小数据集）
    model = RandomForestRegressor(
        n_estimators=30,    # 进一步减少树的数量
        max_depth=3,        # 限制树深度
        min_samples_split=10, # 增加分裂所需样本数
        min_samples_leaf=5,  # 增加叶节点样本数
        max_features=0.8,    # 限制每棵树使用的特征比例
        random_state=42,
        n_jobs=-1
    )
    
    # 训练模型
    model.fit(X_train_scaled, y_train)
    
    # 预测
    y_pred = model.predict(X_test_scaled)
    
    return model, scaler, X_test, y_test, y_pred, X_train.index, X_test.index

def calculate_realistic_metrics(y_true, y_pred):
    """计算现实的模型评估指标"""
    if len(y_true) == 0 or len(y_pred) == 0:
        return {'Error': '没有有效数据用于评估'}
    
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    # 方向准确性（需要至少2个点）
    if len(y_true) > 1:
        actual_direction = np.sign(np.diff(y_true))
        pred_direction = np.sign(np.diff(y_pred))
        direction_accuracy = np.mean(actual_direction == pred_direction)
    else:
        direction_accuracy = 0.0
    
    # 与简单基准比较（使用前一天的净值作为预测）
    baseline_pred = np.roll(y_true, 1)
    if len(y_true) > 1:
        baseline_pred[0] = y_true[0]  # 第一个元素特殊处理
        baseline_mae = mean_absolute_error(y_true[1:], baseline_pred[1:])
        improvement = (baseline_mae - mae) / baseline_mae * 100 if baseline_mae > 0 else 0
    else:
        improvement = 0
    
    return {
        'MAE': mae,
        'RMSE': rmse,
        'R2_score': r2,
        'Direction_Accuracy': direction_accuracy,
        'Improvement_Over_Naive_%': improvement
    }

def plot_simple_results(dates, y_true, y_pred, title):
    """绘制简化的结果图"""
    if len(dates) == 0:
        print("没有数据可绘制")
        return
        
    plt.figure(figsize=(12, 8))
    
    # 主图：实际值 vs 预测值
    plt.subplot(2, 1, 1)
    plt.plot(dates, y_true, 'b-', label='实际净值', linewidth=2, marker='o', markersize=4)
    plt.plot(dates, y_pred, 'r--', label='预测净值', linewidth=2, marker='s', markersize=4)
    plt.title(f'{title} - 净值预测对比', fontsize=14)
    plt.ylabel('净值')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # 误差分布
    plt.subplot(2, 1, 2)
    errors = y_true - y_pred
    plt.bar(range(len(errors)), errors, alpha=0.7, color='orange')
    plt.axhline(y=0, color='red', linestyle='-')
    plt.title('预测误差分布')
    plt.ylabel('误差值')
    plt.xlabel('样本序号')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def predict_next_week(df_clean):
    """预测未来一周（2025年10月1日至10月7日）的基金净值"""
    if len(df_clean) < 5:
        print("数据不足，无法进行未来预测")
        return
    
    # 获取最后一天的日期和净值
    last_date = df_clean['date'].iloc[-1]
    last_value = df_clean['netvalue'].iloc[-1]
    
    print(f"\n最后已知净值日期: {last_date.strftime('%Y-%m-%d')}, 净值: {last_value:.4f}")
    
    # 计算预测起始日期（下一个交易日）
    # 基金通常在交易日更新净值，所以我们需要跳过周末
    # 假设2025年10月1日是周三（实际需要根据日历确认）
    next_trading_day = last_date + timedelta(days=1)  # 2025-10-01
    
    # 预测未来7天（包括周末，但基金净值只在交易日更新）
    # 我们需要预测交易日的数据
    trading_days = []
    current_date = next_trading_day
    for _ in range(7):  # 预测一周
        # 跳过周末（周六和周日）
        while current_date.weekday() >= 5:  # 5=周六, 6=周日
            current_date += timedelta(days=1)
        
        trading_days.append(current_date)
        current_date += timedelta(days=1)
    
    # 使用更稳健的预测方法
    # 计算近期趋势（使用过去5个交易日的平均变化率）
    recent_changes = df_clean['netvalue'].pct_change().tail(5).dropna()
    if len(recent_changes) > 0:
        recent_trend = recent_changes.mean()
        # 过滤异常大的趋势值
        if abs(recent_trend) > 0.05:  # 如果日变化超过5%，视为异常
            recent_trend = 0.0
    else:
        recent_trend = 0.0
    
    print(f"\n基于近期趋势 ({recent_trend:.4%}) 预测未来一周净值:")
    
    # 生成预测
    future_predictions = []
    current_value = last_value
    
    for i, date in enumerate(trading_days):
        # 应用趋势预测
        next_value = current_value * (1 + recent_trend)
        future_predictions.append(next_value)
        current_value = next_value
        
        # 打印每日预测
        weekday = ['周一', '周二', '周三', '周四', '周五'][date.weekday()]
        print(f"{date.strftime('%Y-%m-%d')} ({weekday}): {next_value:.4f}")
    
    # 绘制未来预测
    plt.figure(figsize=(12, 6))
    
    # 绘制历史数据（最后20个交易日）
    historical_dates = df_clean['date'].tail(20)
    historical_values = df_clean['netvalue'].tail(20)
    plt.plot(historical_dates, historical_values, 'b-', label='历史净值', linewidth=2)
    
    # 绘制预测数据
    plt.plot(trading_days, future_predictions, 'ro--', label='预测净值', linewidth=2, markersize=8)
    
    # 标记预测起始点
    plt.plot([last_date], [last_value], 'go', markersize=10, label='最后已知值')
    
    plt.title('华夏人工智能ETF联接D(021580) - 未来一周预测', fontsize=16)
    plt.xlabel('日期')
    plt.ylabel('净值')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 设置日期格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

# 主程序
def main():
    try:
        print("开始基金预测分析（修复版本）...")
        
        # 获取基金数据
        zzyl = xa.fundinfo('021580')
        
        # 筛选日期范围内的数据
        start_date = '2025-06-30'
        end_date = '2025-10-30'
        filtered_data = zzyl.price[(zzyl.price['date'] >= start_date) & 
                                   (zzyl.price['date'] <= end_date)].copy()
        
        print("=" * 50)
        print("数据基本信息:")
        print(f"数据时间段: {filtered_data['date'].min()} 至 {filtered_data['date'].max()}")
        print(f"总数据点数: {len(filtered_data)}")
        
        # 准备特征数据
        df_clean, feature_columns = prepare_robust_features(filtered_data)
        
        if len(df_clean) == 0:
            print("错误: 数据清洗后无有效数据")
            return
        
        print(f"有效特征数量: {len(feature_columns)}")
        print(f"有效样本数: {len(df_clean)}")
        print("使用的特征:", feature_columns)
        
        if len(df_clean) < 15:  # 提高最小数据量要求
            print("警告: 数据量过少，建议获取更多历史数据")
            # 即使数据少也继续，但使用更简单的模型
            
        # 准备特征和目标变量
        X = df_clean[feature_columns]
        y = df_clean['target']
        
        # 训练保守模型
        model, scaler, X_test, y_test, y_pred, train_indices, test_indices = train_conservative_model(X, y)
        
        # 计算模型指标
        metrics = calculate_realistic_metrics(y_test.values, y_pred)
        
        print("=" * 50)
        print("模型评估结果:")
        for metric, value in metrics.items():
            if isinstance(value, float):
                print(f"{metric}: {value:.4f}")
            else:
                print(f"{metric}: {value}")
        
        # 修复：使用安全的索引访问方法
        test_dates = safe_index_access(df_clean, test_indices, 'date')
        
        # 确保数据对齐
        if len(test_dates) != len(y_test):
            print(f"数据对齐警告: 日期数({len(test_dates)}) ≠ 测试集数({len(y_test)})")
            # 使用索引交集
            common_indices = test_indices.intersection(df_clean.index)
            if len(common_indices) > 0:
                test_dates = df_clean.loc[common_indices, 'date']
                y_test = y_test.loc[common_indices]
                y_pred = y_pred[:len(y_test)]  # 调整预测值长度
            else:
                print("错误: 没有共同索引，无法绘制图表")
                return
        
        # 绘制结果
        if len(test_dates) > 0:
            plot_simple_results(test_dates.values, y_test.values, y_pred, 
                              "华夏人工智能ETF联接D(021580)")
        else:
            print("没有有效的数据用于绘图")
        
        # 特征重要性分析
        if len(feature_columns) > 0:
            feature_importance = pd.DataFrame({
                'feature': feature_columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\n特征重要性排名:")
            print(feature_importance.head(10))
            
            # 绘制特征重要性图
            plt.figure(figsize=(8, 6))
            plt.barh(feature_importance['feature'], feature_importance['importance'])
            plt.xlabel('重要性')
            plt.title('特征重要性排名')
            plt.tight_layout()
            plt.show()
        
        # 预测未来一周（2025年10月1日至10月7日）
        predict_next_week(df_clean)
        
        print("\n分析完成! 建议获取更多历史数据以提高模型可靠性。")
        
    except Exception as e:
        print(f"程序执行错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()