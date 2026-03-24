# import numpy as np
# import time
# import wandb
# import random

# def loadData(fileName):
#     '''
#     加载Mnist数据集
#     :param fileName:要加载的数据集路径
#     :return: list形式的数据集及标记
#     '''
#     print('start to read data')
#     dataArr = []  # 用于存储数据集的列表
#     labelArr = []  # 用于存储数据标记的列表
#     fr = open(fileName, 'r')  # 以只读模式打开数据集文件
#     for line in fr.readlines():  # 逐行读取文件内容
#         curLine = line.strip().split(',')  # 去除每行两端的空白字符并按逗号分割
#         if int(curLine[0]) >= 5:  # 根据第一个字符（标签）判断类别，大于等于5标记为1
#             labelArr.append(1)
#         else:  # 小于5标记为 -1
#             labelArr.append(-1)
#         dataArr.append([int(num) / 255 for num in curLine[1:]])  # 将数据归一化后添加到数据列表
#     return dataArr, labelArr  # 返回数据集和标记列表

# def knn(trainData, trainLabel, testData, k=4):  # 适当减小k值加快计算
#     '''
#     K近邻算法
#     :param trainData: 训练集数据 (list)
#     :param trainLabel: 训练集标签 (list)
#     :param testData: 测试集数据 (list)
#     :param k: 近邻数,默认3
#     :return: 预测标签 (list)
#     '''
#     print('start to predict')
#     trainMat = np.mat(trainData)  # 将训练数据转换为矩阵形式
#     testMat = np.mat(testData)  # 将测试数据转换为矩阵形式
#     m, n = np.shape(testMat)  # 获取测试数据矩阵的行数和列数
#     predictLabels = []  # 用于存储预测标签的列表
#     for i in range(m):  # 遍历测试数据的每一行
#         diffMat = testMat[i] - trainMat  # 计算测试数据与训练数据的差值矩阵
#         sqDiffMat = np.square(diffMat)  # 对差值矩阵的每个元素求平方
#         sqDistances = np.sum(sqDiffMat, axis=1)  # 按行求和得到平方距离
#         distances = np.sqrt(sqDistances)  # 对平方距离求平方根得到实际距离
#         sortedIndices = np.argsort(distances, axis=0)  # 对距离进行排序，返回排序后的索引
#         labelCount = {}  # 用于统计近邻标签的字典
#         for j in range(k):  # 遍历前k个近邻
#             voteLabel = trainLabel[sortedIndices[j, 0]]  # 获取近邻的标签
#             labelCount[voteLabel] = labelCount.get(voteLabel, 0) + 1  # 统计标签出现的次数
#         sortedLabelCount = sorted(labelCount.items(), key=lambda item: item[1], reverse=True)  # 按标签出现次数从大到小排序
#         predictLabels.append(sortedLabelCount[0][0])  # 将出现次数最多的标签作为预测标签
#     return predictLabels  # 返回预测标签列表

# def precision_score(testLabel, predictLabels):
#     '''
#     计算精确率
#     :param testLabel: 测试集真实标签
#     :param predictLabels: 预测标签
#     :return: 精确率
#     '''
#     true_positives = 0  # 真正例（预测为正且实际为正）的数量
#     predicted_positives = 0  # 预测为正的数量
#     for i in range(len(testLabel)):  # 遍历测试标签
#         if predictLabels[i] == 1:  # 如果预测标签为正
#             predicted_positives += 1  # 预测为正的数量加1
#             if testLabel[i] == 1:  # 如果实际标签也为正
#                 true_positives += 1  # 真正例数量加1
#     if predicted_positives == 0:  # 如果预测为正的数量为0，避免除零错误
#         return 0
#     return true_positives / predicted_positives  # 返回精确率

# def recall_score(testLabel, predictLabels):
#     '''
#     计算召回率
#     :param testLabel: 测试集真实标签
#     :param predictLabels: 预测标签
#     :return: 召回率
#     '''
#     true_positives = 0  # 真正例（预测为正且实际为正）的数量
#     actual_positives = 0  # 实际为正的数量
#     for i in range(len(testLabel)):  # 遍历测试标签
#         if testLabel[i] == 1:  # 如果实际标签为正
#             actual_positives += 1  # 实际为正的数量加1
#             if predictLabels[i] == 1:  # 如果预测标签也为正
#                 true_positives += 1  # 真正例数量加1
#     if actual_positives == 0:  # 如果实际为正的数量为0，避免除零错误
#         return 0
#     return true_positives / actual_positives  # 返回召回率

# def f1_score(testLabel, predictLabels):
#     '''
#     计算F1值
#     :param testLabel: 测试集真实标签
#     :param predictLabels: 预测标签
#     :return: F1值
#     '''
#     precision = precision_score(testLabel, predictLabels)  # 计算精确率
#     recall = recall_score(testLabel, predictLabels)  # 计算召回率
#     if precision + recall == 0:  # 如果精确率和召回率之和为0，避免除零错误
#         return 0
#     return 2 * (precision * recall) / (precision + recall)  # 返回F1值

# def model_test(testLabel, predictLabels):
#     '''
#     测试准确率
#     :param testLabel: 测试集真实标签
#     :param predictLabels: 预测标签
#     :return: 正确率
#     '''
#     print('start to test')
#     errorCnt = 0  # 错误预测的数量
#     m = len(testLabel)  # 测试标签的数量
#     for i in range(m):  # 遍历测试标签
#         if testLabel[i] != predictLabels[i]:  # 如果预测标签与真实标签不相等
#             errorCnt += 1  # 错误数量加1
#     accruRate = 1 - (errorCnt / m)  # 计算准确率
#     return accruRate  # 返回准确率

# if __name__ == '__main__':
#     wandb.init(project="mnist_knn", name="KNN_Experiment")  # 初始化wandb项目和实验名称
#     start_time = time.time()  # 记录开始时间
#     trainData, trainLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_train.csv")  # 加载训练数据和标签
#     testData, testLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_test.csv")  # 加载测试数据和标签

#     # 随机抽取部分训练数据，这里抽取1000条示例
#     sample_indices = random.sample(range(len(trainData)), 5000)  # 随机抽取1000个索引
#     sampled_trainData = [trainData[i] for i in sample_indices]  # 根据索引获取训练数据
#     sampled_trainLabel = [trainLabel[i] for i in sample_indices]  # 根据索引获取训练标签

#     num_iterations = 5  # 设定迭代次数
#     iteration_step = len(sampled_trainData) // num_iterations  # 每次迭代增加的样本数
#     for i in range(num_iterations):  # 进行迭代
#         start_idx = i * iteration_step  # 起始索引
#         end_idx = (i + 1) * iteration_step  # 结束索引
#         cur_trainData = sampled_trainData[start_idx:end_idx]  # 获取当前迭代的训练数据
#         cur_trainLabel = sampled_trainLabel[start_idx:end_idx]  # 获取当前迭代的训练标签

#         predictLabels = knn(cur_trainData, cur_trainLabel, testData)  # 使用KNN算法进行预测
#         accruRate = model_test(testLabel, predictLabels)  # 计算准确率
#         precision = precision_score(testLabel, predictLabels)  # 计算精确率
#         recall = recall_score(testLabel, predictLabels)  # 计算召回率
#         f1 = f1_score(testLabel, predictLabels)  # 计算F1值

#         wandb.log({
#             "accuracy": accruRate,
#             "precision": precision,
#             "recall": recall,
#             "f1_score": f1,
#             "time_span": time.time() - start_time,
#             "iteration": i + 1
#         })  # 使用wandb记录各项指标和时间

#     end_time = time.time()  # 记录结束时间
#     print('accuracy rate is:', accruRate)  # 打印准确率
#     print('precision is:', precision)  # 打印精确率
#     print('recall is:', recall)  # 打印召回率
#     print('f1 score is:', f1)  # 打印F1值
#     print('time span:', end_time - start_time)  # 打印运行时间
#     wandb.finish()  # 结束wandb记录


import numpy as np
import time
import wandb
import random

def loadData(fileName):
    '''
    加载Mnist数据集
    :param fileName:要加载的数据集路径
    :return: list形式的数据集及标记
    '''
    print('start to read data')
    dataArr = []  # 用于存储数据集的列表
    labelArr = []  # 用于存储数据标记的列表
    fr = open(fileName, 'r')  # 以只读模式打开数据集文件
    for line in fr.readlines():  # 逐行读取文件内容
        curLine = line.strip().split(',')  # 去除每行两端的空白字符并按逗号分割
        if int(curLine[0]) >= 5:  # 根据第一个字符（标签）判断类别，大于等于5标记为1
            labelArr.append(1)
        else:  # 小于5标记为 -1
            labelArr.append(-1)
        dataArr.append([int(num) / 255 for num in curLine[1:]])  # 将数据归一化后添加到数据列表
    return dataArr, labelArr  # 返回数据集和标记列表

def knn(trainData, trainLabel, testData, k=4):  # 适当减小k值加快计算
    '''
    K近邻算法
    :param trainData: 训练集数据 (list)
    :param trainLabel: 训练集标签 (list)
    :param testData: 测试集数据 (list)
    :param k: 近邻数,默认3
    :return: 预测标签 (list)
    '''
    print('start to predict')
    trainMat = np.mat(trainData)  # 将训练数据转换为矩阵形式
    testMat = np.mat(testData)  # 将测试数据转换为矩阵形式
    m, n = np.shape(testMat)  # 获取测试数据矩阵的行数和列数
    predictLabels = []  # 用于存储预测标签的列表
    for i in range(m):  # 遍历测试数据的每一行
        diffMat = testMat[i] - trainMat  # 计算测试数据与训练数据的差值矩阵
        sqDiffMat = np.square(diffMat)  # 对差值矩阵的每个元素求平方
        sqDistances = np.sum(sqDiffMat, axis=1)  # 按行求和得到平方距离
        distances = np.sqrt(sqDistances)  # 对平方距离求平方根得到实际距离
        sortedIndices = np.argsort(distances, axis=0)  # 对距离进行排序，返回排序后的索引
        labelCount = {}  # 用于统计近邻标签的字典
        for j in range(k):  # 遍历前k个近邻
            voteLabel = trainLabel[sortedIndices[j, 0]]  # 获取近邻的标签
            labelCount[voteLabel] = labelCount.get(voteLabel, 0) + 1  # 统计标签出现的次数
        sortedLabelCount = sorted(labelCount.items(), key=lambda item: item[1], reverse=True)  # 按标签出现次数从大到小排序
        predictLabels.append(sortedLabelCount[0][0])  # 将出现次数最多的标签作为预测标签
    return predictLabels  # 返回预测标签列表

def precision_score(testLabel, predictLabels):
    '''
    计算精确率
    :param testLabel: 测试集真实标签
    :param predictLabels: 预测标签
    :return: 精确率
    '''
    true_positives = 0  # 真正例（预测为正且实际为正）的数量
    predicted_positives = 0  # 预测为正的数量
    for i in range(len(testLabel)):  # 遍历测试标签
        if predictLabels[i] == 1:  # 如果预测标签为正
            predicted_positives += 1  # 预测为正的数量加1
            if testLabel[i] == 1:  # 如果实际标签也为正
                true_positives += 1  # 真正例数量加1
    if predicted_positives == 0:  # 如果预测为正的数量为0，避免除零错误
        return 0
    return true_positives / predicted_positives  # 返回精确率

def recall_score(testLabel, predictLabels):
    '''
    计算召回率
    :param testLabel: 测试集真实标签
    :param predictLabels: 预测标签
    :return: 召回率
    '''
    true_positives = 0  # 真正例（预测为正且实际为正）的数量
    actual_positives = 0  # 实际为正的数量
    for i in range(len(testLabel)):  # 遍历测试标签
        if testLabel[i] == 1:  # 如果实际标签为正
            actual_positives += 1  # 实际为正的数量加1
            if predictLabels[i] == 1:  # 如果预测标签也为正
                true_positives += 1  # 真正例数量加1
    if actual_positives == 0:  # 如果实际为正的数量为0，避免除零错误
        return 0
    return true_positives / actual_positives  # 返回召回率

def f1_score(testLabel, predictLabels):
    '''
    计算F1值
    :param testLabel: 测试集真实标签
    :param predictLabels: 预测标签
    :return: F1值
    '''
    precision = precision_score(testLabel, predictLabels)  # 计算精确率
    recall = recall_score(testLabel, predictLabels)  # 计算召回率
    if precision + recall == 0:  # 如果精确率和召回率之和为0，避免除零错误
        return 0
    return 2 * (precision * recall) / (precision + recall)  # 返回F1值

def model_test(testLabel, predictLabels):
    '''
    测试准确率
    :param testLabel: 测试集真实标签
    :param predictLabels: 预测标签
    :return: 正确率
    '''
    print('start to test')
    errorCnt = 0  # 错误预测的数量
    m = len(testLabel)  # 测试标签的数量
    for i in range(m):  # 遍历测试标签
        if testLabel[i] != predictLabels[i]:  # 如果预测标签与真实标签不相等
            errorCnt += 1  # 错误数量加1
    accruRate = 1 - (errorCnt / m)  # 计算准确率
    return accruRate  # 返回准确率

if __name__ == '__main__':
    wandb.init(project="mnist_knn", name="KNN_Experiment")  # 初始化wandb项目和实验名称
    start_time = time.time()  # 记录开始时间
    trainData, trainLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_train.csv")  # 加载训练数据和标签
    testData, testLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_test.csv")  # 加载测试数据和标签

    num_iterations = 5  # 设定迭代次数
    iteration_step = len(trainData) // num_iterations  # 每次迭代增加的样本数，这里基于全部训练数据计算
    for i in range(num_iterations):  # 进行迭代
        start_idx = i * iteration_step  # 起始索引
        end_idx = (i + 1) * iteration_step  # 结束索引
        cur_trainData = trainData[start_idx:end_idx]  # 获取当前迭代的训练数据
        cur_trainLabel = trainLabel[start_idx:end_idx]  # 获取当前迭代的训练标签

        predictLabels = knn(cur_trainData, cur_trainLabel, testData)  # 使用KNN算法进行预测
        accruRate = model_test(testLabel, predictLabels)  # 计算准确率
        precision = precision_score(testLabel, predictLabels)  # 计算精确率
        recall = recall_score(testLabel, predictLabels)  # 计算召回率
        f1 = f1_score(testLabel, predictLabels)  # 计算F1值

        wandb.log({
            "accuracy": accruRate,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "time_span": time.time() - start_time,
            "iteration": i + 1
        })  # 使用wandb记录各项指标和时间

    end_time = time.time()  # 记录结束时间
    print('accuracy rate is:', accruRate)  # 打印准确率
    print('precision is:', precision)  # 打印精确率
    print('recall is:', recall)  # 打印召回率
    print('f1 score is:', f1)  # 打印F1值
    print('time span:', end_time - start_time)  # 打印运行时间
    wandb.finish()  # 结束wandb记录