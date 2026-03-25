
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# -------------------- 传统机器学习模型预测 --------------------
def traditional_ml_prediction(X_train, X_test, y_train, y_test, feature_names):
    """使用多种传统机器学习方法进行房价预测"""
    
    # 定义要比较的模型
    models = {
        '线性回归': LinearRegression(),
        '岭回归': Ridge(alpha=1.0),
        'Lasso回归': Lasso(alpha=0.1),
        '随机森林': RandomForestRegressor(n_estimators=100, random_state=42),
        '梯度提升': GradientBoostingRegressor(n_estimators=100, random_state=42),
        '支持向量机': SVR(kernel='rbf', C=1.0)
    }
    
    # 存储结果
    results = {}
    predictions = {}
    
    print("开始传统机器学习模型训练...")
    print("=" * 60)
    
    for name, model in models.items():
        print(f"训练 {name} 模型...")
        
        # 训练模型
        model.fit(X_train, y_train)
        
        # 预测
        y_pred_log = model.predict(X_test)
        
        # 逆变换（因为对标签做了对数变换）
        y_pred = np.exp(y_pred_log)
        y_true = np.exp(y_test)
        
        # 计算评估指标
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        
        # 交叉验证
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
        cv_rmse = np.sqrt(-cv_scores.mean())
        
        results[name] = {
            'RMSE': rmse,
            'R2': r2,
            'MAE': mae,
            'CV_RMSE': cv_rmse
        }
        
        predictions[name] = y_pred
        
        print(f"{name} - RMSE: {rmse:.2f}, R²: {r2:.4f}, MAE: {mae:.2f}")
        print(f"交叉验证RMSE: {cv_rmse:.2f}")
        print("-" * 40)
    
    return results, predictions, models

# -------------------- 模型对比可视化 --------------------
def compare_models_visualization(ml_results, dl_results, ml_predictions, dl_predictions, y_test):
    """可视化对比传统机器学习与深度学习模型效果"""
    
    # 准备数据
    y_true = np.exp(y_test)
    
    # 1. 模型性能对比柱状图
    fig, axes = plt.subplots(2, 2, figsize=(20, 15))
    
    # RMSE对比
    ml_rmse = [ml_results[name]['RMSE'] for name in ml_results]
    ml_names = list(ml_results.keys())
    
    axes[0, 0].bar(ml_names, ml_rmse, alpha=0.7, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'])
    axes[0, 0].axhline(y=dl_results['RMSE'], color='red', linestyle='--', linewidth=2, label=f'深度学习模型: {dl_results["RMSE"]:.2f}')
    axes[0, 0].set_title('模型RMSE对比', fontsize=14)
    axes[0, 0].set_ylabel('RMSE')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # R²对比
    ml_r2 = [ml_results[name]['R2'] for name in ml_results]
    
    axes[0, 1].bar(ml_names, ml_r2, alpha=0.7, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'])
    axes[0, 1].axhline(y=dl_results['R2_Score'], color='red', linestyle='--', linewidth=2, label=f'深度学习模型: {dl_results["R2_Score"]:.4f}')
    axes[0, 1].set_title('模型R²分数对比', fontsize=14)
    axes[0, 1].set_ylabel('R² Score')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 2. 预测值对比散点图（选择最佳传统模型 vs 深度学习）
    best_ml_name = min(ml_results, key=lambda x: ml_results[x]['RMSE'])
    best_ml_pred = ml_predictions[best_ml_name]
    
    axes[1, 0].scatter(y_true, best_ml_pred, alpha=0.6, label=f'最佳传统模型 ({best_ml_name})', color='blue')
    axes[1, 0].scatter(y_true, dl_predictions, alpha=0.6, label='深度学习模型', color='red')
    max_val = max(y_true.max(), best_ml_pred.max(), dl_predictions.max())
    axes[1, 0].plot([0, max_val], [0, max_val], 'k--', lw=2)
    axes[1, 0].set_xlabel('真实房价')
    axes[1, 0].set_ylabel('预测房价')
    axes[1, 0].set_title('最佳传统模型 vs 深度学习模型预测对比')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 3. 误差分布对比
    ml_errors = best_ml_pred - y_true
    dl_errors = dl_predictions - y_true
    
    axes[1, 1].hist(ml_errors, bins=50, alpha=0.7, label=f'{best_ml_name}', color='blue')
    axes[1, 1].hist(dl_errors, bins=50, alpha=0.7, label='深度学习', color='red')
    axes[1, 1].axvline(x=0, color='black', linestyle='--', linewidth=2)
    axes[1, 1].set_xlabel('预测误差')
    axes[1, 1].set_ylabel('频次')
    axes[1, 1].set_title('预测误差分布对比')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 4. 训练时间对比（需要实际测量）
    print("\n模型性能总结:")
    print("=" * 60)
    print(f"{'模型名称':<15} {'RMSE':<10} {'R² Score':<12} {'MAE':<10} {'CV RMSE':<10}")
    print("-" * 60)
    
    for name in ml_results:
        print(f"{name:<15} {ml_results[name]['RMSE']:<10.2f} {ml_results[name]['R2']:<12.4f} "
              f"{ml_results[name]['MAE']:<10.2f} {ml_results[name]['CV_RMSE']:<10.2f}")
    
    print(f"{'深度学习':<15} {dl_results['RMSE']:<10.2f} {dl_results['R2_Score']:<12.4f} "
          f"{dl_results['MAE']:<10.2f} {'N/A':<10}")
    print("=" * 60)

# -------------------- 特征重要性分析（随机森林） --------------------
def analyze_traditional_feature_importance(model, feature_names, X_train, y_train):
    """分析传统模型的特征重要性"""
    
    if hasattr(model, 'feature_importances_'):
        # 训练模型获取特征重要性
        model.fit(X_train, y_train)
        importances = model.feature_importances_
        
        # 创建特征重要性DataFrame
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        # 绘制特征重要性图
        plt.figure(figsize=(12, 8))
        sns.barplot(data=importance_df.head(15), x='Importance', y='Feature', palette='viridis')
        plt.title('传统模型特征重要性分析（随机森林）')
        plt.xlabel('重要性分数')
        plt.tight_layout()
        plt.savefig('traditional_feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("\n传统模型特征重要性排名（前10）:")
        print(importance_df.head(10))
        
        return importance_df
    else:
        print("该模型不支持特征重要性分析")
        return None

# -------------------- 超参数调优 --------------------
def hyperparameter_tuning(X_train, y_train):
    """对最佳传统模型进行超参数调优"""
    
    print("\n开始超参数调优...")
    
    # 定义参数网格
    param_grids = {
        '随机森林': {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5]
        },
        '梯度提升': {
            'n_estimators': [100, 200],
            'learning_rate': [0.05, 0.1],
            'max_depth': [3, 5]
        }
    }
    
    best_models = {}
    
    for model_name, param_grid in param_grids.items():
        print(f"调优 {model_name}...")
        
        if model_name == '随机森林':
            model = RandomForestRegressor(random_state=42)
        else:
            model = GradientBoostingRegressor(random_state=42)
        
        # 网格搜索
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        
        best_models[model_name] = {
            'model': grid_search.best_estimator_,
            'params': grid_search.best_params_,
            'score': np.sqrt(-grid_search.best_score_)
        }
        
        print(f"最佳参数: {grid_search.best_params_}")
        print(f"最佳分数: {np.sqrt(-grid_search.best_score_):.2f}")
    
    return best_models

# -------------------- 主流程 --------------------
def main():
    # 数据路径
    data_path = ''F:\\PycharmProjects\\pythonProject\\housing\\housing.csv''
    
    print("=== 传统机器学习方法房价预测 ===")
    
    # 1. 数据加载与检查
    print("\n1. 数据加载与检查...")
    raw_df = pd.read_csv(data_path)
    raw_df = raw_df[raw_df['median_house_value'] > 0].copy()
    
    # 2. 数据清洗
    print("\n2. 数据清洗...")
    # 处理缺失值
    if raw_df['total_bedrooms'].isnull().sum() > 0:
        raw_df['total_bedrooms'].fillna(raw_df['total_bedrooms'].median(), inplace=True)
    
    # 删除重复值
    raw_df = raw_df.drop_duplicates()
    
    # 处理异常值
    numeric_cols = ['housing_median_age', 'total_rooms', 'total_bedrooms',
                    'population', 'households', 'median_income', 'median_house_value']
    z_scores = np.abs(stats.zscore(raw_df[numeric_cols]))
    cleaned_df = raw_df[(z_scores < 3).all(axis=1)]
    
    # 3. 特征工程
    print("\n3. 特征工程...")
    # 创建新特征
    cleaned_df['rooms_per_household'] = cleaned_df['total_rooms'] / cleaned_df['households']
    cleaned_df['bedrooms_per_room'] = cleaned_df['total_bedrooms'] / cleaned_df['total_rooms']
    cleaned_df['population_per_household'] = cleaned_df['population'] / cleaned_df['households']
    
    # 处理分类变量
    feature_df = pd.get_dummies(cleaned_df, columns=['ocean_proximity'], prefix='area', drop_first=True)
    
    # 删除冗余特征
    cols_to_drop = ['total_rooms', 'total_bedrooms', 'population']
    feature_df = feature_df.drop(cols_to_drop, axis=1)
    
    # 4. 准备训练数据
    print("\n4. 准备训练数据...")
    # 分离特征和标签
    X = feature_df.drop('median_house_value', axis=1)
    y = feature_df['median_house_value'].values
    
    # 对标签进行对数变换
    y_log = np.log(y)
    
    # 数据集拆分
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_log, test_size=0.2, random_state=42
    )
    
    # 特征标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    feature_names = X.columns.tolist()
    print(f"使用的特征数量: {len(feature_names)}")
    
    # 5. 传统机器学习预测
    ml_results, ml_predictions, ml_models = traditional_ml_prediction(
        X_train_scaled, X_test_scaled, y_train, y_test, feature_names
    )
    
    # 6. 假设深度学习模型结果（需要替换为实际结果）
    # 这里假设深度学习模型的结果，实际使用时需要从深度学习模型获取
    dl_results = {
        'RMSE': 58752.56,  # 替换为实际值
        'R2_Score': 0.7221,  # 替换为实际值
        'MAE': 39313.50  # 替换为实际值
    }
    dl_predictions = np.exp(y_test) * 0.95 + np.random.normal(0, 10000, len(y_test))  # 模拟预测结果
    
    # 7. 模型对比可视化
    compare_models_visualization(ml_results, dl_results, ml_predictions, dl_predictions, y_test)
    
    # 8. 特征重要性分析
    importance_df = analyze_traditional_feature_importance(
        RandomForestRegressor(n_estimators=100, random_state=42),
        feature_names, X_train_scaled, y_train
    )
    
    # 9. 超参数调优
    tuned_models = hyperparameter_tuning(X_train_scaled, y_train)
    
    # 10. 保存最佳传统模型
    best_ml_name = min(ml_results, key=lambda x: ml_results[x]['RMSE'])
    best_model = ml_models[best_ml_name]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f'traditional_ml_model_{timestamp}.pkl'
    joblib.dump(best_model, model_path)
    print(f"\n最佳传统模型已保存: {model_path}")
    
    print("\n=== 传统机器学习预测完成 ===")

if __name__ == "__main__":
    main()