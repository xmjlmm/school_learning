# import numpy as np
# import time
# import wandb
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score


# def loadData(fileName):
#     '''
#     加载Mnist数据集
#     :param fileName:要加载的数据集路径
#     :return: list形式的数据集及标记
#     '''
#     print('start to read data')
#     dataArr = []
#     labelArr = []
#     fr = open(fileName, 'r')
#     for line in fr.readlines():
#         curLine = line.strip().split(',')
#         if int(curLine[0]) >= 5:
#             labelArr.append(1)
#         else:
#             labelArr.append(-1)
#         dataArr.append([int(num) / 255 for num in curLine[1:]])
#     return dataArr, labelArr


# def decision_tree(trainData, trainLabel, testData, testLabel, num_iterations):
#     print('start to train and predict')
#     accuracies = []
#     precisions = []
#     recalls = []
#     f1_scores = []

#     for i in range(num_iterations):
#         # 转换为numpy数组并打乱数据顺序
#         cur_trainData = np.array(trainData)
#         cur_trainLabel = np.array(trainLabel)
#         indices = np.arange(len(cur_trainData))
#         np.random.shuffle(indices)  # 打乱数据索引
#         cur_trainData = cur_trainData[indices]
#         cur_trainLabel = cur_trainLabel[indices]

#         testData_np = np.array(testData)
#         testLabel_np = np.array(testLabel)

#         # 确保cur_trainData是二维数组
#         if cur_trainData.ndim == 1:
#             cur_trainData = cur_trainData.reshape(-1, 1)

#         # 移除固定的random_state，引入模型随机性
#         model = DecisionTreeClassifier(max_depth=5)
#         model.fit(cur_trainData, cur_trainLabel)
#         predictLabels = model.predict(testData_np)

#         # 计算评估指标
#         accruRate = accuracy_score(testLabel_np, predictLabels)
#         precision = custom_precision_score(testLabel_np, predictLabels)
#         recall = custom_recall_score(testLabel_np, predictLabels)
#         f1 = custom_f1_score(testLabel_np, predictLabels)

#         accuracies.append(accruRate)
#         precisions.append(precision)
#         recalls.append(recall)
#         f1_scores.append(f1)

#         # 记录指标到wandb
#         wandb.log({
#             "accuracy": accruRate,
#             "precision": precision,
#             "recall": recall,
#             "f1_score": f1,
#             "time_span": time.time() - start_time,
#             "iteration": i + 1
#         })

#     return accuracies, precisions, recalls, f1_scores


# def custom_precision_score(testLabel, predictLabels):
#     '''
#     计算精确率
#     :param testLabel: 测试集真实标签
#     :param predictLabels: 预测标签
#     :return: 精确率
#     '''
#     true_positives = 0
#     predicted_positives = 0
#     for i in range(len(testLabel)):
#         if predictLabels[i] == 1:
#             predicted_positives += 1
#             if testLabel[i] == 1:
#                 true_positives += 1
#     if predicted_positives == 0:
#         return 0
#     return true_positives / predicted_positives


# def custom_recall_score(testLabel, predictLabels):
#     '''
#     计算召回率
#     :param testLabel: 测试集真实标签
#     :param predictLabels: 预测标签
#     :return: 召回率
#     '''
#     true_positives = 0
#     actual_positives = 0
#     for i in range(len(testLabel)):
#         if testLabel[i] == 1:
#             actual_positives += 1
#             if predictLabels[i] == 1:
#                 true_positives += 1
#     if actual_positives == 0:
#         return 0
#     return true_positives / actual_positives


# def custom_f1_score(testLabel, predictLabels):
#     '''
#     计算F1值
#     :param testLabel: 测试集真实标签
#     :param predictLabels: 预测标签
#     :return: F1值
#     '''
#     precision = custom_precision_score(testLabel, predictLabels)
#     recall = custom_recall_score(testLabel, predictLabels)
#     if precision + recall == 0:
#         return 0
#     return 2 * (precision * recall) / (precision + recall)


# if __name__ == '__main__':
#     wandb.init(project="mnist_decision_tree", name="Decision_Tree_Experiment")
#     start_time = time.time()
#     trainData, trainLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_train.csv")
#     testData, testLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_test.csv")

#     num_runs = 5  # 训练轮数
#     num_iterations = 120  # 每轮的迭代次数

#     for run in range(num_runs):
#         print(f"Starting run {run + 1}")
#         accuracies, precisions, recalls, f1_scores = decision_tree(trainData, trainLabel, testData, testLabel,
#                                                                    num_iterations)

#         print(f'Run {run + 1} accuracy rate is:', accuracies[-1])
#         print(f'Run {run + 1} precision is:', precisions[-1])
#         print(f'Run {run + 1} recall is:', recalls[-1])
#         print(f'Run {run + 1} f1 score is:', f1_scores[-1])

#     end_time = time.time()
#     print('Total time span:', end_time - start_time)

#     wandb.finish()



import numpy as np
import time
import wandb
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns


def loadData(fileName):
    '''
    加载Mnist数据集
    :param fileName:要加载的数据集路径
    :return: list形式的数据集及标记
    '''
    print('start to read data')
    dataArr = []
    labelArr = []
    fr = open(fileName, 'r')
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if int(curLine[0]) >= 5:
            labelArr.append(1)
        else:
            labelArr.append(-1)
        dataArr.append([int(num) / 255 for num in curLine[1:]])
    return dataArr, labelArr


def decision_tree(trainData, trainLabel, testData, testLabel, num_iterations):
    print('start to train and predict')
    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []

    for i in range(num_iterations):
        # 转换为numpy数组并打乱数据顺序
        cur_trainData = np.array(trainData)
        cur_trainLabel = np.array(trainLabel)
        indices = np.arange(len(cur_trainData))
        np.random.shuffle(indices)  # 打乱数据索引
        cur_trainData = cur_trainData[indices]
        cur_trainLabel = cur_trainLabel[indices]

        testData_np = np.array(testData)
        testLabel_np = np.array(testLabel)

        # 确保cur_trainData是二维数组
        if cur_trainData.ndim == 1:
            cur_trainData = cur_trainData.reshape(-1, 1)

        # 移除固定的random_state，引入模型随机性
        model = DecisionTreeClassifier(max_depth=5)
        model.fit(cur_trainData, cur_trainLabel)
        predictLabels = model.predict(testData_np)

        # 计算评估指标
        accruRate = accuracy_score(testLabel_np, predictLabels)
        precision = custom_precision_score(testLabel_np, predictLabels)
        recall = custom_recall_score(testLabel_np, predictLabels)
        f1 = custom_f1_score(testLabel_np, predictLabels)

        accuracies.append(accruRate)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)

        # 记录指标到wandb
        wandb.log({
            "accuracy": accruRate,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "time_span": time.time() - start_time,
            "iteration": i + 1
        })

    return accuracies, precisions, recalls, f1_scores


def custom_precision_score(testLabel, predictLabels):
    '''
    计算精确率
    :param testLabel: 测试集真实标签
    :param predictLabels: 预测标签
    :return: 精确率
    '''
    true_positives = 0
    predicted_positives = 0
    for i in range(len(testLabel)):
        if predictLabels[i] == 1:
            predicted_positives += 1
            if testLabel[i] == 1:
                true_positives += 1
    if predicted_positives == 0:
        return 0
    return true_positives / predicted_positives


def custom_recall_score(testLabel, predictLabels):
    '''
    计算召回率
    :param testLabel: 测试集真实标签
    :param predictLabels: 预测标签
    :return: 召回率
    '''
    true_positives = 0
    actual_positives = 0
    for i in range(len(testLabel)):
        if testLabel[i] == 1:
            actual_positives += 1
            if predictLabels[i] == 1:
                true_positives += 1
    if actual_positives == 0:
        return 0
    return true_positives / actual_positives


def custom_f1_score(testLabel, predictLabels):
    '''
    计算F1值
    :param testLabel: 测试集真实标签
    :param predictLabels: 预测标签
    :return: F1值
    '''
    precision = custom_precision_score(testLabel, predictLabels)
    recall = custom_recall_score(testLabel, predictLabels)
    if precision + recall == 0:
        return 0
    return 2 * (precision * recall) / (precision + recall)


if __name__ == '__main__':
    wandb.init(project="mnist_decision_tree", name="Decision_Tree_Experiment")
    start_time = time.time()
    trainData, trainLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_train.csv")
    testData, testLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_test.csv")

    num_runs = 5  # 训练轮数
    num_iterations = 120  # 每轮的迭代次数

    accuracies_all = []
    precisions_all = []
    recalls_all = []
    f1_scores_all = []

    for run in range(num_runs):
        print(f"Starting run {run + 1}")
        accuracies, precisions, recalls, f1_scores = decision_tree(trainData, trainLabel, testData, testLabel,
                                                                   num_iterations)
        accuracies_all.append(accuracies)
        precisions_all.append(precisions)
        recalls_all.append(recalls)
        f1_scores_all.append(f1_scores)

        print(f'Run {run + 1} accuracy rate is:', accuracies[-1])
        print(f'Run {run + 1} precision is:', precisions[-1])
        print(f'Run {run + 1} recall is:', recalls[-1])
        print(f'Run {run + 1} f1 score is:', f1_scores[-1])

    end_time = time.time()
    print('Total time span:', end_time - start_time)

    # 绘制箱线图（各指标在多次运行中的分布）
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    sns.boxplot(data=np.array(accuracies_all).T)
    plt.title('Accuracy Boxplot')
    plt.ylabel('Value')

    plt.subplot(2, 2, 2)
    sns.boxplot(data=np.array(precisions_all).T)
    plt.title('Precision Boxplot')
    plt.ylabel('Value')

    plt.subplot(2, 2, 3)
    sns.boxplot(data=np.array(recalls_all).T)
    plt.title('Recall Boxplot')
    plt.xlabel('Iteration')
    plt.ylabel('Value')

    plt.subplot(2, 2, 4)
    sns.boxplot(data=np.array(f1_scores_all).T)
    plt.title('F1 Score Boxplot')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.tight_layout()
    plt.savefig('boxplots.png')
    plt.show()

    # 绘制多次运行的准确率对比折线图
    plt.figure(figsize=(12, 6))
    for run in range(num_runs):
        plt.plot(accuracies_all[run], label=f'Run {run + 1}')
    plt.xlabel('Iteration')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Across Multiple Runs')
    plt.legend()
    plt.savefig('accuracy_runs.png')
    plt.show()

    wandb.finish()