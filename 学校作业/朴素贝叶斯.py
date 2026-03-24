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


# def decision_tree(trainData, trainLabel, testData, testLabel):
#     print('start to train and predict')
#     num_iterations = 120  # 设定迭代次数
#     iteration_step = len(trainData) // num_iterations  # 每次迭代增加的样本数
#     # iteration_step = len(trainData)
#     accuracies = []
#     precisions = []
#     recalls = []
#     f1_scores = []

#     for i in range(num_iterations):
#         start_idx = i * iteration_step  # 起始索引
#         end_idx = (i + 1) * iteration_step  # 结束索引
#         cur_trainData = trainData[start_idx:end_idx]  # 获取当前迭代的训练数据
#         cur_trainLabel = trainLabel[start_idx:end_idx]  # 获取当前迭代的训练标签

#         # 将数据转换为numpy数组
#         cur_trainData = np.array(cur_trainData)
#         cur_trainLabel = np.array(cur_trainLabel)
#         testData = np.array(testData)
#         testLabel = np.array(testLabel)

#         # 确保cur_trainData是二维数组
#         if cur_trainData.ndim == 1:
#             cur_trainData = cur_trainData.reshape(-1, 1)

#         # 创建决策树模型，这里设置了一些超参数，你可以根据需要调整
#         model = DecisionTreeClassifier(max_depth=5, random_state=42)
#         model.fit(cur_trainData, cur_trainLabel)
#         predictLabels = model.predict(testData)

#         # 计算评估指标
#         accruRate = accuracy_score(testLabel, predictLabels)
#         precision = custom_precision_score(testLabel, predictLabels)
#         recall = custom_recall_score(testLabel, predictLabels)
#         f1 = custom_f1_score(testLabel, predictLabels)

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

#     accuracies, precisions, recalls, f1_scores = decision_tree(trainData, trainLabel, testData, testLabel)

#     end_time = time.time()

#     print('accuracy rate is:', accuracies[-1])
#     print('precision is:', precisions[-1])
#     print('recall is:', recalls[-1])
#     print('f1 score is:', f1_scores[-1])
#     print('time span:', end_time - start_time)

#     wandb.finish()


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


# def decision_tree(trainData, trainLabel, testData, testLabel):
#     print('start to train and predict')
#     num_iterations = 120  # 设定迭代次数
#     accuracies = []
#     precisions = []
#     recalls = []
#     f1_scores = []

#     # 将数据转换为numpy数组
#     trainData = np.array(trainData)
#     trainLabel = np.array(trainLabel)
#     testData = np.array(testData)
#     testLabel = np.array(testLabel)

#     for i in range(num_iterations):
#         # 确保trainData是二维数组
#         if trainData.ndim == 1:
#             trainData = trainData.reshape(-1, 1)

#         # 创建决策树模型，这里设置了一些超参数，你可以根据需要调整
#         model = DecisionTreeClassifier(max_depth=5, random_state=42)
#         model.fit(trainData, trainLabel)
#         predictLabels = model.predict(testData)

#         # 计算评估指标
#         accruRate = accuracy_score(testLabel, predictLabels)
#         precision = custom_precision_score(testLabel, predictLabels)
#         recall = custom_recall_score(testLabel, predictLabels)
#         f1 = custom_f1_score(testLabel, predictLabels)

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

#     accuracies, precisions, recalls, f1_scores = decision_tree(trainData, trainLabel, testData, testLabel)

#     end_time = time.time()

#     print('accuracy rate is:', accuracies[-1])
#     print('precision is:', precisions[-1])
#     print('recall is:', recalls[-1])
#     print('f1 score is:', f1_scores[-1])
#     print('time span:', end_time - start_time)

#     wandb.finish()



import numpy as np
import time
import wandb
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_curve, auc, confusion_matrix
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


def decision_tree(trainData, trainLabel, testData, testLabel):
    print('start to train and predict')
    num_iterations = 120  # 设定迭代次数
    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    fpr_list = []
    tpr_list = []
    auc_list = []
    confusion_matrices = []

    # 将数据转换为numpy数组
    trainData = np.array(trainData)
    trainLabel = np.array(trainLabel)
    testData = np.array(testData)
    testLabel = np.array(testLabel)

    for i in range(num_iterations):
        # 确保trainData是二维数组
        if trainData.ndim == 1:
            trainData = trainData.reshape(-1, 1)

        # 创建决策树模型，这里设置了一些超参数，你可以根据需要调整
        model = DecisionTreeClassifier(max_depth=5, random_state=42)
        model.fit(trainData, trainLabel)
        predictLabels = model.predict(testData)
        probas = model.predict_proba(testData)[:, 1]  # 获取正类概率

        # 计算评估指标
        accruRate = accuracy_score(testLabel, predictLabels)
        precision = custom_precision_score(testLabel, predictLabels)
        recall = custom_recall_score(testLabel, predictLabels)
        f1 = custom_f1_score(testLabel, predictLabels)

        accuracies.append(accruRate)
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)

        # 计算ROC曲线和AUC
        fpr, tpr, _ = roc_curve(testLabel, probas)
        roc_auc = auc(fpr, tpr)
        fpr_list.append(fpr)
        tpr_list.append(tpr)
        auc_list.append(roc_auc)

        # 计算混淆矩阵
        cm = confusion_matrix(testLabel, predictLabels)
        confusion_matrices.append(cm)

        # 记录指标到wandb
        wandb.log({
            "accuracy": accruRate,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "time_span": time.time() - start_time,
            "iteration": i + 1,
            "roc_auc": roc_auc
        })

    return accuracies, precisions, recalls, f1_scores, fpr_list, tpr_list, auc_list, confusion_matrices


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

    accuracies, precisions, recalls, f1_scores, fpr_list, tpr_list, auc_list, confusion_matrices = decision_tree(
        trainData, trainLabel, testData, testLabel)

    end_time = time.time()

    print('accuracy rate is:', accuracies[-1])
    print('precision is:', precisions[-1])
    print('recall is:', recalls[-1])
    print('f1 score is:', f1_scores[-1])
    print('time span:', end_time - start_time)

    # 绘制评估指标随迭代次数变化的折线图
    iterations = range(1, len(accuracies) + 1)
    plt.figure(figsize=(12, 8))
    plt.plot(iterations, accuracies, label='Accuracy')
    plt.plot(iterations, precisions, label='Precision')
    plt.plot(iterations, recalls, label='Recall')
    plt.plot(iterations, f1_scores, label='F1 Score')
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.title('Evaluation Metrics over Iterations')
    plt.legend()
    plt.savefig('evaluation_metrics.png')
    plt.show()

    # 绘制ROC曲线
    plt.figure(figsize=(12, 8))
    for i in range(len(fpr_list)):
        plt.plot(fpr_list[i], tpr_list[i], label=f'Iteration {i + 1} (AUC = {auc_list[i]:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.savefig('roc_curve.png')
    plt.show()

    # 绘制混淆矩阵
    for i in range(len(confusion_matrices)):
        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_matrices[i], annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.title(f'Confusion Matrix - Iteration {i + 1}')
        plt.savefig(f'confusion_matrix_{i + 1}.png')
        plt.show()

    wandb.finish()