import torch
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

# 设置随机种子以确保结果可复现
torch.manual_seed(42)
np.random.seed(42)

# 创建dataset实例
dataset = datasets.ImageFolder(
    'Cross',
    transforms.Compose([
        transforms.ColorJitter(0.1, 0.1, 0.1, 0.1),
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),  # 增加数据增强
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
)

# 更合理的训练集和测试集划分方式
train_indices, test_indices = train_test_split(
    list(range(len(dataset))), 
    test_size=100, 
    stratify=dataset.targets,  # 保持类别比例
    random_state=42
)

train_dataset = torch.utils.data.Subset(dataset, train_indices)
test_dataset = torch.utils.data.Subset(dataset, test_indices)

# 数据加载器
train_loader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True,
    num_workers=4,
    pin_memory=True  # 加速数据转移到GPU
)

test_loader = torch.utils.data.DataLoader(
    test_dataset,
    batch_size=16,
    shuffle=False,  # 测试集不需要shuffle
    num_workers=4,
    pin_memory=True
)

# 定义模型 - 使用ResNet18替代AlexNet（更现代的架构）
model = models.resnet18(pretrained=True)
num_features = model.fc.in_features
model.fc = torch.nn.Linear(num_features, 2)  # 二分类问题

# 使用GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 训练参数
NUM_EPOCHS = 30
BEST_MODEL_PATH = 'Cross.pth'
best_accuracy = 0.0

# 优化器和学习率调度器
optimizer = optim.Adam(model.parameters(), lr=0.001)  # 使用Adam优化器
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)  # 学习率衰减

# 记录训练过程
train_losses = []
test_accuracies = []

for epoch in range(NUM_EPOCHS):
    # 训练阶段
    model.train()
    running_loss = 0.0
    
    print(f'Epoch {epoch+1}/{NUM_EPOCHS} [Training]')
    
    for batch_idx, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = F.cross_entropy(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * images.size(0)
        
        # 每10个batch打印一次损失
        if batch_idx % 10 == 0:
            print(f'Batch {batch_idx}, Loss: {loss.item():.4f}')
    
    epoch_loss = running_loss / len(train_dataset)
    train_losses.append(epoch_loss)
    
    # 评估阶段
    model.eval()
    correct = 0
    total = 0
    
    print(f'Epoch {epoch+1}/{NUM_EPOCHS} [Evaluating]')
    
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    test_accuracy = correct / total
    test_accuracies.append(test_accuracy)
    
    print(f'Epoch {epoch+1}/{NUM_EPOCHS}, Loss: {epoch_loss:.4f}, Test Accuracy: {test_accuracy:.4f}')
    
    # 学习率调整
    scheduler.step()
    
    # 保存最佳模型
    if test_accuracy > best_accuracy:
        torch.save(model.state_dict(), BEST_MODEL_PATH)
        best_accuracy = test_accuracy
        print(f'New best model saved with accuracy: {best_accuracy:.4f}')

# 绘制训练曲线
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(test_accuracies, label='Test Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('training_curve.png')
plt.show()

print(f'Best accuracy: {best_accuracy:.4f}')




import torch
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

# 设置随机种子以确保结果可复现
torch.manual_seed(42)
np.random.seed(42)

# 创建dataset实例
dataset = datasets.ImageFolder(
    'BLOCKING',
    transforms.Compose([
        transforms.ColorJitter(0.1, 0.1, 0.1, 0.1),
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),  # 增加数据增强
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
)

# 更合理的训练集和测试集划分方式
train_indices, test_indices = train_test_split(
    list(range(len(dataset))), 
    test_size=100, 
    stratify=dataset.targets,  # 保持类别比例
    random_state=42
)

train_dataset = torch.utils.data.Subset(dataset, train_indices)
test_dataset = torch.utils.data.Subset(dataset, test_indices)

# 数据加载器
train_loader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True,
    num_workers=4,
    pin_memory=True  # 加速数据转移到GPU
)

test_loader = torch.utils.data.DataLoader(
    test_dataset,
    batch_size=16,
    shuffle=False,  # 测试集不需要shuffle
    num_workers=4,
    pin_memory=True
)

# 定义模型 - 使用ResNet18替代AlexNet（更现代的架构）
model = models.resnet18(pretrained=True)
num_features = model.fc.in_features
model.fc = torch.nn.Linear(num_features, 2)  # 二分类问题

# 使用GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# 训练参数
NUM_EPOCHS = 30
BEST_MODEL_PATH = 'BLOCKING.pth'
best_accuracy = 0.0

# 优化器和学习率调度器
optimizer = optim.Adam(model.parameters(), lr=0.001)  # 使用Adam优化器
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)  # 学习率衰减

# 记录训练过程
train_losses = []
test_accuracies = []

for epoch in range(NUM_EPOCHS):
    # 训练阶段
    model.train()
    running_loss = 0.0
    
    print(f'Epoch {epoch+1}/{NUM_EPOCHS} [Training]')
    
    for batch_idx, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = F.cross_entropy(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * images.size(0)
        
        # 每10个batch打印一次损失
        if batch_idx % 10 == 0:
            print(f'Batch {batch_idx}, Loss: {loss.item():.4f}')
    
    epoch_loss = running_loss / len(train_dataset)
    train_losses.append(epoch_loss)
    
    # 评估阶段
    model.eval()
    correct = 0
    total = 0
    
    print(f'Epoch {epoch+1}/{NUM_EPOCHS} [Evaluating]')
    
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    test_accuracy = correct / total
    test_accuracies.append(test_accuracy)
    
    print(f'Epoch {epoch+1}/{NUM_EPOCHS}, Loss: {epoch_loss:.4f}, Test Accuracy: {test_accuracy:.4f}')
    
    # 学习率调整
    scheduler.step()
    
    # 保存最佳模型
    if test_accuracy > best_accuracy:
        torch.save(model.state_dict(), BEST_MODEL_PATH)
        best_accuracy = test_accuracy
        print(f'New best model saved with accuracy: {best_accuracy:.4f}')

# 绘制训练曲线
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='模型损失')
plt.xlabel('训练轮次')
plt.ylabel('损失')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(test_accuracies, label='模型准确率')
plt.xlabel('训练轮次')
plt.ylabel('精确率')
plt.legend()
plt.savefig('training_curve.png')
plt.show()

print(f'精确率: {best_accuracy:.4f}')




