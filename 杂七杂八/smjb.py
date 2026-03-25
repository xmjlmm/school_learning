导入pytorch使用的模型等
[1]:
import torch
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
创建dataset实例，'dataset'代表图片存放路径。将dataset文件夹的图片转换成pytorch需要的类型（图片和标签），包括对图片颜色的数据增加、重新大小和图像归一化等
[2]:
dataset = datasets.ImageFolder(
    'Bus',
    transforms.Compose([
        transforms.ColorJitter(0.1, 0.1, 0.1, 0.1),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
)
划分训练集和验证集，全部图片为训练集，最后的50个图片为测试集
[3]:
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [len(dataset) - 50, 50])
设置训练的数据加载和验证的数据加载，batch_size和num_workers来定，不能定太大了，可能导致内存不做。shuffle表示是否打乱
[4]:
train_loader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True,
    num_workers=4
)

test_loader = torch.utils.data.DataLoader(
    test_dataset,
    batch_size=16,
    shuffle=True,
    num_workers=4
)
定义神经网络 使用迁移学习的方法来训练模型， 可以减少需要数据的量，只是根据提供的数据来修正参数。 使用ALEX的卷积神经网络，可以预加载网络的训练参数
[5]:


model = models.alexnet(pretrained=True)
alex卷积模型的输出为分类器的第6层，只修改最后输出层的参数，进行迁移学习
[6]:
model.classifier[6] = torch.nn.Linear(model.classifier[6].in_features, 2)
最后将模型在GPU上执行，进行转换
[7]:
device = torch.device('cuda')
model = model.to(device)
训练网络模型，写的方式基本上一样
[*]:
NUM_EPOCHS = 30
BEST_MODEL_PATH = 'Bus.pth'
best_accuracy = 0.0

optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)#学习率为0.001，SGD初始动量为0.9

for epoch in range(NUM_EPOCHS):
    
    for images, labels in iter(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        optimizer.zero_grad() #将梯度初始化为零
        outputs = model(images)
        loss = F.cross_entropy(outputs, labels)#交叉熵计算loss
        loss.backward() #运行反向传播累计梯度
        optimizer.step()#优化器调整参数
    
    test_error_count = 0.0
    for images, labels in iter(test_loader):
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        test_error_count += float(torch.sum(torch.abs(labels - outputs.argmax(1))))
    
    test_accuracy = 1.0 - float(test_error_count) / float(len(test_dataset))
    print('%d: %f' % (epoch, test_accuracy))
    if test_accuracy > best_accuracy:
        torch.save(model.state_dict(), BEST_MODEL_PATH)
        best_accuracy = test_accuracy
0: 1.000000
[ ]:


