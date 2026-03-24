# 好厉害啊蛙趣

import wandb
import random

wandb.init(project = 'my-awesome-project',
           config = {
    "learning_rate": 0.02,
    "architecture": "CNN",
    "dataset": "CIFAR-100",
    "epochs": 10,
    })


wandb.watch_called = False  # 在运行时重新加载模型，无需重新启动运行时


for i in range(100):
    s = (random.random() + random.random()) / 2
    wandb.log({"s": s})

wandb.finish()



