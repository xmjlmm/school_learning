import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# 设置随机种子保证可重复性
torch.manual_seed(42)
np.random.seed(42)

class MNISTDataLoader:
    """MNIST数据加载和预处理类"""
    
    def __init__(self, batch_size=64, use_data_augmentation=False):
        self.batch_size = batch_size
        self.use_data_augmentation = use_data_augmentation
        
    def get_transforms(self):
        """定义数据预处理流程"""
        if self.use_data_augmentation:
            # 训练时使用数据增强
            train_transform = transforms.Compose([
                transforms.RandomRotation(10),  # 随机旋转±10度
                transforms.RandomAffine(0, translate=(0.1, 0.1)),  # 随机平移
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))  # MNIST标准化参数
            ])
        else:
            train_transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ])
        
        test_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        return train_transform, test_transform
    
    def get_dataloaders(self):
        """获取数据加载器"""
        train_transform, test_transform = self.get_transforms()
        
        # 下载并加载MNIST数据集
        train_dataset = torchvision.datasets.MNIST(
            root='./data', train=True, download=True, transform=train_transform)
        test_dataset = torchvision.datasets.MNIST(
            root='./data', train=False, download=True, transform=test_transform)
        
        # 创建数据加载器
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, 
                                 shuffle=True, num_workers=2)
        test_loader = DataLoader(test_dataset, batch_size=self.batch_size, 
                                shuffle=False, num_workers=2)
        
        return train_loader, test_loader

class LeNet(nn.Module):
    """LeNet-5网络架构"""
    
    def __init__(self, num_classes=10):
        super(LeNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 6, kernel_size=5, padding=2),  # 28x28x1 -> 28x28x6
            nn.ReLU(inplace=True),
            nn.AvgPool2d(kernel_size=2, stride=2),      # 28x28x6 -> 14x14x6
            nn.Conv2d(6, 16, kernel_size=5),            # 14x14x6 -> 10x10x16
            nn.ReLU(inplace=True),
            nn.AvgPool2d(kernel_size=2, stride=2),      # 10x10x16 -> 5x5x16
        )
        self.classifier = nn.Sequential(
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU(inplace=True),
            nn.Linear(120, 84),
            nn.ReLU(inplace=True),
            nn.Linear(84, num_classes)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

class VGGNet(nn.Module):
    """简化版VGGNet，适配MNIST尺寸"""
    
    def __init__(self, num_classes=10):
        super(VGGNet, self).__init__()
        self.features = nn.Sequential(
            # 第一组卷积层
            nn.Conv2d(1, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 28x28 -> 14x14
            
            # 第二组卷积层
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 14x14 -> 7x7
        )
        self.classifier = nn.Sequential(
            nn.Linear(128 * 7 * 7, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

class ResidualBlock(nn.Module):
    """ResNet残差块"""
    
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                              stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                              stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1,
                         stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out

class ResNet(nn.Module):
    """简化版ResNet，适配MNIST"""
    
    def __init__(self, num_classes=10):
        super(ResNet, self).__init__()
        self.in_channels = 64
        
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        
        self.layer1 = self._make_layer(64, 2, stride=1)
        self.layer2 = self._make_layer(128, 2, stride=2)
        self.layer3 = self._make_layer(256, 2, stride=2)
        
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(256, num_classes)
    
    def _make_layer(self, out_channels, blocks, stride):
        strides = [stride] + [1] * (blocks - 1)
        layers = []
        for stride in strides:
            layers.append(ResidualBlock(self.in_channels, out_channels, stride))
            self.in_channels = out_channels
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.avg_pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

class ModelTrainer:
    """模型训练和评估类"""
    
    def __init__(self, model, device):
        self.model = model.to(device)
        self.device = device
        self.train_losses = []
        self.train_accuracies = []
        self.test_losses = []
        self.test_accuracies = []
        
    def train(self, train_loader, criterion, optimizer, epoch):
        """训练一个epoch"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(train_loader, desc=f'Epoch {epoch+1} Training')
        for batch_idx, (data, target) in enumerate(pbar):
            data, target = data.to(self.device), target.to(self.device)
            
            optimizer.zero_grad()
            output = self.model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            pbar.set_postfix({
                'Loss': f'{loss.item():.4f}',
                'Acc': f'{100.*correct/total:.2f}%'
            })
        
        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100. * correct / total
        
        self.train_losses.append(epoch_loss)
        self.train_accuracies.append(epoch_acc)
        
        return epoch_loss, epoch_acc
    
    def test(self, test_loader, criterion):
        """测试模型"""
        self.model.eval()
        test_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                loss = criterion(output, target)
                
                test_loss += loss.item()
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
        
        test_loss /= len(test_loader)
        test_acc = 100. * correct / total
        
        self.test_losses.append(test_loss)
        self.test_accuracies.append(test_acc)
        
        print(f'Test set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{total} ({test_acc:.2f}%)')
        
        return test_loss, test_acc

class FeatureVisualizer:
    """特征可视化类"""
    
    def __init__(self, model, device):
        self.model = model.to(device)
        self.device = device
        self.features = {}
        self.hooks = []
        
    def hook_fn(self, module, input, output, name):
        """钩子函数用于提取特征"""
        self.features[name] = output.detach().cpu()
        
    def register_hooks(self, layer_names):
        """注册钩子到指定层"""
        for name, module in self.model.named_modules():
            if name in layer_names:
                hook = module.register_forward_hook(
                    lambda m, i, o, n=name: self.hook_fn(m, i, o, n))
                self.hooks.append(hook)
    
    def remove_hooks(self):
        """移除所有钩子"""
        for hook in self.hooks:
            hook.remove()
    
    def visualize_features(self, test_loader, num_images=5):
        """可视化特征图"""
        self.model.eval()
        data_iter = iter(test_loader)
        images, labels = next(data_iter)
        
        # 选择前num_images个图像
        images = images[:num_images].to(self.device)
        
        # 前向传播获取特征
        with torch.no_grad():
            _ = self.model(images)
        
        # 绘制特征图
        fig = plt.figure(figsize=(15, 10))
        
        for img_idx in range(num_images):
            # 显示原始图像
            ax = plt.subplot(num_images, len(self.features) + 1, 
                           img_idx * (len(self.features) + 1) + 1)
            plt.imshow(images[img_idx].cpu().squeeze(), cmap='gray')
            plt.title(f'Label: {labels[img_idx]}')
            plt.axis('off')
            
            # 显示各层特征
            for layer_idx, (layer_name, feature_maps) in enumerate(self.features.items()):
                ax = plt.subplot(num_images, len(self.features) + 1, 
                               img_idx * (len(self.features) + 1) + layer_idx + 2)
                
                # 显示该层第一个特征图
                if len(feature_maps[img_idx]) > 0:
                    plt.imshow(feature_maps[img_idx][0].cpu().squeeze(), cmap='viridis')
                plt.title(f'{layer_name}')
                plt.axis('off')
        
        plt.tight_layout()
        plt.show()

def plot_training_curves(trainer, model_name):
    """绘制训练曲线"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # 损失曲线
    ax1.plot(trainer.train_losses, label='Training Loss')
    ax1.plot(trainer.test_losses, label='Test Loss')
    ax1.set_title(f'{model_name} - Loss Curves')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)
    
    # 准确率曲线
    ax2.plot(trainer.train_accuracies, label='Training Accuracy')
    ax2.plot(trainer.test_accuracies, label='Test Accuracy')
    ax2.set_title(f'{model_name} - Accuracy Curves')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

def experiment_mnist_lenet():
    """实验1: MNIST手写数字识别 with LeNet"""
    print("=" * 60)
    print("实验1: MNIST手写数字识别 - LeNet")
    print("=" * 60)
    
    # 设备配置
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")
    
    # 数据加载
    data_loader = MNISTDataLoader(batch_size=64, use_data_augmentation=True)
    train_loader, test_loader = data_loader.get_dataloaders()
    
    # 模型初始化
    model = LeNet()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
    
    # 训练模型
    trainer = ModelTrainer(model, device)
    epochs = 100
    
    for epoch in range(epochs):
        train_loss, train_acc = trainer.train(train_loader, criterion, optimizer, epoch)
        test_loss, test_acc = trainer.test(test_loader, criterion)
        scheduler.step()
    
    # 绘制训练曲线
    plot_training_curves(trainer, "LeNet on MNIST")
    
    return model, trainer, test_loader

def experiment_feature_visualization(model, test_loader):
    """实验2: LeNet特征可视化"""
    print("\n" + "=" * 60)
    print("实验2: LeNet特征可视化")
    print("=" * 60)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 特征可视化
    visualizer = FeatureVisualizer(model, device)
    
    # 选择要可视化的层
    layer_names = ['features.0', 'features.3']  # 第一个和第二个卷积层
    visualizer.register_hooks(layer_names)
    
    # 可视化特征
    visualizer.visualize_features(test_loader, num_images=3)
    visualizer.remove_hooks()
    
    print("特征可视化完成！")

def experiment_vgg_resnet():
    """实验3: VGGNet和ResNet对比实验"""
    print("\n" + "=" * 60)
    print("实验3: VGGNet和ResNet对比")
    print("=" * 60)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 数据加载
    data_loader = MNISTDataLoader(batch_size=64, use_data_augmentation=False)
    train_loader, test_loader = data_loader.get_dataloaders()
    
    models = {
        'VGGNet': VGGNet(),
        'ResNet': ResNet()
    }
    
    results = {}
    
    for model_name, model in models.items():
        print(f"\n训练{model_name}...")
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
        
        trainer = ModelTrainer(model, device)
        epochs = 100
        
        for epoch in range(epochs):
            train_loss, train_acc = trainer.train(train_loader, criterion, optimizer, epoch)
            test_loss, test_acc = trainer.test(test_loader, criterion)
            scheduler.step()
        
        plot_training_curves(trainer, f"{model_name} on MNIST")
        results[model_name] = trainer.test_accuracies[-1]
    
    # 比较结果
    print("\n模型性能对比:")
    for model_name, accuracy in results.items():
        print(f"{model_name}: {accuracy:.2f}%")
    
    return results


def main():
    """主函数"""
    print("图像分类实验开始...")
    
    try:
        # 实验1: MNIST + LeNet
        model, trainer, test_loader = experiment_mnist_lenet()
        
        # 实验2: 特征可视化
        experiment_feature_visualization(model, test_loader)
        
        # 实验3: VGGNet和ResNet对比
        results = experiment_vgg_resnet()
        
        
    except Exception as e:
        print(f"实验过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":

    main()