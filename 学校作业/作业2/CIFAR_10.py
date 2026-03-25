import torch
import torch.nn as nn
import torchvision
from torch.utils.data import DataLoader
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np
import wandb
import torch.nn.functional as F
import time

# 初始化wandb项目
wandb.init(project="CIFAR_CNN")

# 数据预处理
trans = transforms.Compose([
    transforms.ToTensor()
])

# 加载训练集
train_set = torchvision.datasets.CIFAR10(
    root="./data",
    train=True,
    transform=trans,
    download=True
)
print(train_set.data.shape, len(train_set.targets))

# 加载测试集
test_set = torchvision.datasets.CIFAR10(
    root="./data",
    train=False,
    transform=trans,
    download=True
)
print(test_set.data.shape, len(test_set.targets))

# 可视化其中一张图像和标签
sample_idx = 0  # 可修改为其他索引值观察不同样本 
image_tensor, label = train_set[sample_idx]

# 反归一化处理（恢复原始像素范围）
# 将通道维度移到最后一维，因为matplotlib显示图像时通道维度在最后
image = image_tensor.permute(1, 2, 0).numpy()
# 将像素值从[0, 1]恢复到[0, 255]并转换为无符号8位整数
image = (image * 255).astype('uint8')  

# 可视化设置 
plt.figure(figsize=(5, 5))
# 由于是彩色图像，不需要指定 cmap='gray'
plt.imshow(image)
plt.title(f"Label:  {label}", fontsize=14)
plt.axis('off')

# 保存与显示 
plt.savefig('cifar10-sample.pdf', bbox_inches='tight', dpi=300)
plt.show()

print(f"样本索引: {sample_idx}")
print(f"实际标签: {label}")
print(f"图像尺寸: {image.shape}")
print(f"像素范围: [{image.min()},  {image.max()}]")

# 定义数据加载器
# 训练数据加载器，增大batch_size以减少迭代次数
train_loader = DataLoader(train_set, batch_size=256, shuffle=True)
# 测试数据加载器，batch_size设置为64，不打乱数据顺序
test_loader = DataLoader(test_set, batch_size=64, shuffle=False)

# 加载预训练的ResNet18模型
from torchvision.models.resnet import ResNet18_Weights
model = torchvision.models.resnet18(weights=ResNet18_Weights.DEFAULT)
# 修改最后一层全连接层以适配CIFAR - 10的10个类别
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 10)

# 检查是否有可用的GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

# 定义损失函数和优化器，使用Adam优化器
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

# 记录训练过程的指标
history1 = {}

# 记录训练开始时间
start_time = time.time()

# 训练模型，减少训练轮数
num_epochs = 20
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct_train = 0
    total_train = 0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        train_loss = criterion(outputs, labels)
        train_loss.backward()
        optimizer.step()
        running_loss += train_loss.item()
        # 计算训练集上当前batch的正确预测数
        _, predicted = torch.max(outputs.data, 1)
        total_train += labels.size(0)
        correct_train += (predicted == labels).sum().item()
    # 计算每个epoch的平均训练损失
    epoch_train_loss = running_loss / len(train_loader)
    # 计算每个epoch的训练准确率
    train_accuracy = correct_train / total_train

    # 验证评估 
    model.eval() 
    total_correct = 0 
    total_loss = 0
    with torch.no_grad(): 
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            predicted = outputs.argmax(dim=1)
            total_correct += (predicted == labels).sum().item()
            total_loss += loss.item()  * labels.size(0) 
    # 计算测试集上的准确率和平均损失
    test_acc = total_correct / len(test_set)
    test_loss = total_loss / len(test_set)

    # 记录指标
    if 'train_loss' not in history1:
        history1['train_loss'] = []
        history1['train_accuracy'] = []
        history1['test_loss'] = []
        history1['test_accuracy'] = []

    history1['train_loss'].append(epoch_train_loss)
    history1['train_accuracy'].append(train_accuracy)
    history1['test_loss'].append(test_loss)
    history1['test_accuracy'].append(test_acc)

    wandb.log({
        "train_loss": epoch_train_loss,
        "train_accuracy": train_accuracy,
        "test_loss": test_loss,
        "test_accuracy": test_acc,
    })

    # 打印每个epoch的指标
    print(f'Epoch {epoch+1}, '
          f'Train Loss: {epoch_train_loss:.4f},  Train Accuracy: {train_accuracy:.2%} '
          f'Test Loss: {test_loss:.4f},  Test Accuracy: {test_acc:.2%}')

# 记录训练结束时间
end_time = time.time()
# 计算训练总时间
training_time = end_time - start_time
print(f"Total training time: {training_time:.2f} seconds")

# 绘制损失曲线
train_loss = history1['train_loss']
test_loss = history1['test_loss']
epochs = range(1, len(train_loss) + 1)

plt.plot(epochs, train_loss, label='Train Loss')
plt.plot(epochs, test_loss, label='Test Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Test Loss')
plt.legend()
plt.show()

# 绘制准确率曲线
train_accuracy = history1['train_accuracy']
test_accuracy = history1['test_accuracy']

plt.plot(epochs, train_accuracy, label='Train Accuracy')
plt.plot(epochs, test_accuracy, label='Test Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Test Accuracy')
plt.legend()
plt.show()

# 结束wandb记录
wandb.finish()    