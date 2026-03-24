import wandb

# 初始化wandb
wandb.init(
    # set the wandb project where this run will be logged
    project="my-awesome-project",

    # track hyperparameters and run metadata
    config={
        "learning_rate": lr,
        ...
    }
)

# 整体嵌入架构
epochs = 100
for i in range(epochs):
    net.train():
    train_total_loss = 0
    for ... in train_loader:
        ...
        ...
        train_total_loss += loss.item()
        train_total_acc += acc(....)
    train_acc = train_total_acc / len(train_loader)

    net.eval()
    val_total_loss = 0
    for ... in val_loader:
        ...
        ...
        val_total_loss += loss.item()
        val_total_acc += acc(...)
    val_acc = val_total_acc / len(val_loader)
    wandb.log({"train_loss": train_total_loss, "val_loss": val_total_loss, "train_acc": train_acc, "val_acc": val_acc})
wandb.finish()
