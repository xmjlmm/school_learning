from __future__ import print_function
import random
import numpy as np
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as T
import torch.nn.functional as F
import wandb
import os

device = "cuda:0" if torch.cuda.is_available() else "cpu"

# create train and test dataloaders
def get_dataloader(is_train, batch_size, slice=5):
    "Get a training dataloader"
    ds = torchvision.datasets.MNIST(root=".", train=is_train, transform=T.ToTensor(), download=True)
    loader = torch.utils.data.DataLoader(dataset=ds,
                                         batch_size=batch_size,
                                         shuffle=True if is_train else False,
                                         pin_memory=True, num_workers=2)
    return loader

# Number of epochs to run
# Each epoch includes a training step and a test step, so this sets
# the number of tables of test predictions to log
EPOCHS = 1

# Number of batches to log from the test data for each test step
# (default set low to simplify demo)
NUM_BATCHES_TO_LOG = 10 #79

# Number of images to log per test batch
# (default set low to simplify demo)
NUM_IMAGES_PER_BATCH = 32 #128

# training configuration and hyperparameters
NUM_CLASSES = 10
BATCH_SIZE = 32
LEARNING_RATE = 0.001
L1_SIZE = 32
L2_SIZE = 64
# changing this may require changing the shape of adjacent layers
CONV_KERNEL_SIZE = 5

# define a two-layer convolutional neural network
class ConvNet(nn.Module):
    def __init__(self, num_classes=10):
        super(ConvNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, L1_SIZE, CONV_KERNEL_SIZE, stride=1, padding=2),
            nn.BatchNorm2d(L1_SIZE),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(L1_SIZE, L2_SIZE, CONV_KERNEL_SIZE, stride=1, padding=2),
            nn.BatchNorm2d(L2_SIZE),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc = nn.Linear(7*7*L2_SIZE, NUM_CLASSES)
        self.softmax = nn.Softmax(NUM_CLASSES)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        return out

def main():
    train_loader = get_dataloader(is_train=True, batch_size=BATCH_SIZE)
    test_loader = get_dataloader(is_train=False, batch_size=2*BATCH_SIZE)

    # ✨ W&B: Initialize a new run to track this model's training
    wandb.init(project="table-quickstart")

    # ✨ W&B: Log hyperparameters using config
    cfg = wandb.config
    cfg.update({"epochs": EPOCHS, "batch_size": BATCH_SIZE, "lr": LEARNING_RATE,
                "l1_size": L1_SIZE, "l2_size": L2_SIZE,
                "conv_kernel": CONV_KERNEL_SIZE,
                "img_count": min(10000, NUM_IMAGES_PER_BATCH * NUM_BATCHES_TO_LOG)})

    # define model, loss, and optimizer
    model = ConvNet(NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # convenience funtion to log predictions for a batch of test images
    def log_test_predictions(images, labels, outputs, predicted, test_table, log_counter):
        scores = F.softmax(outputs.data, dim=1)
        log_scores = scores.cpu().numpy()
        log_images = images.cpu().numpy()
        log_labels = labels.cpu().numpy()
        log_preds = predicted.cpu().numpy()
        _id = 0
        for i, l, p, s in zip(log_images, log_labels, log_preds, log_scores):
            img_id = str(_id) + "_" + str(log_counter)
            test_table.add_data(img_id, wandb.Image(i), p, l, *s)
            _id += 1
            if _id == NUM_IMAGES_PER_BATCH:
                break

    total_step = len(train_loader)
    for epoch in range(EPOCHS):
        for i, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            wandb.log({"loss": loss})
            if (i + 1) % 100 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch + 1, EPOCHS, i + 1, total_step, loss.item()))

        columns = ["id", "image", "guess", "truth"]
        for digit in range(10):
            columns.append("score_" + str(digit))
        test_table = wandb.Table(columns=columns)

        model.eval()
        log_counter = 0
        with torch.no_grad():
            correct = 0
            total = 0
            for images, labels in test_loader:
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                if log_counter < NUM_BATCHES_TO_LOG:
                    log_test_predictions(images, labels, outputs, predicted, test_table, log_counter)
                    log_counter += 1
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            acc = 100 * correct / total
            wandb.log({"epoch": epoch, "acc": acc})
            print('Test Accuracy of the model on the 10000 test images: {} %'.format(acc))

        wandb.log({"test_predictions": test_table})

    wandb.finish()

if __name__ == '__main__':
    main()
