import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import joblib

# 设置中文字体和图形样式
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class HandwrittenDigitRecognizer:
    def __init__(self, dataset_type='sklearn'):
        """
        初始化手写数字识别器
        
        参数:
        dataset_type: 数据集类型 ('sklearn' 或 'csv')
        """
        self.dataset_type = dataset_type
        self.model = None
        self.scaler = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_sklearn_dataset(self):
        # 加载sklearn自带的数字数据集
        digits = load_digits()
        data = digits.data
        target = digits.target
        
        print('数据集形状:', data.shape)
        print('标签形状:', target.shape)
        print('类别分布:')
        for i in range(10):
            print(f'数字 {i}: {np.sum(target == i)} 个样本')
        
        return data, target, digits.images
    
    def load_csv_dataset(self, file_path):
        """从CSV文件加载数据集[5](@ref)"""
        data = pd.read_csv(file_path)
        print('数据集基本信息:', data.shape)
        
        # 假设第一列是标签，其余列是特征
        y = data.iloc[:, 0].values
        X = data.iloc[:, 1:].values
        
        print('特征形状:', X.shape)
        print('标签形状:', y.shape)
        print('类别分布:')
        for i in range(10):
            print(f'数字 {i}: {np.sum(y == i)} 个样本')
            
        return X, y, None
    
    def explore_dataset(self, images, target, n_samples=5):
        # 探索数据集并可视化样本
        if images is not None:
            fig, axes = plt.subplots(2, n_samples, figsize=(15, 6))
            
            for i in range(n_samples):
                # 显示原始样本
                axes[0, i].imshow(images[i], cmap='gray')
                axes[0, i].set_title(f'标签: {target[i]}')
                axes[0, i].axis('off')
                
                # 显示随机样本
                idx = np.random.randint(0, len(images))
                axes[1, i].imshow(images[idx], cmap='gray')
                axes[1, i].set_title(f'标签: {target[idx]}')
                axes[1, i].axis('off')
            
            plt.suptitle('手写数字样本展示', fontsize=16)
            plt.tight_layout()
            plt.show()
    
    def preprocess_data(self, X, y, test_size=0.25, random_state=42, method='standard'):
        
        # 划分训练集和测试集
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f'训练集大小: {self.X_train.shape}')
        print(f'测试集大小: {self.X_test.shape}')
        
        # 数据标准化
        if method == 'standard':
            self.scaler = StandardScaler()
            self.X_train_scaled = self.scaler.fit_transform(self.X_train)
            self.X_test_scaled = self.scaler.transform(self.X_test)
        else:  # minmax
            self.scaler = MinMaxScaler()
            self.X_train_scaled = self.scaler.fit_transform(self.X_train)
            self.X_test_scaled = self.scaler.transform(self.X_test)
            
        return self.X_train_scaled, self.X_test_scaled, self.y_train, self.y_test
    
    def train_model(self, n_neighbors=5, algorithm='auto', weights='uniform'):
        """训练KNN模型[1,2](@ref)"""
        self.model = KNeighborsClassifier(
            n_neighbors=n_neighbors,
            algorithm=algorithm,
            weights=weights
        )
        
        self.model.fit(self.X_train_scaled, self.y_train)
        
        # 训练集准确率
        train_pred = self.model.predict(self.X_train_scaled)
        train_accuracy = accuracy_score(self.y_train, train_pred)
        print(f'训练集准确率: {train_accuracy:.4f}')
        
        return self.model
    
    def evaluate_model(self):
        # 模型评估
        if self.model is None:
            print("请先训练模型！")
            return
        
        # 测试集预测
        y_pred = self.model.predict(self.X_test_scaled)
        
        # 准确率
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f'测试集准确率: {accuracy:.4f}')
        
        # 详细分类报告
        print('\n详细分类报告:')
        print(classification_report(self.y_test, y_pred))
        
        # 混淆矩阵
        self.plot_confusion_matrix(self.y_test, y_pred)
        
        return accuracy, y_pred
    
    def plot_confusion_matrix(self, y_true, y_pred):
        """绘制混淆矩阵"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=range(10), yticklabels=range(10))
        plt.title('混淆矩阵')
        plt.xlabel('预测值')
        plt.ylabel('真实值')
        plt.show()
    
    def find_best_k(self, k_range=range(1, 16)):
        # 寻找最佳k值
        train_scores = []
        test_scores = []
        
        for k in k_range:
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(self.X_train_scaled, self.y_train)
            
            train_score = knn.score(self.X_train_scaled, self.y_train)
            test_score = knn.score(self.X_test_scaled, self.y_test)
            
            train_scores.append(train_score)
            test_scores.append(test_score)
        
        # 绘制K值选择图
        plt.figure(figsize=(10, 6))
        plt.plot(k_range, train_scores, label='训练集准确率')
        plt.plot(k_range, test_scores, label='测试集准确率')
        plt.xlabel('K值')
        plt.ylabel('准确率')
        plt.title('K值选择对准确率的影响')
        plt.legend()
        plt.show()
        
        best_k = k_range[np.argmax(test_scores)]
        best_score = max(test_scores)
        print(f'最佳K值: {best_k}, 对应准确率: {best_score:.4f}')
        
        return best_k, best_score
    
    def predict_single_digit(self, digit_data):
        # 预测单个数字
        if self.model is None or self.scaler is None:
            print("请先训练模型！")
            return
        
        # 数据预处理
        if len(digit_data.shape) > 1:
            digit_data = digit_data.reshape(1, -1)
        
        digit_scaled = self.scaler.transform(digit_data)
        prediction = self.model.predict(digit_scaled)[0]
        probability = np.max(self.model.predict_proba(digit_scaled))
        
        print(f'预测数字: {prediction}, 置信度: {probability:.4f}')
        return prediction, probability
    
    def save_model(self, file_path):
        # 保存训练模型
        if self.model is not None:
            joblib.dump({
                'model': self.model,
                'scaler': self.scaler
            }, file_path)
            print(f'模型已保存到: {file_path}')
    
    def load_model(self, file_path):
        # 加载已保存的模型
        try:
            loaded = joblib.load(file_path)
            self.model = loaded['model']
            self.scaler = loaded['scaler']
            print(f'模型已从 {file_path} 加载')
        except:
            print('模型加载失败！')

def main():
    # 创建识别器实例
    recognizer = HandwrittenDigitRecognizer(dataset_type='sklearn')
    
    # 1. 加载数据
    print("=" * 50)
    print("步骤1: 加载数据")
    print("=" * 50)
    
    X, y, images = recognizer.load_sklearn_dataset()
    
    # 2. 数据探索
    print("\n" + "=" * 50)
    print("步骤2: 数据探索")
    print("=" * 50)
    
    recognizer.explore_dataset(images, y)
    
    # 3. 数据预处理
    print("\n" + "=" * 50)
    print("步骤3: 数据预处理")
    print("=" * 50)
    
    X_train_scaled, X_test_scaled, y_train, y_test = recognizer.preprocess_data(
        X, y, test_size=0.25, random_state=42, method='standard'
    )
    
    # 4. 寻找最佳K值
    print("\n" + "=" * 50)
    print("步骤4: 寻找最佳K值")
    print("=" * 50)
    
    best_k, best_score = recognizer.find_best_k(range(1, 16))
    
    # 5. 使用最佳K值训练模型
    print("\n" + "=" * 50)
    print("步骤5: 训练模型")
    print("=" * 50)
    
    model = recognizer.train_model(n_neighbors=best_k, algorithm='kd_tree')
    
    # 6. 评估模型
    print("\n" + "=" * 50)
    print("步骤6: 模型评估")
    print("=" * 50)
    
    accuracy, y_pred = recognizer.evaluate_model()
    
    # 7. 保存模型
    print("\n" + "=" * 50)
    print("步骤7: 保存模型")
    print("=" * 50)
    
    recognizer.save_model('knn_handwritten_digit_model.pkl')
    
    # 8. 实例预测
    print("\n" + "=" * 50)
    print("步骤8: 实例预测")
    print("=" * 50)
    
    if images is not None:
        # 随机选择测试样本进行预测
        test_idx = np.random.randint(0, len(recognizer.X_test))
        test_sample = recognizer.X_test[test_idx].reshape(1, -1)
        actual_label = recognizer.y_test[test_idx]
        
        print(f"测试样本索引: {test_idx}")
        print(f"实际数字: {actual_label}")
        
        prediction, confidence = recognizer.predict_single_digit(test_sample)
        
        # 显示测试样本
        if images is not None:
            # 需要找到原始图像
            original_idx = np.where((X == recognizer.X_test[test_idx]).all(axis=1))[0]
            if len(original_idx) > 0:
                plt.imshow(images[original_idx[0]], cmap='gray')
                plt.title(f'实际: {actual_label}, 预测: {prediction}, 置信度: {confidence:.4f}')
                plt.axis('off')
                plt.show()

if __name__ == "__main__":
    main()