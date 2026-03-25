# %%
import torch
import torch.nn as nn
import torchvision
from torch.utils.data import DataLoader
from torchvision import transforms

import matplotlib.pyplot  as plt 
import numpy as np

import hiddenlayer as hl

import wandb


wandb.init(project="MNIST_CNN")

# %% 数据集加载
# trans = transforms.Compose([
#     transforms.ToTensor(),
#     torchvision.transforms.Normalize((0.1307,),  (0.3081,))])

trans = transforms.Compose([
    transforms.ToTensor()])  # 变成张量

# 直接用这个数据集
train_set=torchvision.datasets.MNIST(
    root="./data",
    train=True,    # 下载训练集
    transform=trans,   # 数据预处理
    download=True
)

print(train_set.data.shape,train_set.targets.shape)

test_set=torchvision.datasets.MNIST(
    root="./data",
    train=False,   # 下载测试集
    transform=trans,
    download=True
)
print(test_set.data.shape,test_set.targets.shape)

# %% 可视化其中一张图像和标签
sample_idx = 0  # 可修改为其他索引值观察不同样本 
image_tensor, label = train_set[sample_idx]

# 反归一化处理（恢复原始像素范围）
image = image_tensor.squeeze().numpy()   # 去除通道维度 [1,28,28] -> [28,28]
# mean = 0.1307 
# std = 0.3081 
# image = (image * std) + mean  # 恢复归一化前的数值范围 
image = np.clip(image  * 255, 0, 255).astype('uint8')  # 转换为8位像素值 
 
# 可视化设置 
plt.figure(figsize=(5,5)) 
plt.imshow(image,  cmap='gray')
plt.title(f"Label:  {label}", fontsize=14)
plt.axis('off') 

# 保存与显示 
plt.savefig('mnist-sample.pdf',  bbox_inches='tight', dpi=300)
plt.show() 
 
print(f"样本索引: {sample_idx}")
print(f"实际标签: {label}")
print(f"图像尺寸: {image.shape}") 
print(f"像素范围: [{image.min()},  {image.max()}]") 


# %% 数据加载器
# 数据加载器 
train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
test_loader = DataLoader(test_set, batch_size=1000, shuffle=False)

# %% LeNet-5卷积神经网路构建
# model = nn.Sequential(
#     nn.Conv2d(1, 6, kernel_size=5, padding=2), nn.Sigmoid(),
#     nn.AvgPool2d(kernel_size=2, stride=2),
#     nn.Conv2d(6, 16, kernel_size=5), nn.Sigmoid(),
#     nn.AvgPool2d(kernel_size=2, stride=2),
#     nn.Flatten(),
#     nn.Linear(16 * 5 * 5, 120), nn.Sigmoid(),
#     nn.Linear(120, 84), nn.Sigmoid(),
#     nn.Linear(84, 10))

class MNIST_CNN(nn.Module):
    def __init__(self):
        # 调用父类 nn.Module 的构造函数
        super().__init__()
        # 定义神经网络的层结构
        self.net = nn.Sequential(
            # 第一个卷积层：输入通道数为 1（灰度图像），输出通道数为 6，卷积核大小为 5x5，填充为 2
            nn.Conv2d(1, 6, kernel_size=5, padding=2),
            # 激活函数：Sigmoid
            nn.ReLU(),
            # 平均池化层：池化核大小为 2x2，步长为 2
            nn.AvgPool2d(kernel_size=2, stride=2),
            # 第二个卷积层：输入通道数为 6，输出通道数为 16，卷积核大小为 5x5
            nn.Conv2d(6, 16, kernel_size=5),
            # 激活函数：Sigmoid
            nn.Sigmoid(),
            # 平均池化层：池化核大小为 2x2，步长为 2
            nn.AvgPool2d(kernel_size=2, stride=2),
            # 将多维的输入一维化，方便后续全连接层处理
            nn.Flatten(),
            # 第一个全连接层：输入特征数为 16*5*5，输出特征数为 120
            nn.Linear(16 * 5 * 5, 120),
            # 激活函数：Sigmoid
            nn.Sigmoid(),
            # 第二个全连接层：输入特征数为 120，输出特征数为 84
            nn.Linear(120, 84),
            # 激活函数：Sigmoid
            nn.Sigmoid(),
            # 第三个全连接层：输入特征数为 84，输出特征数为 10（对应 10 个数字类别）
            nn.Linear(84, 10)
        )


    def forward(self,x):
        return self.net(x)
    
# 打印每一层的形状
LeNet5=MNIST_CNN() 
X = torch.randn(size=(1, 1, 28, 28), dtype=torch.float32)
layers=list(LeNet5.net)
for layer in layers:
    X = layer(X)
    print(layer.__class__.__name__,'output shape: \t',X.shape)

    
# %% 模型训练
model = MNIST_CNN()

# 初始化
def init_weights(m):
    if type(m)==nn.Linear or type(m)==nn.Conv2d:
        # nn.init.normal_(m.weight,std=0.01)
        nn.init.xavier_uniform_(m.weight)# 从均值为0，方差为sigma^2=2/(nin+nout)的高斯分布中抽样权重，也可以改为从均匀分布中抽样权重，U(-sqrt(6/(nin+nout)),sqrt(6/(nin+nout)))
model.apply(init_weights)

# 训练配置
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 记录训练过程的指标
history1=hl.History()
# 使用Canvas进行可视化
canvas1=hl.Canvas()

# 训练模型
num_epochs = 10  # 定义训练的轮数
for epoch in range(num_epochs):
    model.train() 
    # 对训练数据的加载器进行迭代计算
    for step, (images, labels) in enumerate(train_loader):
        # 前向传播
        optimizer.zero_grad() 
        outputs = model(images)
        train_loss = criterion(outputs, labels)
        train_loss.backward() 
        optimizer.step() 

    pred = outputs.argmax(dim=1)   # 获取预测类别 
    correct = (pred == labels).sum().item()  # 计算正确预测数 
    train_accuracy = correct / labels.size(0)   # 计算batch准确率 
    
    # 验证评估 
    model.eval() 
    total_correct = 0 
    total_loss=0
    with torch.no_grad(): 
        for images, labels in test_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            predicted = outputs.argmax(dim=1)
            total_correct += (predicted == labels).sum().item()
            total_loss += loss.item()  * labels.size(0) 
    
    test_acc = total_correct / len(test_set)
    test_loss=total_loss/len(test_set)

    # 记录指标
    history1.log(    
        epoch=epoch+1,
        step=(epoch+1)*len(train_loader),
        train_loss=train_loss.item(), 
        train_accuracy=train_accuracy,
        test_loss=test_loss,
        test_accuracy=test_acc 
    )

    wandb.log({
        "train_loss": train_loss.item(),
        "train_accuracy": train_accuracy,
        "test_loss": test_loss,
        "test_accuracy": test_acc,
    })


    # 打印每个epoch的指标
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

    print(f'Epoch {epoch+1}, '
            f'Train Loss: {train_loss.item():.4f},  Train Accuracy: {train_accuracy:.2%} '
            f'Test Loss: {test_loss:.4f},  Test Accuracy: {test_acc:.2%}')

# %%

wandb.finish()

# %%