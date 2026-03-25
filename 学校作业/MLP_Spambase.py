# # %%
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler, MinMaxScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# import matplotlib.pyplot as plt
# import seaborn as sns

# import torch
# import torch.nn as nn
# from torch.optim import SGD, Adam
# import torch.utils.data as Data

# import hiddenlayer as hl
# from torchviz import make_dot

# # %% 特征名称读取
# columns = []

# with open('F://PycharmProjects//pythonProject//深度学习//学校作业//spambase//spambase.names', 'r') as f:
# # with open('./spambase/spambase.names',  'r') as f:
#     for line in f:
#         if line[0]=='|':
#             continue
#         line = line.strip() 
#         # 检查是否包含特征名前缀
#         if any(prefix in line for prefix in ['word_freq_', 'char_freq_', 'capital_run_length_']):
#             # 提取特征名部分
#             col_part = line.split(':',  1)[0].strip()  # 分割冒号前的部分
#             columns.append(col_part) 
# print(columns)


# # %% 读取数据文件
# spam = pd.read_csv( 
#     # './spambase/spambase.data', 
#     'F://PycharmProjects//pythonProject//深度学习//学校作业//spambase//spambase.names',
#     header=None,
#     names=columns + ['label'],  # 确保包含最后的分类标签 
#     sep=',',
#     engine='python'
# )
# spam.head()
# # %% 计算垃圾邮件和非垃圾邮件的数量
# pd.value_counts(spam.label)

# # %% 将数据随机切分为训练集和测试集
# X = spam.iloc[:, 0:57].values
# y = spam.label.values
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=123)

# # %% 对数据的前57列特征进行数据标准化处理
# scales = MinMaxScaler(feature_range=(0, 1))
# X_train_s = scales.fit_transform(X_train)
# X_test_s = scales.transform(X_test)

# # %%
# # 将训练数据集的每个特征变量使用箱线图进行显示
# colname = spam.columns.values[:-1]
# plt.figure(figsize=(20, 14))
# for ii in range(len(colname)):
#     plt.subplot(7, 9, ii + 1)
#     sns.boxplot(x=y_train, y=X_train_s[:, ii])
#     plt.title(colname[ii])

# plt.subplots_adjust(hspace=0.4)
# plt.show()

# # %%
# class MLPclassifica(nn.Module):
#     def __init__(self):
#         super(MLPclassifica, self).__init__()
#         ## 定义第一个隐藏层
#         self.hidden1 = nn.Sequential(
#             nn.Linear(
#                 in_features=57,  # 第一个隐藏层的输入，数据的特征数
#                 out_features=30,  # 第一个隐藏层的输出，神经元的数量
#                 bias=True,  # 默认会有偏置
#             ),
#             nn.ReLU(),
#         )
#         ## 定义第二个隐藏层
#         self.hidden2 = nn.Sequential(
#             nn.Linear(30, 10),
#             nn.ReLU(),
#         )
#         ## 分类层
#         self.classifica = nn.Sequential(
#             nn.Linear(10, 2),
#             nn.Sigmoid(),
#         )
#     ## 定义网络的前向传播过程
#     def forward(self, x):
#         fc1 = self.hidden1(x)
#         fc2 = self.hidden2(fc1)
#         output = self.classifica(fc2)
#         ## 输出为两个隐藏层和输出层
#         return fc1, fc2, output
# # %% 输出网络结构
# mlpc=MLPclassifica()
# x=torch.randn(1,57).requires_grad_(True)
# y=mlpc(x)
# Mymlpcvis=make_dot(y, params=dict(list(mlpc.named_parameters())+[('x',x)]))
# Mymlpcvis                   

# # %%------------------------训练模型-----------------------------
# ## 将数据转化为张量
# # X_train_t = torch.from_numpy(X_train_s.astype(np.float32))
# X_train_t = torch.from_numpy(X_train.astype(np.float32))
# y_train_t = torch.from_numpy(y_train.astype(np.int64))
# # X_test_t = torch.from_numpy(X_test_s.astype(np.float32))
# X_test_t = torch.from_numpy(X_test.astype(np.float32))
# y_test_t = torch.from_numpy(y_test.astype(np.int64))

# ## 将训练集转化为张量后，使用 TensorDataset 将 X 和 y 整理到一起
# # 1) 定义一个数据集的加载器，将数据集分为训练集和测试集，使用 DataLoader 将其转化为批量的张量
# train_data = Data.TensorDataset(X_train_t, y_train_t)  # 定义数据集
# train_loader = Data.DataLoader(
#     dataset=train_data,  # 使用数据集
#     batch_size=64,  # 每批处理64个样本
#     shuffle=True,  # 每个epoch后打乱数据
#     num_workers=0  # 数据加载在主进程（即训练进程）中同步执行
# )

# test_data = Data.TensorDataset(X_test_t, y_test_t)
# test_loader = Data.DataLoader(
#     dataset=test_data,
#     batch_size=256,  
#     shuffle=False,
#     num_workers=0 
# )


# def evaluate(model, data_loader):
#     model.eval()   # 切换到评估模式 
#     total_correct = 0 
#     total_loss = 0.0 
#     with torch.no_grad():   # 禁用梯度计算 
#         for X_batch, y_batch in data_loader:
#             _, _, output = model(X_batch)
#             loss = loss_fn(output, y_batch)
#             pred = output.argmax(dim=1) 
#             total_correct += (pred == y_batch).sum().item()
#             total_loss += loss.item()  * X_batch.size(0) 
#     model.train()   # 恢复训练模式 
#     return total_loss / len(data_loader.dataset),  total_correct / len(data_loader.dataset) 

# # 2) 定义损失函数和优化器
# loss_fn = nn.CrossEntropyLoss()  # 定义损失函数为交叉熵
# optimizer = torch.optim.Adam(mlpc.parameters(), lr=0.01)  # 定义优化器为Adam

# # 记录训练过程的指标
# history1=hl.History()
# # 使用Canvas进行可视化
# canvas1=hl.Canvas()

# # 3) 训练模型
# num_epochs = 10  # 定义训练的轮数
# for epoch in range(num_epochs):
#     ## 对训练数据的加载器进行迭代计算
#     for step, (b_x, b_y) in enumerate(train_loader):
#         # 前向传播
#         _,_,output = mlpc(b_x) # MLP在训练batch上的输出
#         train_loss = loss_fn(output, b_y) # 计算每个batch的损失

#         # 计算精度
#         pred = output.argmax(dim=1)   # 获取预测类别 
#         correct = (pred == b_y).sum().item()  # 计算正确预测数 
#         train_accuracy = correct / b_y.size(0)   # 计算batch准确率 

#         # 反向传播和优化
#         optimizer.zero_grad() # 每个迭代步的梯度初始化为0
#         train_loss.backward() # 损失的后向传播，计算梯度
#         optimizer.step() # 使用梯度进行优化

#         test_loss, test_accuracy = evaluate(mlpc, test_loader)

        
#         # 记录指标
#         history1.log( 
#             epoch=epoch+1,
#             step=epoch*len(train_loader)+step,
#             train_loss=train_loss.item(), 
#             train_accuracy=train_accuracy,
#             test_loss=test_loss,
#             test_accuracy=test_accuracy 
#         )

#         # 打印每10个step的指标
#         if (step + 1) % 10 == 0:
#             with canvas1:
#                 canvas1.draw_plot( 
#                     history1["train_loss"], 
#                 )
#                 canvas1.draw_plot( 
#                     history1["test_loss"], 
#                 )             
#                 canvas1.draw_plot( 
#                     history1["train_accuracy"], 
#                 )
#                 canvas1.draw_plot( 
#                     history1["test_accuracy"], 
#                 )
                

#             print(f'Epoch [{epoch+1}/{num_epochs}], Step [{step+1}/{len(train_loader)}], '
#                   f'Train Loss: {train_loss.item():.4f},  Train Accuracy: {train_accuracy:.2%} '
#                   f'Test Loss: {test_loss:.4f},  Test Accuracy: {test_accuracy:.2%}')
            
# # %%






import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
from torch.optim import SGD, Adam
import torch.utils.data as Data

import hiddenlayer as hl
from torchviz import make_dot

# 特征名称读取
columns = []

with open('F://PycharmProjects//pythonProject//深度学习//学校作业//spambase//spambase.names', 'r') as f:
    for line in f:
        if line[0] == '|':
            continue
        line = line.strip()
        # 检查是否包含特征名前缀
        if any(prefix in line for prefix in ['word_freq_', 'char_freq_', 'capital_run_length_']):
            # 提取特征名部分
            col_part = line.split(':', 1)[0].strip()  # 分割冒号前的部分
            columns.append(col_part)

print(columns)

# 读取数据文件
spam = pd.read_csv(
    'F://PycharmProjects//pythonProject//深度学习//学校作业//spambase//spambase.data',
    header=None,
    names=columns + ['label'],  # 确保包含最后的分类标签
    sep=',',
    engine='python'
)
spam.head()

# 计算垃圾邮件和非垃圾邮件的数量
# 修正警告信息
spam['label'].value_counts()

# 将数据随机切分为训练集和测试集
X = spam.iloc[:, 0:57].values
y = spam.label.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=123)

# 对数据的前57列特征进行数据标准化处理
scales = MinMaxScaler(feature_range=(0, 1))
X_train_s = scales.fit_transform(X_train)
X_test_s = scales.transform(X_test)

# 将训练数据集的每个特征变量使用箱线图进行显示
colname = spam.columns.values[:-1]
plt.figure(figsize=(20, 14))
for ii in range(len(colname)):
    plt.subplot(7, 9, ii + 1)
    sns.boxplot(x=y_train, y=X_train_s[:, ii])
    plt.title(colname[ii])

plt.subplots_adjust(hspace=0.4)
plt.show()


class MLPclassifica(nn.Module):
    def __init__(self):
        super(MLPclassifica, self).__init__()
        ## 定义第一个隐藏层
        self.hidden1 = nn.Sequential(
            nn.Linear(
                in_features=57,  # 第一个隐藏层的输入，数据的特征数
                out_features=30,  # 第一个隐藏层的输出，神经元的数量
                bias=True,  # 默认会有偏置
            ),
            nn.ReLU(),
        )
        ## 定义第二个隐藏层
        self.hidden2 = nn.Sequential(
            nn.Linear(30, 10),
            nn.ReLU(),
        )
        ## 分类层
        self.classifica = nn.Sequential(
            nn.Linear(10, 2),
            nn.Sigmoid(),
        )

    ## 定义网络的前向传播过程
    def forward(self, x):
        fc1 = self.hidden1(x)
        fc2 = self.hidden2(fc1)
        output = self.classifica(fc2)
        ## 输出为两个隐藏层和输出层
        return fc1, fc2, output


# 输出网络结构
mlpc = MLPclassifica()
x = torch.randn(1, 57).requires_grad_(True)
y = mlpc(x)
Mymlpcvis = make_dot(y, params=dict(list(mlpc.named_parameters()) + [('x', x)]))
print(Mymlpcvis)

# ------------------------训练模型-----------------------------
## 将数据转化为张量
X_train_t = torch.from_numpy(X_train_s.astype(np.float32))
y_train_t = torch.from_numpy(y_train.astype(np.int64))
X_test_t = torch.from_numpy(X_test_s.astype(np.float32))
y_test_t = torch.from_numpy(y_test.astype(np.int64))

## 将训练集转化为张量后，使用 TensorDataset 将 X 和 y 整理到一起
# 1) 定义一个数据集的加载器，将数据集分为训练集和测试集，使用 DataLoader 将其转化为批量的张量
train_data = Data.TensorDataset(X_train_t, y_train_t)  # 定义数据集
train_loader = Data.DataLoader(
    dataset=train_data,  # 使用数据集
    batch_size=64,  # 每批处理64个样本
    shuffle=True,  # 每个epoch后打乱数据
    num_workers=0  # 数据加载在主进程（即训练进程）中同步执行
)

test_data = Data.TensorDataset(X_test_t, y_test_t)
test_loader = Data.DataLoader(
    dataset=test_data,
    batch_size=256,
    shuffle=False,
    num_workers=0
)


def evaluate(model, data_loader):
    model.eval()  # 切换到评估模式
    total_correct = 0
    total_loss = 0.0
    with torch.no_grad():  # 禁用梯度计算
        for X_batch, y_batch in data_loader:
            _, _, output = model(X_batch)
            loss = loss_fn(output, y_batch)
            pred = output.argmax(dim=1)
            total_correct += (pred == y_batch).sum().item()
            total_loss += loss.item() * X_batch.size(0)
    model.train()  # 恢复训练模式
    return total_loss / len(data_loader.dataset), total_correct / len(data_loader.dataset)


# 2) 定义损失函数和优化器
loss_fn = nn.CrossEntropyLoss()  # 定义损失函数为交叉熵
optimizer = torch.optim.Adam(mlpc.parameters(), lr=0.01)  # 定义优化器为Adam

# 记录训练过程的指标
history1 = hl.History()
# 使用Canvas进行可视化
canvas1 = hl.Canvas()

# 3) 训练模型
num_epochs = 10  # 定义训练的轮数
for epoch in range(num_epochs):
    ## 对训练数据的加载器进行迭代计算
    for step, (b_x, b_y) in enumerate(train_loader):
        # 前向传播
        _, _, output = mlpc(b_x)  # MLP在训练batch上的输出
        train_loss = loss_fn(output, b_y)  # 计算每个batch的损失

        # 计算精度
        pred = output.argmax(dim=1)  # 获取预测类别
        correct = (pred == b_y).sum().item()  # 计算正确预测数
        train_accuracy = correct / b_y.size(0)  # 计算batch准确率

        # 反向传播和优化
        optimizer.zero_grad()  # 每个迭代步的梯度初始化为0
        train_loss.backward()  # 损失的后向传播，计算梯度
        optimizer.step()  # 使用梯度进行优化

        test_loss, test_accuracy = evaluate(mlpc, test_loader)

        # 记录指标
        history1.log(
            epoch=epoch + 1,
            step=epoch * len(train_loader) + step,
            train_loss=train_loss.item(),
            train_accuracy=train_accuracy,
            test_loss=test_loss,
            test_accuracy=test_accuracy
        )

        # 打印每10个step的指标
        if (step + 1) % 10 == 0:
            with canvas1:
                canvas1.draw_plot(
                    history1["train_loss"],
                )
                canvas1.draw_plot(
                    history1["test_loss"],
                )
                canvas1.draw_plot(
                    history1["train_accuracy"],
                )
                canvas1.draw_plot(
                    history1["test_accuracy"],
                )

            print(f'Epoch [{epoch + 1}/{num_epochs}], Step [{step + 1}/{len(train_loader)}], '
                  f'Train Loss: {train_loss.item():.4f},  Train Accuracy: {train_accuracy:.2%} '
                  f'Test Loss: {test_loss:.4f},  Test Accuracy: {test_accuracy:.2%}')