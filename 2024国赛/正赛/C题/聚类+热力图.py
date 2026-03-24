import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
from matplotlib.font_manager import FontProperties

# 设置字体属性
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=10)

# 1. 读取数据
data = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\附件2预处理单价(已处理).xlsx", sheet_name="Sheet1")

# 2. 数据预处理
# 去除重复的作物名称（保留第一个出现的）
data = data.drop_duplicates(subset=['作物名称'])

# 选择聚类的特征
features = ['种植成本/(元/亩)', '销售单价(最大值)', '预期销售量']

# 选择用于聚类的列
cluster_data = data[features].copy()  # 使用.copy()来避免SettingWithCopyWarning
cluster_data['作物名称'] = data['作物名称']

# 处理缺失值
cluster_data_clean = cluster_data.dropna()
data_clean = data.loc[cluster_data_clean.index]  # 保留对应的行

# 确保所有聚类特征都是数值类型
for col in features:
    cluster_data_clean[col] = pd.to_numeric(cluster_data_clean[col], errors='coerce')

# 处理因转换而产生的NaN值
cluster_data_clean = cluster_data_clean.dropna()
data_clean = data.loc[cluster_data_clean.index]

# 数据标准化
scaler = StandardScaler()
scaled_data = scaler.fit_transform(cluster_data_clean[features])

# 3. 计算作物之间的相关性矩阵
# 将标准化数据与作物名称重新组合
scaled_data_df = pd.DataFrame(scaled_data, columns=features, index=cluster_data_clean['作物名称'])
corr_matrix = scaled_data_df.corr()

# 计算作物之间的相关性（基于标准化后的数据）
crop_corr_matrix = pd.DataFrame(index=scaled_data_df.index, columns=scaled_data_df.index)

for i in scaled_data_df.index:
    for j in scaled_data_df.index:
        crop_corr_matrix.loc[i, j] = np.corrcoef(scaled_data_df.loc[i], scaled_data_df.loc[j])[0, 1]
crop_corr_matrix.to_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\农作物相关系数矩阵.xlsx")
# 转化为距离矩阵（相关性转化为距离）
distance_matrix = pdist(crop_corr_matrix.astype(float), metric='euclidean')

# 层次聚类
Z = linkage(distance_matrix, method='average')

# 创建一个子图，左边为树状图，上面为树状图，右下角为热力图
fig = plt.figure(figsize=(18, 12))  # 增加整体图像宽度

# 上方树状图
ax_dendro_x = fig.add_axes([0.3, 0.9, 0.45, 0.05])  # 缩小树状图的宽度
dendrogram(Z, ax=ax_dendro_x, color_threshold=0, orientation='top')
ax_dendro_x.set_xticks([])
ax_dendro_x.set_yticks([])

# 左侧树状图
ax_dendro_y = fig.add_axes([0.25, 0.3, 0.05, 0.6])
dendrogram(Z, ax=ax_dendro_y, color_threshold=0, orientation='left')
ax_dendro_y.set_xticks([])
ax_dendro_y.set_yticks([])

# 根据聚类结果重新排列数据
dendro_idx = np.arange(len(crop_corr_matrix.index))
dendro_idx = np.array([dendro_idx[i] for i in dendrogram(Z, no_plot=True)['leaves']])

# 绘制热力图
ax_heatmap = fig.add_axes([0.3, 0.3, 0.6, 0.6])
sns.heatmap(
    crop_corr_matrix.iloc[dendro_idx, dendro_idx].astype(float),  # 确保数据类型为浮点型
    annot=False, fmt=".2f", linewidths=.5, cmap='coolwarm', cbar=True,
    ax=ax_heatmap, cbar_kws={"shrink": 1.0, "aspect": 15, "pad": 0.1}
)

# 设置中文标题和标签
ax_heatmap.set_xticks(np.arange(len(crop_corr_matrix.index)) + 0.5)
ax_heatmap.set_yticks(np.arange(len(crop_corr_matrix.index)) + 0.5)
ax_heatmap.set_xticklabels(crop_corr_matrix.index[dendro_idx], rotation=90, fontproperties=font)
ax_heatmap.set_yticklabels(crop_corr_matrix.index[dendro_idx], rotation=0, fontproperties=font)

# 隐藏左侧的 y 轴标签
ax_heatmap.yaxis.set_ticks_position('right')
ax_heatmap.yaxis.set_label_position('right')

# 调整 y 轴标签位置（向右移动）
for label in ax_heatmap.get_yticklabels():
    label.set_horizontalalignment('right')
    label.set_x(label.get_position()[0] + 0.05)  # 这里的0.1可以根据需要调整


# 调整右边的边距
plt.subplots_adjust(right=0.85)  # 这里调整右边距以增加空间

# 显示图形
plt.show()
