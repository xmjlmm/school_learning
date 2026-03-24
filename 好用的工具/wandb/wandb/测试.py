from __future__ import print_function
import argparse
import random
import numpy
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import logging
import os

logging.propagate = False
logging.getLogger().setLevel(logging.ERROR)

# WandB – Import the wandb library
import wandb

# 定义Convolutional Neural Network：
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, kernel_size=5)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2(x), 2))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.log_softmax(x, dim=1)

def train(config, model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_id, (data, target) in enumerate(train_loader):
        if batch_id > 20:
            break
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()

def test(args, model, device, test_loader, classes):
    model.eval()
    test_loss = 0
    correct = 0
    example_images = []

    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()
            example_images.append(wandb.Image(
                data[0], caption="Pred:{} Truth:{}".format(classes[pred[0].item()], classes[target[0]])))

    wandb.log({
        "Examples": example_images,
        "Test Accuracy": 100. * correct / len(test_loader.dataset),
        "Test Loss": test_loss
    })

# 设置 WANDB_DIR 环境变量
os.environ['WANDB_DIR'] = os.path.abspath(os.getcwd())

wandb.init(project="pytorch-intro")
wandb.watch_called = False

config = wandb.config
config.batch_size = 4
config.test_batch_size = 10
config.epochs = 50
config.lr = 0.1
config.momentum = 0.1
config.no_cuda = False
config.seed = 42
config.log_interval = 10

def main():
    use_cuda = not config.no_cuda and torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

    torch.manual_seed(config.seed)
    torch.backends.cudnn.deterministic = True

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    train_loader = DataLoader(datasets.CIFAR10(
        root=os.path.join(os.getcwd(), 'data'),
        train=True,
        download=True,
        transform=transform
    ), batch_size=config.batch_size, shuffle=True, **kwargs)

    test_loader = DataLoader(datasets.CIFAR10(
        root=os.path.join(os.getcwd(), 'data'),
        train=False,
        download=True,
        transform=transform
    ), batch_size=config.batch_size, shuffle=False, **kwargs)

    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    model = Net().to(device)
    optimizer = optim.SGD(model.parameters(), lr=config.lr, momentum=config.momentum)

    wandb.watch(model, log="all")
    for epoch in range(1, config.epochs + 1):
        train(config, model, device, train_loader, optimizer, epoch)
        test(config, model, device, test_loader, classes)

    torch.save(model.state_dict(), 'model.h5')
    wandb.save('model.h5')

if __name__ == '__main__':
    main()
