import wandb
import random

# start a new wandb run to track this script
'''
wandb.init() —— 初始化一个新的 wandb 实验，并开始记录实验的信息和结果。
函数功能：用于初始化一个新的 wandb 实验，并开始记录实验的信息和结果。
函数说明：wandb.init(project=None, entity=None, group=None, job_type=None, config=None,
                   tags=None, resume=False, dir=None, name=None, notes=None, id=None,
                   magic=None, anonymous=None, allow_val_change=False, reinit=False, settings=None,)
参数说明：
        project：实验所属的项目名称。
        entity：实验所属的实体（例如，团队或用户）。
        group：实验的分组名称。
        job_type：实验的类型（例如，训练、评估等）。
        config：实验的配置参数，可以是一个字典或 Namespace 对象。
        tags：实验的标签，可以是一个字符串列表。
        resume：如果为 True，则尝试恢复先前的实验。默认为 False。
        dir：存储实验数据和日志的目录路径。
        name：实验的名称。
        notes：实验的说明或注释。
        id：实验的唯一标识符。
        magic：用于指定特殊功能的魔法命令。
        anonymous：如果为 True，则匿名上传实验结果。默认为 False。
        allow_val_change：如果为 True，则允许修改已存在的配置参数。默认为 False。
        reinit：如果为 True，则重新初始化实验，忽略先前的配置。默认为 False。
        settings：一个字典，用于设置实验的其他参数。
返回参数：
        一个 wandb.Run 对象，代表当前的实验运行。


'''

wandb.init(
    # set the wandb project where this run will be logged
    project="my-awesome-project",

    # track hyperparameters and run metadata
    config={
    "learning_rate": 0.02,
    "architecture": "CNN",
    "dataset": "CIFAR-100",
    "epochs": 10,
    }
)

# simulate training
epochs = 10
offset = random.random() / 5
for epoch in range(2, epochs):
    acc = 1 - 2 ** -epoch - random.random() / epoch - offset
    loss = 2 ** -epoch + random.random() / epoch + offset

    # log metrics to wandb
    wandb.log({"acc": acc, "loss": loss})

# [optional] finish the wandb run, necessary in notebooks
wandb.finish()
