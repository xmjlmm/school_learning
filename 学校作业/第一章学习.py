# %%
import torch
import torch.nn  as nn 
import torch.utils.data as Data

# %%
print(torch.__version__)

# %%
x = torch.tensor([[1,  2], [3, 4]], dtype=torch.float32,  device="cpu")
print(x.shape)   # 输出: torch.Size([2, 2])
print(x.dtype)    # 输出: torch.float32 
print(x.device)   # 输出: cpu

x = x.to('cuda')
print(x.device)


# %%
# 从列表/元组创建
a = torch.tensor([[1,  2], [3, 4]])  
print("a: ",a)
print("a.shape: ",a.shape)
print("a.dtype: ",a.dtype)
print("a.device: ", a.device)


# 生成张量系列函数
# %% 特殊值
zeros_tensor = torch.zeros((3,  2))      # 全0张量
ones_tensor = torch.ones((3,  2))      # 全0张量
eye_tensor = torch.eye(3)   # 3x3对角矩阵
full_tensor=torch.full((3,3),fill_value=0.25) #  3x3使用0.25填充的张量
empty_tensor=torch.empty(3,3) # 创建未初始化张量（内存中为随机值）
print("zeros_tensor:\n",zeros_tensor)
print("ones_tenor:\n", ones_tensor)
print("eye_tensor:\n",eye_tensor)
print("full_tensor:\n",full_tensor)
print("empty_tensor:\n",empty_tensor)

# %% 随机数
uniform_tensor = torch.rand(2, 3)   # [0,1)均匀分布张量（所有数概率相同）
normal_tensor = torch.randn(2, 3)   # 标准正态分布张量 （数据集中在均值0附近（约68%在±1标准差内））
intnormal_tensor=torch.randint(low=5,  high=15, size=(2,2))  # 输出如 tensor([[7, 6], [9, 12]])
print("uniform_tensor:\n",uniform_tensor)
print("normal_tensor:\n",normal_tensor)
print("intnormal_tensor:\n",intnormal_tensor)

# %% like系列 (继承了属性：形状、类型和设备)
oneslike_tensor = torch.ones_like(a)   # 与a形状相同的全1张量
zeroslike_tensor = torch.zeros_like(a)  # 与a形状相同的全0张量
fulllike_tensor=torch.full_like(a.float(), fill_value=3.14)   # 与a形状相同所有元素为3.14的张量

uniformlike_tensor=torch.rand_like(a.float())  # a形状相同的均匀分布 [0,1)张量
normallike_tensor=torch.randn_like(a.float())  # a形状相同的标准正态分布张量
normalintlike_tensor = torch.randint_like(a,  low=0, high=100)  # 整数均匀分布（需指定取值范围）0~99的整数 
print("oneslike_tensor:\n", oneslike_tensor)
print("zeroslike_tensor:\n", zeroslike_tensor)
print("fulllike_tensor:\n",fulllike_tensor)
print("uniformlike_tensor:\n",uniformlike_tensor)
print("normallike_tensor:\n", normallike_tensor)
print("normalintlike_tensor:\n", normalintlike_tensor)

# %%
arange_tensor = torch.arange(1,  10, 2)  # [1,3,5,7,9]生成固定步长的等差数列张量，左闭右开区间
linspace_tensor = torch.linspace(0, 1, 5)  # [0.0, 0.25, 0.5, 0.75, 1.0]生成指定元素数量的均分序列张量，闭区间包含起始和终止值
print("arange_tensor:\n",arange_tensor)
print("linspace_tensor:\n",linspace_tensor)


# %%
import numpy as np
np_array = np.array([1.0,  2.0])
print("np_array=",np_array)
torch_tensor = torch.from_numpy(np_array)   # 共享内存 
torch_tensor[0] = 3.0 
print("torch_tensor=",torch_tensor)
print("np_array",np_array)  # 输出 [3.0, 2.0]（原Numpy数组被修改）


# %% 改变张量形状
# 基础用法（元素总数需一致）
a = torch.arange(6)   # [0,1,2,3,4,5]
b = a.view(2,  3)     # 2x3矩阵 [[0,1,2],[3,4,5]]
c = a.reshape(3,  2)  # 3x2矩阵 [[0,1],[2,3],[4,5]]

# 内存连续性差异（关键区别）：view要求内存连续，reshape自动处理连续性
d = a[::2]           # 不连续张量 [0,2,4]
# e = d.view(3,1)     # 报错（需连续内存）
e = d.reshape(3,1)    # 正常执行 [[0],[2],[4]]

# %% 维度压缩与扩展
# 增加维度
x = torch.randn(3,4) 
y = torch.unsqueeze(x,  dim=0)  # 形状变为[1,3,4]

# 移除空维度：squeeze默认移除所有size=1的维度，可指定dim参数
z = torch.randn(1,3,1,4) 
w = torch.squeeze(z)            # 形状变为[3,4]

# %% 获取张量元素
# 基础索引与切片，注意：索引操作返回的是原张量的视图，修改会影响原数据
t = torch.tensor([[1,2,3],  [4,5,6], [7,8,9]])
print(t[0, :])     # 首行 → [1,2,3]
print(t[1:, 1:3])  # 后两行的1-2列 → [[5,6],[8,9]]
# 高级选择方法
# 布尔掩码选择
mask = t > 5
# 把false全部去掉，然后拼接成新的张量
selected = t[mask]  # 返回一维张量 [6,7,8,9]

# torch.where 条件筛选
result = torch.where(t%2==0,  t, torch.zeros_like(t))   
# 偶数保留，奇数置零 → [[0,2,0],[4,0,6],[0,8,0]]

# %% 拼接与拆分
# 维度拼接
a = torch.randn(2,3) 
print("a=\n",a)
b = torch.randn(2,3)
print("b=\n",b)
# cat:沿现有维度拼接张量，不新增维度;除拼接维度外，其他维度必须相同;适用于需直接扩展数据量（如合并通道）
# 合并特征：将多个通道的特征图拼接（如ResNet中的残差连接）
# 序列处理：合并不同时间步的隐藏状态
cat_tensor = torch.cat([a,b],  dim=0)  # 4x3（行拼接），cat_shape → torch.Size([4,3])，
print("cat_tensor=\n",cat_tensor)
# statck:在新维度上堆叠张量，新增一个维度;所有输入张量形状必须完全相同;适用于需保留独立结构（如时间步或批次）
# 构建批次数据：将单张图片堆叠为批次形式（如从(3,224,224)到(N,3,224,224)）
# 时间序列建模：将多个时间步的输出堆叠为三维张量（如RNN输入）
stack_tensor = torch.stack([a,b])      # 2x2x3（新增维度），stack_shape → torch.Size([2,2,3])
print("stack_tensor=\n",stack_tensor)
# 拆分操作
x = torch.arange(5)   # [0, 1, 2, 3, 4]
print("x=\n",x)
# chunk将张量沿指定维度均分为若干块。若无法整除，最后一块会较小
y = torch.chunk(x,  chunks=2, dim=0) # 输出：[tensor([0, 1, 2]), tensor([3, 4])]
print("y=\n",y)

# split按固定大小或自定义尺寸列表拆分张量
# 按固定大小拆分 
y = torch.split(x,  split_size_or_sections=2, dim=0)# 输出：[tensor([0, 1]), tensor([2, 3]), tensor([4])]
print("y=\n",y)
# 按自定义列表拆分 
y = torch.split(x,  split_size_or_sections=[3, 2], dim=0)  # 第0维总长度为5，拆分3+2 # 输出：[tensor([0, 1, 2]), tensor([3, 4])]
print("y=\n",y)


##--------------------------- 比较大小操作----------------------
# %% 整体近似比较，判断张量是否在误差范围内近似相等
#∣A−B∣≤atol+rtol×∣B∣
#若所有元素的差值均满足上述不等式，则视为整体近似相等
a = torch.tensor([1.0,  2.0], dtype=torch.float32) 
b = torch.tensor([1.001,  2.003], dtype=torch.float32) 
print(torch.allclose(a,  b, rtol=0.01, atol=0.02))  # 输出：True
# 与严格相等的区别
#严格相等：torch.equal(a,  b)，要求所有元素完全相同
print(torch.equal(a,b))

# %% 逐元素比较
x = torch.tensor([[1,  4], [2, 5]])
y = torch.tensor([[1,  3], [3, 5]])

print(torch.eq(x,  y))   # 等于比较 
# tensor([[ True, False],
#         [False,  True]])
 
print(torch.gt(x,  y))   # 大于比较 
# tensor([[False,  True],
#         [False, False]])

print(torch.le(x,y))  # 小于等于比较
# tensor([[ True, False],
#        [ True,  True]])

print(torch.ge(x,y)) # 大于等于比较
#tensor([[ True,  True],
#        [False,  True]])

print(torch.lt(x,y)) # 小于比较
#tensor([[False, False],
#        [ True, False]])

print(torch.ne(x,y))# 不等于比较
#tensor([[False,  True],
#       [ True, False]])

# %% 特殊值判断
t = torch.tensor([0,  1, float("nan"), 2])
print(torch.isnan(t))   # 检测缺失值 
# tensor([False, False,  True, False])

#--------------------------------基本运算---------------------------
## 元素级运算
a = torch.tensor([1,  4])
b = torch.tensor([2,  3])
 
# %% 四则运算（支持广播）
print(a + b)  # 逐元素加法 tensor([3, 7])
print(a * 2)  # 标量乘法 tensor([2, 8])
print(a-b)    # 逐元素相减 tensor([-1,  1])
print(a/b)    # 逐元素相除 tensor([0.5000, 1.3333])
print(a//b)   # 逐元素整除 tensor([0, 1])
print(a%b)    # 逐元素取余 tensor([1, 1])
 
# %% 数学函数 
print(torch.sqrt(a.float()))   # 平方根 tensor([1.0000, 2.0000])
print(torch.rsqrt(a.float()))  # 平方根倒数 tensor([1.0000, 0.5000])
print(torch.log(b.float()))    # 自然对数 tensor([0.6931, 1.0986])
print(torch.exp(a.float()))    # 指数 tensor([ 2.7183, 54.5981])
print(torch.pow(a.float(),3))  # 幂 tensor([ 1., 64.])
print(a.float()**3)            # 幂 tensor([ 1., 64.])

##矩阵运算
# %%矩阵乘法 torch.mm和torch.matmul
# 二维结果相同
mat1 = torch.randn(2,  3)
mat2 = torch.randn(3,  2)
print(torch.mm(mat1,  mat2))  # 结果形状：2x2 
print(torch.matmul(mat1,mat2)) # 结果相同

# 一维显著差异
v1 = torch.tensor([1,  2, 3])   # 形状 (3,)
v2 = torch.tensor([4,  5, 6])   # 形状 (3,)
# torch.mm  不支持一维输入 → 报错 
# result = torch.mm(v1,  v2)  # RuntimeError 
# torch.matmul  返回点积（标量）
result = torch.matmul(v1,  v2)  # 输出 32 
print(result)

# 三维广播机制
A = torch.randn(2,  3, 4)  # 批量维度2，每个元素为3x4矩阵 
B = torch.randn(4,  5)      # 二维矩阵 
# torch.mm  不支持三维输入 → 报错 
# C_mm = torch.mm(A,  B)    # RuntimeError 
# torch.matmul  自动广播B为 (2,4,5) → 结果形状 (2,3,5)
C_matmul = torch.matmul(A,  B)
print(C_matmul)

# 批量矩阵乘法（高维场景）
A = torch.randn(5,  2, 3)  # 批量维度5，每个元素为2x3矩阵 
B = torch.randn(5,  3, 4)  # 批量维度5，每个元素为3x4矩阵 
# torch.mm  无法处理 → 报错 
# C_mm = torch.mm(A,  B)    # RuntimeError 
# torch.matmul  批量相乘 → 结果形状 (5,2,4)使用 torch.matmul 时，需确保最后两个维度满足矩阵乘法规则
C_matmul = torch.matmul(A,  B)
print(C_matmul)


# %% 转置操作 
A= torch.randn(2,  3)
print(A.T)  # 形状变为3x2 

# %% 逆矩阵
A_tensor = torch.tensor([[1.0,  2.0], [3.0, 4.0]])
inv_A_tensor = torch.inverse(A_tensor) 
print(inv_A_tensor)

# %% 矩阵的迹
trace_A_tensor = torch.trace(A_tensor)   # 仅支持2D张量 
print(trace_A_tensor)

##广播机制
# %% 标量自动广播 
vec = torch.tensor([[1],  [2]])  # 2x1 
scalar = torch.tensor([10])      # 标量自动广播 
print(vec + scalar)
# tensor([[11],
#         [12]])

vec = torch.tensor([1,  2, 3])     # 形状 (3,)
mat = torch.ones(2,  3)            # 形状 (2,3)
result = vec + mat                # vec广播为 [[1,2,3],[1,2,3]]
# tensor([[2,3,4],
#         [2,3,4]])

a = torch.ones(4,  1, 3)    # 形状 (4,1,3)
b = torch.ones(    2, 3)    # 形状 (2,3)
result = a + b             # a 的广播：将第2维（原为1）复制为2，最终形状变为 (4,2,3)
                           # b 的广播：将第1维（原为1）复制为4，最终形状变为 (4,2,3)
                           # 最终形状 (4,2,3)

#--------------------统计相关运算-------------
#维度指定：dim=0表示列方向操作，dim=1为行方向3
#内存共享：索引操作（如argmax）返回的新张量与原始张量共享内存
#数据类型：整型张量需转换为浮点型才能进行标准差等计算1
#性能优化：大张量计算建议使用torch.nanmean() 处理缺失值
# %% 均值与标准差
x = torch.tensor([[2,  5], [8, 3], [1, 6]], dtype=torch.float32) 
# 全局均值 
mean_all = torch.mean(x)   # tensor(4.1667)
# 按行计算均值 
mean_row = torch.mean(x,  dim=1)  # tensor([3.5, 5.5, 3.5])
# 全局标准差（无偏估计）
std_all = torch.std(x)   # tensor(2.7080)
# 按列计算标准差（有偏估计）
std_col = torch.std(x,  dim=0, unbiased=False)  # tensor([3.0414, 1.6997])

# %% 最大值/最小值及其位置
x = torch.tensor([[2,  5], [8, 3], [1, 6]], dtype=torch.float32) 
# 全局最大值 
max_val = torch.max(x)   # tensor(8.) 
# 按列取最大值及其索引 
max_col, max_idx = torch.max(x,  dim=0)
# max_col: tensor([8., 6.]), max_idx: tensor([1, 2])
# 全局最小值位置 
min_pos = torch.argmin(x)   # tensor(4) 对应元素1的索引 

# %% 张量排序
x = torch.tensor([[2,  5], [8, 3], [1, 6]], dtype=torch.float32) 
# 全局排序（升序）
sorted_val, sorted_idx = torch.sort(x.flatten()) 
# sorted_val: tensor([1., 2., 3., 5., 6., 8.])
# sorted_idx: tensor([4, 0, 3, 1, 2, 5])
 
# 按行降序排序 
sorted_row, idx_row = torch.sort(x,  dim=1, descending=True)
# sorted_row: 
# tensor([[5., 2.],
#        [8., 3.],
#        [6., 1.]])

# %% 求和运算
x = torch.tensor([[2,  5], [8, 3], [1, 6]], dtype=torch.float32) 
# # 全局求和 
sum_all = torch.sum(x)   # tensor(25.) 
# 按列累加和 
cumsum_col = torch.cumsum(x,  dim=0)
# tensor([[ 2.,  5.],
#        [10.,  8.],
#        [11., 14.]])

# 保留维度求和 
sum_keepdim = torch.sum(x,  dim=1, keepdim=True)
# tensor([[ 7.],
#        [11.],
#        [ 7.]])

# %% Top-K 值获取
x = torch.tensor([[2,  5], [8, 3], [1, 6]], dtype=torch.float32) 
# 获取前2大的值及其索引 
top2_val, top2_idx = torch.topk(x.flatten(),  k=2)
# top2_val: tensor([8., 6.]), top2_idx: tensor([1, 5])

# %% 中位数计算
x = torch.tensor([[2,  5], [8, 3], [1, 6]], dtype=torch.float32) 
median_all = torch.median(x)   # tensor(5.) 
median_col = torch.median(x,  dim=0).values  # tensor([2., 5.])

#***************************************自动微分*************************
# %%
x=torch.tensor([[1.0,2.0],[3.0,4.0]],requires_grad=True) # 注意默认requires_grad=False
y=torch.sum(x**2+2*x+1) # 自动构建计算图
print("x.reguires_grad:",x.requires_grad) # 这两个变量都可导（因为x可以求导，所以计算得到的y也可以求导）
print("y.requires_grad:",y.requires_grad)
print("x:",x)
print("y:",y)

y.backward() # 调用.backward()时从最后一个节点反向遍历计算图，应用链式法则
x.grad # 计算出的梯度存储在张量的.grad属性中，通过x的grad属性即可获取此时的x的梯度信息


#***********************************神经网络层******************************************
# %% 
# 二维卷积（图像处理）
conv = nn.Conv2d(
    in_channels=3,   # 输入通道数（RGB图像为3）
    out_channels=16, # 输出通道数（特征图数量）
    kernel_size=3,   # 卷积核尺寸 
    stride=1,        # 步长 
    padding=1        # 填充（保持尺寸不变）
)
 
# 示例：处理4x128x128的RGB图像 
x = torch.randn(4,  3, 128, 128)  # (batch, channel, height, width)
output = conv(x)  # 输出形状：(4, 16, 128, 128)
print(output.shape)

# %% 转置卷积
# 图像生成（如GAN）在生成器中，转置卷积将随机噪声逐步上采样为高分辨率图像
# 语义分割（如FCN），将编码器提取的低分辨率特征图恢复到原图尺寸，用于像素级分类
# 定义输入：模拟编码器输出的低分辨率特征图（batch_size=1, 通道数=1）
input_tensor = torch.tensor([[[[1.,  2.], [3., 4.]]]], dtype=torch.float32)   # shape: (1, 1, 2, 2)
 
# 定义转置卷积层 
trans_conv = nn.ConvTranspose2d(
    in_channels=1, 
    out_channels=1, 
    kernel_size=3,  # 3x3卷积核 
    stride=1,       # 步长控制输出放大倍数 
    padding=0       # 输入边缘不填充 
)
 
# 执行上采样操作 
output = trans_conv(input_tensor)
print("Output shape:", output.shape)   # 输出形状: (1, 1, 4, 4)
print("Output values:\n", output.detach()) 

# %% 池化层
# 最大值池化（窗口2x2，步长2）
maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
# 自适应池化（输出固定为3x3）
adaptive_pool = nn.AdaptiveAvgPool2d((3,3))  # 输入尺寸任意 
# 传统池化（输入需适配参数）
avg_pool = nn.AvgPool2d(kernel_size=2, stride=2)  # 输入需为偶数尺寸 
 
x = torch.randn(4,  16, 128, 128)
out_max = maxpool(x)     # 形状变为(4, 16, 64, 64)
out_adapt = adaptive_pool(x)  # 形状变为(4, 16, 100, 100)

# %%激活函数层
# Sigmoid
x = torch.tensor([-2.0,  0.0, 1.5])
output = torch.sigmoid(x)   # 输出：[0.1192, 0.5000, 0.8176]

# Tanh
x = torch.tensor([-1.0,  0.0, 2.0])
output = torch.tanh(x)   # 输出：[-0.7616, 0.0000, 0.9640]

# ReLU
relu = torch.nn.ReLU() 
x = torch.tensor([-3.0,  0.5, 4.0])
output = relu(x)  # 输出：[0.0, 0.5, 4.0]

# Leaky ReLU
leaky_relu = torch.nn.LeakyReLU(negative_slope=0.01) 
x = torch.tensor([-2.0,  0.0, 1.0])
output = leaky_relu(x)  # 输出：[-0.02, 0.0, 1.0]

# ELU
elu = torch.nn.ELU(alpha=1.0) 
x = torch.tensor([-1.0,  0.0, 2.0])
output = elu(x)  # 输出：[-0.6321, 0.0, 2.0]

#***********************************循环层**********************************************
# %% LSTM
lstm = nn.LSTM(
    input_size=100,   # 输入特征维度 
    hidden_size=256,  # 隐藏状态维度 
    num_layers=2,     # 堆叠层数 
    batch_first=True  # 输入格式为(batch, seq_len, feature)
)
 
# 输入序列（batch=4，序列长度=10）
x = torch.randn(4,  10, 100)
output, (h_n, c_n) = lstm(x)  # output形状：(4,10,256)

# %% ***********************************全连接层**************************************************
# 全连接网络结构示例 
class Classifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc  = nn.Sequential(
            nn.Linear(256*7*7, 512),  # 展平后输入 
            nn.ReLU(),
            nn.Linear(512, 10)        # 输出10分类 
        )
    
    def forward(self, x):
        x = x.view(x.size(0),  -1)     # 展平操作 
        return self.fc(x) 
    
# **********************************高维数组数据处理***********************************
# %%-----------------------------分类模型数据准备-------------------------------
from sklearn.datasets import load_iris
import numpy as np
# 分类数据准备
iris_X, iris_y = load_iris(return_X_y=True)
print("iris_X.shape:", iris_X.shape)
print("iris_y.shape:", iris_y.shape)

# 将数据转为张量
train_xt = torch.from_numpy(iris_X.astype(np.float32))
train_yt = torch.from_numpy(iris_y.astype(np.int64))
print("train_xt.dtype:", train_xt.dtype)
print("train_yt.dtype:", train_yt.dtype)

# 使用TensorDataset将X和y整理到一起
train_data = Data.TensorDataset(train_xt, train_yt) 
# 定义一个数据加载器，将训练集进行批量处理
train_loader = Data.DataLoader(
    dataset=train_data,
    batch_size=10,
    shuffle=True,
    num_workers=0
)

# 检查训练数据集的一个batch样本的维度是否正确
for step, (b_x, b_y) in enumerate(train_loader):
    if step > 0:
        break
print("b_x.shape:", b_x.shape)
print("b_y.shape:", b_y.shape)
print("b_x.dtype:", b_x.dtype)
print("b_y.dtype:", b_y.dtype)

# %%
