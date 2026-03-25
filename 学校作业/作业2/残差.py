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

import torch.nn.functional as F

wandb.init(project='Res_net')

trans = transforms.Compose([
    transforms.ToTensor()
])

train_set = torchvision.datasets.MNIST(
    root="./data",
    train=True,
    transform=trans,
    download=True
)

print(train_set.data.shape, train_set.targets.shape)

test_set = torchvision.datasets.MNIST(
    root="./data",
    train=False,
    transform=trans,
    download=True
)

print(test_set.data.shape, test_set.targets.shape)

sample_idx = 0
image_tensor, label = train_set[sample_idx]

image = image_tensor.squeeze().numpy()
mean = 0.1307
std = 0.3081
image = image * std + mean

image = np.clip(image * 255, 0, 255).astype('uint8')

# 可视化
plt.figure(figsize=(5,5))
plt.imshow(image, cmap='gray')
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


# 定义残差块
class Residual(nn.Module):
    def __init__(self, input_channels, num_channels, use_1x1conv=False, strides=1):
        super().__init__()
        self.conv1 = nn.Conv2d(input_channels, num_channels,
                               kernel_size=3, padding=1, stride=strides)
        self.conv2 = nn.Conv2d(num_channels, num_channels, kernel_size=3, padding=1)
        if use_1x1conv:
            self.conv3 = nn.Conv2d(input_channels, num_channels, kernel_size=1, stride=strides)
        else:
            self.conv3 = None
        self.bn1 = nn.BatchNorm2d(num_channels)
        self.bn2 = nn.BatchNorm2d(num_channels)

    def forward(self, X):
        Y = F.relu(self.bn1(self.conv1(X)))
        Y = self.bn2(self.conv2(Y))
        if self.conv3:
            X = self.conv3(X)
        Y += X
        return F.relu(Y)

# 定义残差块构建函数
def resnet_block(input_channels, num_channels, num_residuals, use_1x1conv=True, strides=2):
    blk = []
    for i in range(num_residuals):
        if i == 0:
            blk.append(Residual(input_channels, num_channels,
                                use_1x1conv=use_1x1conv, strides=strides))
        else:
            blk.append(Residual(num_channels, num_channels,
                                use_1x1conv=False, strides=1))
    return blk

# 定义完整的残差网络
class ResNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )
        self.net.extend(resnet_block(64, 64, 2, use_1x1conv=False, strides=1))
        self.net.extend(resnet_block(64, 128, 2, use_1x1conv=True, strides=2))
        self.net.extend(resnet_block(128, 256, 2, use_1x1conv=True, strides=2))
        self.net.extend(resnet_block(256, 512, 2, use_1x1conv=True, strides=2))
        self.net.add_module("global_avg_pool", nn.AdaptiveAvgPool2d((1, 1)))
        self.net.add_module("flatten", nn.Flatten())
        self.net.add_module("fc", nn.Linear(512, 10))

    def forward(self, x):
        return self.net(x)

# b1 = nn.Sequential(
#     nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3),
#     nn.BatchNorm2d(64),
#     nn.ReLU(),
#     nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
# )

# b2 = nn.Sequential(
#     resnet_block(64, 64, 2, use_1x1conv=True, strides=1),
#     resnet_block(64, 128, 2, use_1x1conv=True, strides=2)
# )

# b3 = nn.Sequential(
#     resnet_block(128, 128, 2, use_1x1conv=True, strides=1),
#     resnet_block(128, 256, 2, use_1x1conv=True, strides=2)
# )

# b4 = nn.Sequential(
#     resnet_block(256, 256, 2, use_1x1conv=True, strides=1),
#     resnet_block(256, 512, 2, use_1x1conv=True, strides=2)
# )

# b5 = nn.Sequential(
#     resnet_block(512, 512, 2, use_1x1conv=True, strides=1),
#     resnet_block(512, 512, 2, use_1x1conv=True, strides=2)
# )

# class Model_ResNet18(nn.Module):
#     def __init__(self, in_channels=1, num_classes=10):
#         super().__init__()
#         self.net = nn.Sequential(
#             nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3),
#             nn.BatchNorm2d(64),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
#             b1,
#             b2,
#             b3,
#             b4,
#             b5,
#             nn.AdaptiveAvgPool2d((1, 1)),
#             nn.Flatten(),
#             nn.Linear(512, num_classes)
#         )


# 初始化模型
model = ResNet()

# 初始化权重
def init_weights(m):
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        nn.init.xavier_uniform_(m.weight)
model.apply(init_weights)

# 训练配置
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 记录训练过程的指标
history1 = hl.History()
# 使用 Canvas 进行可视化
canvas1 = hl.Canvas()

# 训练模型
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for step, (images, labels) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = model(images)
        train_loss = criterion(outputs, labels)
        train_loss.backward()
        optimizer.step()

    pred = outputs.argmax(dim=1)
    correct = (pred == labels).sum().item()
    train_accuracy = correct / labels.size(0)

    model.eval()
    total_correct = 0
    total_loss = 0
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            predicted = outputs.argmax(dim=1)
            total_correct += (predicted == labels).sum().item()
            total_loss += loss.item() * labels.size(0)

    test_acc = total_correct / len(test_set)
    test_loss = total_loss / len(test_set)

    # 记录指标
    history1.log(
        epoch=epoch + 1,
        step=(epoch + 1) * len(train_loader),
        train_loss=train_loss.item(),
        train_accuracy=train_accuracy,
        test_loss=test_loss,
        test_accuracy=test_acc
    )

    wandb.log({
        "train_loss": train_loss.item(),
        "train_accuracy": train_accuracy,
        "test_loss": test_loss,
        "test_accuracy": test_acc
    })

    # 打印每个 epoch 的指标
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

    print(f'Epoch {epoch + 1}, '
          f'Train Loss: {train_loss.item():.4f},  Train Accuracy: {train_accuracy:.2%} '
          f'Test Loss: {test_loss:.4f},  Test Accuracy: {test_acc:.2%}')

# 结束 wandb 记录
wandb.finish()