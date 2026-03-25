import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split

import spacy
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import os
import re
from bs4 import BeautifulSoup

import hiddenlayer as hl
import matplotlib.pyplot as plt

import wandb
import optuna

wandb.init(project="IMDB_RNN_LSTM_GRU")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 配置参数（全局统一）
class Config:
    max_seq_len = 500  # 序列截断长度
    batch_size = 64  # 批处理大小
    embed_dim = 300  # 词向量维度
    hidden_size = 128  # 隐藏层维度
    num_layers = 2  # RNN堆叠层数
    epochs = 5  # 训练轮次
    lr = 0.001
    # glove_path = "./glove_data/glove.6B.300d.txt"   # GloVe文件路径
    glove_path = "F:\\学习\\大三下\\深度学习\\实验三\\glove_data\\glove.6B.300d.txt"


# 数据预处理模块
class IMDBProcessor:
    def __init__(self, config):
        self.nlp = spacy.load("en_core_web_sm")  # 加载英文分词模型
        self.word2idx = {"<pad>": 0, "<unk>": 1}  # 初始化特殊符号词典
        self.embed_matrix = [np.zeros(config.embed_dim), np.random.normal(
            size=config.embed_dim)]  # <pad>的零向量 <unk>的随机初始化向量
        self.config = config  # 存储配置参数对象
        self._load_glove()  # 加载GloVe预训练词向量

    def _load_glove(self):
        """加载GloVe词向量"""
        with open(self.config.glove_path, 'r', encoding='utf-8') as f:
            for line in f:
                word, vector = line.split(maxsplit=1)  # 分离首个标识与后续数据
                vector = np.fromstring(vector, sep=' ')  # 字符串转numpy数组
                if word not in self.word2idx:
                    self.word2idx[word] = len(self.embed_matrix)
                    self.embed_matrix.append(vector)
        self.embed_matrix = torch.FloatTensor(np.vstack(self.embed_matrix))

    def text_to_indices(self, text):
        """文本转索引序列"""
        tokens = [token.text.lower() for token in self.nlp.tokenizer(text)]
        indices = [self.word2idx.get(token, 1)
                   for token in tokens[:self.config.max_seq_len]]
        return indices + [0] * (self.config.max_seq_len - len(indices))


# 数据集类
class IMDBDataset(Dataset):
    def __init__(self, data_dir, processor, split='train'):
        self.data = []
        self.processor = processor

        # 遍历pos/neg目录
        for sentiment in ['pos', 'neg']:
            label = 1 if sentiment == 'pos' else 0
            dir_path = os.path.join(data_dir, split, sentiment)
            for filename in os.listdir(dir_path):
                with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as f:
                    text = f.read()
                    text = self._clean_html(text)  # HTML清洗
                    self.data.append((text, label))

    def _clean_html(self, text):
        """去除HTML标签与特殊字符"""
        text = re.sub(r'<br  />', ' ', text)  # 替换换行标签
        return BeautifulSoup(text, "html.parser").get_text().strip()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text, label = self.data[idx]
        return (
            torch.LongTensor(self.processor.text_to_indices(text)),
            torch.FloatTensor([float(label)])
        )


# 独立模型定义
class RNNModel(nn.Module):
    def __init__(self, vocab_size, embed_matrix):
        super().__init__()
        self.embed = nn.Embedding.from_pretrained(
            embed_matrix, padding_idx=0)
        # 添加bidirectional=True参数，并将hidden_size乘以2
        self.rnn = nn.RNN(Config.embed_dim, Config.hidden_size,
                          Config.num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(Config.hidden_size * 2, 1)  # 输入维度翻倍
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.embed(x)
        _, h_n = self.rnn(x)
        # 拼接双向的隐藏状态
        combined_hidden = torch.cat((h_n[-2, :, :], h_n[-1, :, :]), dim=1)
        return self.sigmoid(self.fc(combined_hidden))


class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embed_matrix):
        super().__init__()
        self.embed = nn.Embedding.from_pretrained(
            embed_matrix, padding_idx=0)
        # 添加bidirectional=True参数，并将hidden_size乘以2
        self.lstm = nn.LSTM(Config.embed_dim, Config.hidden_size,
                            Config.num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(Config.hidden_size * 2, 1)  # 输入维度翻倍
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.embed(x)
        _, (h_n, _) = self.lstm(x)
        # 拼接双向的隐藏状态
        combined_hidden = torch.cat((h_n[-2, :, :], h_n[-1, :, :]), dim=1)
        return self.sigmoid(self.fc(combined_hidden))


class GRUModel(nn.Module):
    def __init__(self, vocab_size, embed_matrix):
        super().__init__()
        self.embed = nn.Embedding.from_pretrained(
            embed_matrix, padding_idx=0)
        # 添加bidirectional=True参数，并将hidden_size乘以2
        self.gru = nn.GRU(Config.embed_dim, Config.hidden_size,
                          Config.num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(Config.hidden_size * 2, 1)  # 输入维度翻倍
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.embed(x)
        _, h_n = self.gru(x)
        # 拼接双向的隐藏状态
        combined_hidden = torch.cat((h_n[-2, :, :], h_n[-1, :, :]), dim=1)
        return self.sigmoid(self.fc(combined_hidden))

# 统一训练函数
def train_and_evaluate(model, train_loader, val_loader, test_loader, config, model_name):
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.lr)

    # 初始化记录容器
    history = hl.History()  # 可视化记录器
    canvas = hl.Canvas()  # 画布对象
    train_losses, val_losses, test_loss = [], [], []
    train_accs, val_accs, test_acc = [], [], []

    # 训练循环
    for epoch in range(config.epochs):
        # ---------- 训练阶段 ----------
        model.train()
        epoch_train_loss, train_preds, train_labels = 0.0, [], []
        for inputs, labels in train_loader:
            # 将数据转移到设备上
            inputs = inputs.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            epoch_train_loss += loss.item()
            train_preds.extend((outputs > 0.5).float().tolist())
            train_labels.extend(labels.tolist())

        # 计算训练指标
        avg_train_loss = epoch_train_loss / len(train_loader)
        train_accuracy = accuracy_score(train_labels, train_preds)
        train_losses.append(avg_train_loss)
        train_accs.append(train_accuracy)

        # ---------- 验证阶段 ----------
        model.eval()
        val_loss, val_preds, val_labels = 0.0, [], []
        with torch.no_grad():
            for inputs, labels in val_loader:
                # 将数据转移到设备上
                inputs = inputs.to(device)
                labels = labels.to(device)
                outputs = model(inputs)
                val_loss += criterion(outputs, labels).item()
                val_preds.extend((outputs > 0.5).float().tolist())
                val_labels.extend(labels.tolist())

        # 计算验证指标
        avg_val_loss = val_loss / len(val_loader)
        val_accuracy = accuracy_score(val_labels, val_preds)
        val_losses.append(avg_val_loss)
        val_accs.append(val_accuracy)

        # 记录指标到HiddenLayer
        history.log(epoch,
                    train_loss=avg_train_loss,
                    val_loss=avg_val_loss,
                    train_acc=train_accuracy,
                    val_acc=val_accuracy)

        # 将每个模型每个epoch的训练和验证指标记录到wandb
        wandb.log({
            f"{model_name}/train_loss": avg_train_loss,
            f"{model_name}/val_loss": avg_val_loss,
            f"{model_name}/train_acc": train_accuracy,
            f"{model_name}/val_acc": val_accuracy
        })

        # 绘制可视化曲线
        with canvas:
            canvas.draw_plot([history["train_loss"], history["val_loss"]],
                             labels=["Train Loss", "Val Loss"])
            canvas.draw_plot([history["train_acc"], history["val_acc"]],
                             labels=["Train Acc", "Val Acc"])

        # 实时打印指标
        print(f"Epoch {epoch + 1}/{config.epochs}")
        print(f"  Train Loss: {avg_train_loss:.4f} | Acc: {train_accuracy:.3f}")
        print(f"  Val Loss: {avg_val_loss:.4f} | Acc: {val_accuracy:.3f}\n")

    # ---------- 测试阶段 ----------
    model.eval()
    test_loss, test_preds, test_labels = 0.0, [], []  # 初始化test_loss为累加器
    with torch.no_grad():
        for inputs, labels in test_loader:
            # 将数据转移到设备上
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            test_loss += criterion(outputs, labels).item()  # 累加每个batch的loss
            test_preds.extend((outputs > 0.5).float().tolist())
            test_labels.extend(labels.tolist())

    # 计算测试指标
    avg_test_loss = test_loss / len(test_loader)

    return {
        "train_loss": train_losses,
        "val_loss": val_losses,
        "test_loss": avg_test_loss,
        "train_acc": train_accs,
        "val_acc": val_accs,
        "test_metrics": {
            "accuracy": accuracy_score(test_labels, test_preds),
            "precision": precision_score(test_labels, test_preds),
            "recall": recall_score(test_labels, test_preds),
            "f1": f1_score(test_labels, test_preds)
        }
    }


# %% 全局参数定义
config = Config()

# %% 数据处理
processor = IMDBProcessor(config)

acl_path = "F:\\学习\\大三下\\深度学习\\实验三\\aclImdb\\aclImdb"

# %% 数据集接口
train_dataset = IMDBDataset(acl_path, processor, split='train')
test_dataset = IMDBDataset(acl_path, processor, split='test')

# %% 划分验证集
train_size = int(0.9 * len(train_dataset))
train_set, val_set = random_split(train_dataset, [train_size, len(train_dataset) - train_size])

# %% 数据集加载器
train_loader = DataLoader(train_set, batch_size=config.batch_size, shuffle=True)
val_loader = DataLoader(val_set, batch_size=config.batch_size)
test_loader = DataLoader(test_dataset, batch_size=config.batch_size)

# %% 初始化模型
models = {
    "RNN": RNNModel(len(processor.embed_matrix), processor.embed_matrix),
    "LSTM": LSTMModel(len(processor.embed_matrix), processor.embed_matrix),
    "GRU": GRUModel(len(processor.embed_matrix), processor.embed_matrix)
}


# %% 训练与评估
# %% 训练与评估
results = {}
for name, model in models.items():
    model = model.to(device)
    print(f"\n=== Training {name} Model ===")
    results[name] = train_and_evaluate(model, train_loader, val_loader, test_loader, config, name)

    # 提取测试指标
    test_metrics = results[name]["test_metrics"]

    # 输出测试结果
    print(f"\n{name} Test Results:")
    print(f"Accuracy: {test_metrics['accuracy']:.3f}")
    print(f"Precision: {test_metrics['precision']:.3f}")
    print(f"Recall: {test_metrics['recall']:.3f}")
    print(f"F1-Score: {test_metrics['f1']:.3f}")
    print(f"Test Loss: {results[name]['test_loss']:.4f}")

# %% 绘制多模型训练曲线对比
plt.figure(figsize=(12, 5))
for model_name in models.keys():
    plt.plot(results[model_name]["train_loss"],
             label=f"{model_name} Train Loss")
    plt.plot(results[model_name]["val_loss"],
             linestyle="--", label=f"{model_name} Val Loss")
plt.legend()
plt.title("Cross-Model  Loss Comparison")

wandb.finish()
    