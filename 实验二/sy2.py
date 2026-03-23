
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import os
import time

# ==================== 设置 ====================
# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 解决Windows多进程问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 设置随机种子
torch.manual_seed(42)
np.random.seed(42)

# 检查设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用设备: {device}")

# ==================== 1. MNIST数据加载 ====================
print("\n1. 加载MNIST数据集...")

# 数据预处理
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# 下载数据集
train_dataset = torchvision.datasets.MNIST(
    root='./data', train=True, transform=transform, download=True
)
test_dataset = torchvision.datasets.MNIST(
    root='./data', train=False, transform=transform, download=True
)

# 创建数据加载器
train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=64, shuffle=True, num_workers=0
)
test_loader = torch.utils.data.DataLoader(
    test_dataset, batch_size=64, shuffle=False, num_workers=0
)

print(f"训练集: {len(train_dataset)} 张图像")
print(f"测试集: {len(test_dataset)} 张图像")

# 显示样本
def show_samples():
    fig, axes = plt.subplots(2, 5, figsize=(12, 5))
    for i in range(10):
        img, label = train_dataset[i]
        row, col = i // 5, i % 5
        axes[row, col].imshow(img.squeeze(), cmap='gray')
        axes[row, col].set_title(f'标签: {label}')
        axes[row, col].axis('off')
    plt.suptitle('MNIST手写数字样本')
    plt.tight_layout()
    plt.show()

show_samples()

# ==================== 2. LeNet模型定义 ====================
print("\n2. 定义LeNet模型...")

class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, padding=2)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool(x)
        x = self.relu(self.conv2(x))
        x = self.pool(x)
        x = x.view(-1, 16 * 5 * 5)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

lenet = LeNet().to(device)
print(f"LeNet参数数量: {sum(p.numel() for p in lenet.parameters()):,}")

# ==================== 3. 训练LeNet ====================
print("\n3. 训练LeNet模型...")

def train_model(model, train_loader, test_loader, epochs=5, lr=0.001, model_name="模型"):
    criterion = nn.CrossEntropyLoss()
    
    # 只训练可训练的参数
    trainable_params = [p for p in model.parameters() if p.requires_grad]
    if len(trainable_params) == 0:
        print(f"⚠ {model_name}没有可训练的参数，将跳过训练")
        return [0]*epochs, [0]*epochs, [0]*epochs
    
    optimizer = optim.Adam(trainable_params, lr=lr)
    
    train_losses, train_accs, test_accs = [], [], []
    
    for epoch in range(epochs):
        # 训练
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
        
        train_loss = running_loss / len(train_loader)
        train_acc = 100. * correct / total
        
        # 测试
        model.eval()
        test_correct = 0
        test_total = 0
        
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = outputs.max(1)
                test_total += labels.size(0)
                test_correct += predicted.eq(labels).sum().item()
        
        test_acc = 100. * test_correct / test_total
        
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        test_accs.append(test_acc)
        
        print(f'轮次 [{epoch+1:2d}/{epochs}] | '
              f'损失: {train_loss:.4f} | '
              f'训练准确率: {train_acc:.2f}% | '
              f'测试准确率: {test_acc:.2f}%')
    
    return train_losses, train_accs, test_accs

# 训练LeNet
lenet_train_loss, lenet_train_acc, lenet_test_acc = train_model(
    lenet, train_loader, test_loader, epochs=5, lr=0.001, model_name="LeNet"
)

print(f"✓ LeNet训练完成，最终测试准确率: {lenet_test_acc[-1]:.2f}%")

# 绘制训练曲线
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(lenet_train_loss)
plt.title('LeNet训练损失')
plt.xlabel('轮次')
plt.ylabel('损失')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(lenet_train_acc, label='训练')
plt.plot(lenet_test_acc, label='测试')
plt.title('LeNet准确率')
plt.xlabel('轮次')
plt.ylabel('准确率 (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ==================== 4. LeNet特征可视化 ====================
print("\n4. 可视化LeNet特征...")

# 可视化卷积核
def visualize_kernels(model):
    conv_layers = [model.conv1, model.conv2]
    layer_names = ['第一卷积层', '第二卷积层']
    
    for i, (layer, name) in enumerate(zip(conv_layers, layer_names)):
        kernels = layer.weight.data.cpu()
        num_kernels = kernels.size(0)
        
        print(f"{name}: {num_kernels}个卷积核")
        
        # 只可视化第一个通道的卷积核
        fig, axes = plt.subplots(2, 3, figsize=(10, 7))
        for k in range(min(num_kernels, 6)):  # 最多显示6个
            row, col = k // 3, k % 3
            kernel = kernels[k, 0].numpy()  # 只取第一个通道
            axes[row, col].imshow(kernel, cmap='gray')
            axes[row, col].set_title(f'卷积核 {k+1}')
            axes[row, col].axis('off')
        
        # 隐藏多余的子图
        for k in range(num_kernels, 6):
            row, col = k // 3, k % 3
            axes[row, col].axis('off')
        
        plt.suptitle(f'{name}卷积核可视化')
        plt.tight_layout()
        plt.show()

visualize_kernels(lenet)

# ==================== 5. VGG-16迁移学习（极简修复版） ====================
print("\n5. VGG-16迁移学习实验...")

try:
    print("准备VGG-16数据...")
    # 使用标准224x224尺寸
    vgg_transform = transforms.Compose([
        transforms.Resize(224),
        transforms.Grayscale(3),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                            std=[0.229, 0.224, 0.225])
    ])
    
    # 创建数据集
    vgg_train_dataset = torchvision.datasets.MNIST(
        root='./data', train=True, transform=vgg_transform, download=False
    )
    vgg_test_dataset = torchvision.datasets.MNIST(
        root='./data', train=False, transform=vgg_transform, download=False
    )
    
    # 使用少量数据加速训练
    from torch.utils.data import Subset
    indices = list(range(2000))
    vgg_train_dataset = Subset(vgg_train_dataset, indices)
    vgg_test_dataset = Subset(vgg_test_dataset, indices[:500])
    
    vgg_train_loader = torch.utils.data.DataLoader(
        vgg_train_dataset, batch_size=16, shuffle=True, num_workers=0
    )
    vgg_test_loader = torch.utils.data.DataLoader(
        vgg_test_dataset, batch_size=16, shuffle=False, num_workers=0
    )
    
    print(f"✓ VGG-16数据准备完成")
    
    # 最简单的VGG-16修复
    print("创建VGG-16模型...")
    
    # 直接使用预训练模型
    vgg_model = torchvision.models.vgg16(pretrained=True)
    
    # 冻结所有参数
    for param in vgg_model.parameters():
        param.requires_grad = False
    
    # 重新构建分类器（关键修复）
    # 对于224x224输入，特征图尺寸是512x7x7=25088
    vgg_model.classifier = nn.Sequential(
        nn.Linear(25088, 256),  # 第一层必须是25088
        nn.ReLU(),
        nn.Dropout(0.5),
        nn.Linear(256, 10)      # 输出10个类别
    )
    
    # 允许分类器的参数被训练
    for param in vgg_model.classifier.parameters():
        param.requires_grad = True
    
    vgg_model = vgg_model.to(device)
    print("  ✓ VGG-16模型创建完成")
    print(f"  ✓ 分类器结构: 25088 -> 256 -> 10")
    
    # 训练
    print("训练VGG-16迁移学习模型...")
    optimizer = optim.Adam(vgg_model.classifier.parameters(), lr=0.0001)
    criterion = nn.CrossEntropyLoss()
    
    vgg_train_losses, vgg_train_accs, vgg_test_accs = [], [], []
    
    for epoch in range(5):
        vgg_model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for images, labels in vgg_train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = vgg_model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        train_loss = total_loss / len(vgg_train_loader)
        train_acc = 100 * correct / total
        
        # 测试
        vgg_model.eval()
        test_correct = 0
        test_total = 0
        
        with torch.no_grad():
            for images, labels in vgg_test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = vgg_model(images)
                _, predicted = torch.max(outputs, 1)
                test_total += labels.size(0)
                test_correct += (predicted == labels).sum().item()
        
        test_acc = 100 * test_correct / test_total
        
        vgg_train_losses.append(train_loss)
        vgg_train_accs.append(train_acc)
        vgg_test_accs.append(test_acc)
        
        print(f'轮次 {epoch+1}/5 | 损失: {train_loss:.4f} | '
              f'训练准确率: {train_acc:.2f}% | 测试准确率: {test_acc:.2f}%')
    
    print(f"✓ VGG-16训练完成")
    
    # ==================== 新增：VGG-16特征可视化 ====================
    print("\n5.1 VGG-16特征可视化...")
    
    def visualize_vgg_features(model, data_loader, device, num_images=3):
        """
        可视化VGG-16中间层的特征图[3,4](@ref)
        
        参数:
            model: VGG模型
            data_loader: 数据加载器
            device: 设备
            num_images: 要可视化的图像数量
        """
        # 获取一批数据
        data_iter = iter(data_loader)
        images, labels = next(data_iter)
        images = images.to(device)
        
        # 选择要可视化的层（VGG的特征层）
        # VGG的features部分包含多个卷积块
        feature_layers = {
            'block1_conv2': model.features[3],  # 第一个卷积块的第二个卷积层后
            'block2_conv2': model.features[8],  # 第二个卷积块的第二个卷积层后
            'block3_conv3': model.features[15], # 第三个卷积块的第三个卷积层后
        }
        
        # 注册钩子来捕获特征图[6,7](@ref)
        features = {}
        def get_features(name):
            def hook(model, input, output):
                features[name] = output.detach()
            return hook
        
        hooks = []
        for layer_name, layer in feature_layers.items():
            hook = layer.register_forward_hook(get_features(layer_name))
            hooks.append(hook)
        
        # 前向传播获取特征
        model.eval()
        with torch.no_grad():
            _ = model(images[:num_images])
        
        # 移除钩子
        for hook in hooks:
            hook.remove()
        
        # 可视化特征图
        for img_idx in range(min(num_images, len(images))):
            fig, axes = plt.subplots(2, 4, figsize=(15, 8))
            fig.suptitle(f'VGG-16特征图可视化 - 图像 {img_idx+1} (标签: {labels[img_idx].item()})', fontsize=16)
            
            # 显示原始图像
            original_img = images[img_idx].cpu().squeeze().permute(1, 2, 0)
            # 反标准化显示
            mean = torch.tensor([0.485, 0.456, 0.406])
            std = torch.tensor([0.229, 0.224, 0.225])
            original_img = original_img * std + mean
            original_img = torch.clamp(original_img, 0, 1)
            
            axes[0, 0].imshow(original_img)
            axes[0, 0].set_title('原始图像')
            axes[0, 0].axis('off')
            
            # 显示各层的特征图
            for i, (layer_name, feature_map) in enumerate(features.items()):
                row, col = (i+1) // 2, (i+1) % 2
                if row >= 2:  # 确保不会超出范围
                    row, col = 1, i-1
                
                # 获取该图像的特征图
                feature = feature_map[img_idx].cpu()
                
                # 选择前8个通道进行显示
                num_channels = min(8, feature.shape[0])
                
                # 计算特征图的平均值作为该层的代表[4](@ref)
                channel_avg = torch.mean(feature, dim=0)
                
                axes[row, col].imshow(channel_avg, cmap='viridis')
                axes[row, col].set_title(f'{layer_name}\n({feature.shape[0]}个通道)')
                axes[row, col].axis('off')
            
            # 显示多个通道的特征图（第三个卷积块）
            if 'block3_conv3' in features:
                feature = features['block3_conv3'][img_idx].cpu()
                num_channels = min(4, feature.shape[0])
                
                for ch in range(num_channels):
                    row, col = ch // 2, 2 + ch % 2
                    if row < 2 and col < 4:  # 确保在子图范围内
                        axes[row, col].imshow(feature[ch], cmap='viridis')
                        axes[row, col].set_title(f'block3_conv3\n通道{ch+1}')
                        axes[row, col].axis('off')
            
            plt.tight_layout()
            plt.show()
            
            # 单独显示第一个卷积块的多通道特征
            if 'block1_conv2' in features:
                feature = features['block1_conv2'][img_idx].cpu()
                visualize_multiple_channels(feature, 'block1_conv2', max_channels=16)
            
            # 显示深层特征
            if 'block3_conv3' in features:
                feature = features['block3_conv3'][img_idx].cpu()
                visualize_multiple_channels(feature, 'block3_conv3', max_channels=16)
    
    def visualize_multiple_channels(feature, layer_name, max_channels=16):
        """
        可视化单个层的多个通道特征图[4,7](@ref)
        """
        num_channels = min(max_channels, feature.shape[0])
        rows = int(np.ceil(np.sqrt(num_channels)))
        cols = int(np.ceil(num_channels / rows))
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 12))
        fig.suptitle(f'VGG-16 {layer_name} - 多个通道特征图', fontsize=16)
        
        if rows == 1 and cols == 1:
            axes = np.array([[axes]])
        elif rows == 1:
            axes = axes.reshape(1, -1)
        elif cols == 1:
            axes = axes.reshape(-1, 1)
        
        for i in range(rows * cols):
            row, col = i // cols, i % cols
            if i < num_channels:
                axes[row, col].imshow(feature[i], cmap='viridis')
                axes[row, col].set_title(f'通道 {i+1}')
            axes[row, col].axis('off')
        
        plt.tight_layout()
        plt.show()
        
        # 显示特征图统计信息
        print(f"{layer_name}特征图统计:")
        print(f"  形状: {feature.shape}")
        print(f"  最小值: {feature.min().item():.4f}, 最大值: {feature.max().item():.4f}")
        print(f"  平均值: {feature.mean().item():.4f}, 标准差: {feature.std().item():.4f}")
        print()
    
    # 执行VGG特征可视化
    visualize_vgg_features(vgg_model, vgg_test_loader, device, num_images=2)
    
except Exception as e:
    print(f"✗ VGG-16训练出错: {e}")
    vgg_test_accs = [0.0]

# ==================== 6. ResNet-18迁移学习（10轮） ====================
print("\n6. ResNet-18迁移学习实验（10轮训练）...")

try:
    print("准备ResNet-18数据...")
    # 使用相同的数据
    resnet_train_loader = vgg_train_loader if 'vgg_train_loader' in locals() else None
    resnet_test_loader = vgg_test_loader if 'vgg_test_loader' in locals() else None
    
    if resnet_train_loader is None:
        # 如果VGG部分失败，重新创建数据加载器
        resnet_transform = transforms.Compose([
            transforms.Resize(224),
            transforms.Grayscale(3),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                std=[0.229, 0.224, 0.225])
        ])
        
        resnet_train_dataset = torchvision.datasets.MNIST(
            root='./data', train=True, transform=resnet_transform, download=False
        )
        resnet_test_dataset = torchvision.datasets.MNIST(
            root='./data', train=False, transform=resnet_transform, download=False
        )
        
        from torch.utils.data import Subset
        indices = list(range(2000))
        resnet_train_dataset = Subset(resnet_train_dataset, indices)
        resnet_test_dataset = Subset(resnet_test_dataset, indices[:500])
        
        resnet_train_loader = torch.utils.data.DataLoader(
            resnet_train_dataset, batch_size=16, shuffle=True, num_workers=0
        )
        resnet_test_loader = torch.utils.data.DataLoader(
            resnet_test_dataset, batch_size=16, shuffle=False, num_workers=0
        )
    
    class SimpleResNet18(nn.Module):
        def __init__(self, num_classes=10):
            super(SimpleResNet18, self).__init__()
            
            # 加载预训练模型
            try:
                resnet = torchvision.models.resnet18(pretrained=True)
            except:
                print("  ⚠ 预训练模型加载失败，创建新模型")
                resnet = torchvision.models.resnet18(pretrained=False)
            
            # 冻结卷积层
            for param in resnet.parameters():
                param.requires_grad = False
            
            print("  ✓ 冻结了ResNet-18的卷积层")
            
            # 修改全连接层
            num_features = resnet.fc.in_features
            resnet.fc = nn.Sequential(
                nn.Linear(num_features, 128),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(128, num_classes)
            )
            
            self.model = resnet
        
        def forward(self, x):
            return self.model(x)
    
    print("训练ResNet-18迁移学习模型（10轮）...")
    resnet_model = SimpleResNet18(num_classes=10).to(device)
    
    # 只训练全连接层
    optimizer = optim.Adam(resnet_model.model.fc.parameters(), lr=0.0001)
    criterion = nn.CrossEntropyLoss()
    
    resnet_train_acc, resnet_test_acc = [], []
    
    for epoch in range(10):
        # 训练
        resnet_model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for images, labels in resnet_train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = resnet_model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()
        
        train_acc = 100.0 * train_correct / train_total
        resnet_train_acc.append(train_acc)
        
        # 测试
        resnet_model.eval()
        test_correct = 0
        test_total = 0
        
        with torch.no_grad():
            for images, labels in resnet_test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = resnet_model(images)
                _, predicted = outputs.max(1)
                test_total += labels.size(0)
                test_correct += predicted.eq(labels).sum().item()
        
        test_acc = 100.0 * test_correct / test_total
        resnet_test_acc.append(test_acc)
        
        print(f'轮次 [{epoch+1:2d}/10] | '
              f'损失: {train_loss/len(resnet_train_loader):.4f} | '
              f'训练准确率: {train_acc:.2f}% | '
              f'测试准确率: {test_acc:.2f}%')
    
    print(f"✓ ResNet-18训练完成，最终测试准确率: {resnet_test_acc[-1]:.2f}%")
    
    # 绘制训练曲线
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(range(1, 11), resnet_train_acc, 'b-', label='训练', marker='o')
    plt.plot(range(1, 11), resnet_test_acc, 'r-', label='测试', marker='s')
    plt.title('ResNet-18准确率曲线（10轮）')
    plt.xlabel('训练轮次')
    plt.ylabel('准确率 (%)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    models_to_compare = ['LeNet']
    accuracies = [lenet_test_acc[-1]]
    
    if 'vgg_test_accs' in locals() and len(vgg_test_accs) > 0:
        models_to_compare.append('VGG-16')
        accuracies.append(vgg_test_accs[-1])
    
    models_to_compare.append('ResNet-18')
    accuracies.append(resnet_test_acc[-1])
    
    plt.bar(models_to_compare, accuracies, color=['blue', 'green', 'red'])
    plt.title('模型准确率对比')
    plt.ylabel('准确率 (%)')
    plt.grid(True, axis='y')
    
    plt.tight_layout()
    plt.show()
    
except Exception as e:
    print(f"✗ ResNet-18训练出错: {e}")
    print("⚠ 跳过ResNet-18实验...")
    resnet_test_acc = [0.0]

# ==================== 7. 实验结果对比 ====================
print("\n7. 实验结果对比分析")

# 确保所有测试准确率列表都有数据
if 'lenet_test_acc' not in locals():
    lenet_test_acc = [0.0]
if 'vgg_test_accs' not in locals():
    vgg_test_accs = [0.0]
if 'resnet_test_acc' not in locals():
    resnet_test_acc = [0.0]

# 模型对比图
plt.figure(figsize=(10, 6))

# 只绘制有数据的部分
if len(lenet_test_acc) > 1:
    epochs_lenet = range(1, len(lenet_test_acc) + 1)
    plt.plot(epochs_lenet, lenet_test_acc, 'o-', label='LeNet', linewidth=2, markersize=8)

if len(vgg_test_accs) > 1:
    epochs_vgg = range(1, len(vgg_test_accs) + 1)
    plt.plot(epochs_vgg, vgg_test_accs, 's-', label='VGG-16', linewidth=2, markersize=8)

if len(resnet_test_acc) > 1:
    epochs_resnet = range(1, len(resnet_test_acc) + 1)
    plt.plot(epochs_resnet, resnet_test_acc, '^-', label='ResNet-18', linewidth=2, markersize=8)

plt.title('模型对比 - 测试准确率')
plt.xlabel('训练轮次')
plt.ylabel('准确率 (%)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 最终准确率对比
print("\n" + "="*50)
print("最终测试准确率对比")
print("="*50)
print(f"LeNet:     {lenet_test_acc[-1]:.2f}%")
print(f"VGG-16:    {vgg_test_accs[-1]:.2f}%")
print(f"ResNet-18: {resnet_test_acc[-1]:.2f}%")
print("="*50)

# 模型参数对比
print(f"\n模型参数数量对比:")
print(f"LeNet:     {sum(p.numel() for p in lenet.parameters()):,} 参数")
if 'vgg_model' in locals():
    vgg_trainable = sum(p.numel() for p in vgg_model.parameters() if p.requires_grad)
    vgg_total = sum(p.numel() for p in vgg_model.parameters())
    print(f"VGG-16:    {vgg_total:,} 参数 (可训练: {vgg_trainable:,})")
if 'resnet_model' in locals():
    resnet_trainable = sum(p.numel() for p in resnet_model.parameters() if p.requires_grad)
    resnet_total = sum(p.numel() for p in resnet_model.parameters())
    print(f"ResNet-18: {resnet_total:,} 参数 (可训练: {resnet_trainable:,})")

print("\n实验完成！")