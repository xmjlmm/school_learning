# import numpy as np
# import time
# from sklearn.metrics import precision_score, recall_score, f1_score
# import wandb
# import matplotlib.pyplot as plt

# def loadData(fileName):
#     '''
#     加载Mnist数据集
#     :param fileName:要加载的数据集路径
#     :return: list形式的数据集及标记
#     '''
#     print('start to read data')
#     # 存放数据及标记的list
#     dataArr = []
#     labelArr = []
#     # 打开文件
#     fr = open(fileName, 'r')
#     # 将文件按行读取
#     for line in fr.readlines():
#         # 对每一行数据进行切割，返回字段列表
#         curLine = line.strip().split(',')

#         # Mnsit有0 - 9十个标记，由于是二分类任务，所以将>=5的作为1，<5为 - 1
#         if int(curLine[0]) >= 5:
#             labelArr.append(1)
#         else:
#             labelArr.append(-1)
#         # 存放标记
#         # [int(num) for num in curLine[1:]] -> 遍历每一行中除了以第一个元素（标记）外将所有元素转换成int类型
#         # [int(num)/255 for num in curLine[1:]] -> 将所有数据除255归一化(非必须步骤，可以不归一化)
#         dataArr.append([int(num) / 255 for num in curLine[1:]])

#     # 返回data和label
#     return dataArr, labelArr

# def perceptron(dataArr, labelArr, iter=50):
#     '''
#     感知器训练过程
#     :param dataArr:训练集的数据 (list)
#     :param labelArr: 训练集的标签(list)
#     :param iter: 迭代次数,默认30
#     :return: 训练好的w和b
#     '''
#     print('start to trans')
#     # 将数据转换成矩阵形式（在机器学习中因为通常都是向量的运算，转换称矩阵形式方便运算）
#     # 转换后的数据中每一个样本的向量都是横向的
#     dataMat = np.mat(dataArr)
#     # 将标签转换成矩阵，之后转置(.T为转置)。
#     # 转置是因为在运算中需要单独取label中的某一个元素，如果是Nx1的矩阵的话，无法用label[i]的方式读取
#     # 对于只有1xN的label可以不转换成矩阵，直接label[i]即可，这里转换是为了格式上的统一
#     labelMat = np.mat(labelArr).T
#     # 获取数据矩阵的大小，为m*n
#     m, n = np.shape(dataMat)
#     # 创建初始权重w，初始值全为0。
#     # np.shape(dataMat)的返回值为m，n -> np.shape(dataMat)[1])的值即为n，与
#     # 样本长度保持一致
#     w = np.zeros((1, np.shape(dataMat)[1]))
#     # 初始化偏置b为0
#     b = 0
#     # 初始化步长，也就是梯度下降过程中的n，控制梯度下降速率
#     h = 0.0001

#     # 进行iter次迭代计算
#     for k in range(iter):
#         # 对于每一个样本进行梯度下降
#         for i in range(m):
#             # 获取当前样本的向量
#             xi = dataMat[i]
#             # 获取当前样本所对应的标签
#             yi = labelMat[i]
#             # 判断是否是误分类样本
#             if -1 * yi * (w * xi.T + b) >= 0:
#                 # 对于误分类样本，进行梯度下降，更新w和b
#                 w = w + h * yi * xi
#                 b = b + h * yi
#         # 打印训练进度
#         print('Round %d:%d training' % (k, iter))
#     # 返回训练完的w、b
#     return w, b

# def model_test(dataArr, labelArr, w, b):
#     '''
#     测试准确率
#     :param dataArr:测试集
#     :param labelArr: 测试集标签
#     :param w: 训练获得的权重w
#     :param b: 训练获得的偏置b
#     :return: 正确率
#     '''
#     print('start to test')
#     # 将数据集转换为矩阵形式方便运算
#     dataMat = np.mat(dataArr)
#     #将label转换为矩阵并转置
#     labelMat = np.mat(labelArr).T

#     #获取测试数据集矩阵的大小
#     m, n = np.shape(dataMat)
#     #错误样本数计数
#     errorCnt = 0
#     #预测标签列表
#     predictions = []
#     #遍历所有测试样本
#     for i in range(m):
#         #获得单个样本向量
#         xi = dataMat[i]
#         #获得该样本标记
#         yi = labelMat[i]
#         #获得运算结果
#         result = -1 * yi * (w * xi.T + b)
#         #进行预测
#         prediction = 1 if w * xi.T + b >= 0 else -1
#         predictions.append(prediction)
#         #如果-yi(w*xi+b)>=0，说明该样本被误分类，错误样本数加一
#         if result >= 0:
#             errorCnt += 1
#     #正确率 = 1 - （样本分类错误数 / 样本总数）
#     accuracy = 1 - (errorCnt / m)
#     #计算精确率、召回率和F1值
#     precision = precision_score(labelArr, predictions)
#     recall = recall_score(labelArr, predictions)
#     f1 = f1_score(labelArr, predictions)
#     return accuracy, precision, recall, f1

# if __name__ == '__main__':
#     # 初始化WandB
#     wandb.init(project="mnist_perceptron", name="perceptron_run")
#     # 获取当前时间
#     start = time.time()

#     #获取训练集及标签
#     trainData, trainLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_train.csv")
#     #获取测试集及标签
#     testData, testLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_test.csv")

#     #训练获得权重
#     w, b = perceptron(trainData, trainLabel, iter=30)
#     #进行测试，获得评估指标
#     accuracy, precision, recall, f1 = model_test(testData, testLabel, w, b)

#     # 记录评估指标到WandB
#     wandb.log({
#         "accuracy": accuracy,
#         "precision": precision,
#         "recall": recall,
#         "f1_score": f1
#     })

#     # 绘制柱状图
#     metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
#     values = [accuracy, precision, recall, f1]
#     plt.bar(metrics, values)
#     plt.xlabel('Metrics')
#     plt.ylabel('Values')
#     plt.title('Performance Metrics of Perceptron on MNIST')
#     plt.show()

#     #获取当前时间，作为结束时间
#     end = time.time()
#     #显示正确率
#     print('accuracy rate is:', accuracy)
#     print('precision:', precision)
#     print('recall:', recall)
#     print('f1_score:', f1)
#     #显示用时时长
#     print('time span:', end - start)
#     #结束WandB运行
#     wandb.finish()







import numpy as np
import time
from sklearn.metrics import precision_score, recall_score, f1_score
import wandb
import matplotlib.pyplot as plt

def loadData(fileName):
    '''
    加载Mnist数据集
    :param fileName:要加载的数据集路径
    :return: list形式的数据集及标记
    '''
    print('start to read data')
    # 存放数据及标记的list
    dataArr = []
    labelArr = []
    # 打开文件
    fr = open(fileName, 'r')
    # 将文件按行读取
    for line in fr.readlines():
        # 对每一行数据进行切割，返回字段列表
        curLine = line.strip().split(',')

        # Mnsit有0 - 9十个标记，由于是二分类任务，所以将>=5的作为1，<5为 - 1
        if int(curLine[0]) >= 5:
            labelArr.append(1)
        else:
            labelArr.append(-1)
        # 存放标记
        # [int(num) for num in curLine[1:]] -> 遍历每一行中除了以第一个元素（标记）外将所有元素转换成int类型
        # [int(num)/255 for num in curLine[1:]] -> 将所有数据除255归一化(非必须步骤，可以不归一化)
        dataArr.append([int(num) / 255 for num in curLine[1:]])

    # 返回data和label
    return dataArr, labelArr

def perceptron(dataArr, labelArr, iter=50):
    '''
    感知器训练过程
    :param dataArr:训练集的数据 (list)
    :param labelArr: 训练集的标签(list)
    :param iter: 迭代次数,默认30
    :return: 训练好的w和b
    '''
    print('start to trans')
    # 将数据转换成矩阵形式（在机器学习中因为通常都是向量的运算，转换称矩阵形式方便运算）
    # 转换后的数据中每一个样本的向量都是横向的
    dataMat = np.mat(dataArr)
    # 将标签转换成矩阵，之后转置(.T为转置)。
    # 转置是因为在运算中需要单独取label中的某一个元素，如果是Nx1的矩阵的话，无法用label[i]的方式读取
    # 对于只有1xN的label可以不转换成矩阵，直接label[i]即可，这里转换是为了格式上的统一
    labelMat = np.mat(labelArr).T
    # 获取数据矩阵的大小，为m*n
    m, n = np.shape(dataMat)
    # 创建初始权重w，初始值全为0。
    # np.shape(dataMat)的返回值为m，n -> np.shape(dataMat)[1])的值即为n，与
    # 样本长度保持一致
    w = np.zeros((1, np.shape(dataMat)[1]))
    # 初始化偏置b为0
    b = 0
    # 初始化步长，也就是梯度下降过程中的n，控制梯度下降速率
    h = 0.0001

    accuracies = []  # 用于记录每次迭代后的准确率

    # 进行iter次迭代计算
    for k in range(iter):
        # 对于每一个样本进行梯度下降
        for i in range(m):
            # 获取当前样本的向量
            xi = dataMat[i]
            # 获取当前样本所对应的标签
            yi = labelMat[i]
            # 判断是否是误分类样本
            if -1 * yi * (w * xi.T + b) >= 0:
                # 对于误分类样本，进行梯度下降，更新w和b
                w = w + h * yi * xi
                b = b + h * yi

        # 计算当前迭代的准确率
        predictions = []
        for i in range(m):
            xi = dataMat[i]
            prediction = 1 if w * xi.T + b >= 0 else -1
            predictions.append(prediction)
        correct = sum([1 for p, l in zip(predictions, labelArr) if p == l])
        accuracy = correct / m
        accuracies.append(accuracy)

        # 打印训练进度
        print('Round %d:%d training, accuracy: %.4f' % (k, iter, accuracy))

    # 返回训练完的w、b和每次迭代的准确率
    return w, b, accuracies

def model_test(dataArr, labelArr, w, b):
    '''
    测试准确率
    :param dataArr:测试集
    :param labelArr: 测试集标签
    :param w: 训练获得的权重w
    :param b: 训练获得的偏置b
    :return: 正确率
    '''
    print('start to test')
    #将数据集转换为矩阵形式方便运算
    dataMat = np.mat(dataArr)
    #将label转换为矩阵并转置
    labelMat = np.mat(labelArr).T

    #获取测试数据集矩阵的大小
    m, n = np.shape(dataMat)
    #错误样本数计数
    errorCnt = 0
    #预测标签列表
    predictions = []
    #遍历所有测试样本
    for i in range(m):
        #获得单个样本向量
        xi = dataMat[i]
        #获得该样本标记
        yi = labelMat[i]
        #获得运算结果
        result = -1 * yi * (w * xi.T + b)
        #进行预测
        prediction = 1 if w * xi.T + b >= 0 else -1
        predictions.append(prediction)
        #如果-yi(w*xi+b)>=0，说明该样本被误分类，错误样本数加一
        if result >= 0:
            errorCnt += 1
    #正确率 = 1 - （样本分类错误数 / 样本总数）
    accuracy = 1 - (errorCnt / m)
    #计算精确率、召回率和F1值
    precision = precision_score(labelArr, predictions)
    recall = recall_score(labelArr, predictions)
    f1 = f1_score(labelArr, predictions)
    return accuracy, precision, recall, f1

if __name__ == '__main__':
    # 初始化WandB
    wandb.init(project="mnist_perceptron", name="perceptron_run")
    # 获取当前时间
    start = time.time()

    #获取训练集及标签
    trainData, trainLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_train.csv")
    #获取测试集及标签
    testData, testLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_test.csv")

    #训练获得权重
    w, b, accuracies = perceptron(trainData, trainLabel, iter=30)
    #进行测试，获得评估指标
    accuracy, precision, recall, f1 = model_test(testData, testLabel, w, b)

    # 记录评估指标到WandB
    wandb.log({
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    })

    # 绘制柱状图
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    values = [accuracy, precision, recall, f1]
    plt.bar(metrics, values)
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.title('Performance Metrics of Perceptron on MNIST')
    plt.show()

    # 绘制折线图展示训练过程中的准确率变化
    plt.plot(range(1, len(accuracies) + 1), accuracies)
    plt.xlabel('Iteration')
    plt.ylabel('Accuracy')
    plt.title('Training Accuracy Over Iterations')
    plt.show()

    #获取当前时间，作为结束时间
    end = time.time()
    #显示正确率
    print('accuracy rate is:', accuracy)
    print('precision:', precision)
    print('recall:', recall)
    print('f1_score:', f1)
    #显示用时时长
    print('time span:', end - start)
    #结束WandB运行
    wandb.finish()