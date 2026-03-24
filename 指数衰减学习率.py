import tensorflow as tf
# 超参数设定
epoch = 40
LR_BASE = 0.2
LR_DECAY = 0.99
LR_STEP = 1
w = w1 = tf.Variable(tf.random.truncated_normal([], stddev = 0.1, seed = 1))


for epoch in range(epoch):
    lr = LR_BASE * LR_DECAY ** (epoch / LR_STEP)
    with tf.GradientTape() as tape:
        loss = tf.square(w + 1)
    grads = tape.gradient(loss, w)

    w.assign_sub(lr * grads)
    print('After {} epoch, w is {}, loss is {}, lr is {}'.format(epoch, w.numpy(), loss, lr))

