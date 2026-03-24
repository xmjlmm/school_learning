# import plotly.graph_objects as go
# import networkx as nx
# import pandas as pd
# # 示例数据
# # data = {
# #     '始发分拣中心': ['SC1', 'SC10', 'SC12', 'SC15', 'SC15'],
# #     '到达分拣中心': ['SC25', 'SC57', 'SC6', 'SC47', 'SC7']
# # }
#
# data = pd.read_excel("F:\\数模\\2024年国赛复习资料\\论文\\MathorCupC\\C题\\附件\\附件3.xlsx")
# ds = data['到达分拣中心']
# dfs = data['始发分拣中心']
# # # 定义起点-终点数据
# # data = {
# #     '始发分拣中心': ['SC1', 'SC10', 'SC12', 'SC15', 'SC15'],
# #     '到达分拣中心': ['SC25', 'SC57', 'SC6', 'SC47', 'SC7']
# # }
#
# data = {
#     '始发分拣中心': dfs,
#     '到达分拣中心': ds
# }
# #
# df = pd.DataFrame(data)
#
# # 创建图
# G = nx.DiGraph()
#
# # 添加边
# for _, row in pd.DataFrame(data).iterrows():
#     G.add_edge(row['始发分拣中心'], row['到达分拣中心'])
#
# # 获取节点的位置
# pos = nx.spring_layout(G)
#
# # 节点坐标
# x_nodes = [pos[node][0] for node in G.nodes()]
# y_nodes = [pos[node][1] for node in G.nodes()]
#
# # 边坐标
# x_edges = []
# y_edges = []
# for edge in G.edges():
#     x_edges.append(pos[edge[0]][0])
#     x_edges.append(pos[edge[1]][0])
#     x_edges.append(None)  # None 用于分隔边的线段
#     y_edges.append(pos[edge[0]][1])
#     y_edges.append(pos[edge[1]][1])
#     y_edges.append(None)
#
# # 创建图形
# fig = go.Figure()
#
# # 添加节点
# fig.add_trace(go.Scatter(x=x_nodes, y=y_nodes, mode='markers+text', text=list(G.nodes()),
#                          marker=dict(size=1, color='lightblue'), textposition='top center'))
#
# # 添加边
# fig.add_trace(go.Scatter(x=x_edges, y=y_edges, mode='lines+markers', line=dict(width=2, color='gray'),
#                          marker=dict(size=8, color='gray')))
#
# # 添加箭头
# for edge in G.edges():
#     fig.add_annotation(
#         x=pos[edge[1]][0],
#         y=pos[edge[1]][1],
#         ax=pos[edge[0]][0],
#         ay=pos[edge[0]][1],
#         xref="x",
#         yref="y",
#         axref="x",
#         ayref="y",
#         showarrow=True,
#         arrowsize=2,
#         arrowwidth=1,
#         arrowhead=2,
#         arrowcolor="gray"
#     )
#
# # 设置布局
# fig.update_layout(title='分拣中心运输线路有向图', showlegend=False)
#
# fig.show()


import networkx as nx
import matplotlib.pyplot as plt

# 示例数据
data = {
    '始发分拣中心': ['SC1', 'SC10', 'SC12', 'SC15', 'SC15'],
    '到达分拣中心': ['SC25', 'SC57', 'SC6', 'SC47', 'SC7']
}

# 创建图
G = nx.DiGraph()

# 添加边
for _, row in pd.DataFrame(data).iterrows():
    G.add_edge(row['始发分拣中心'], row['到达分拣中心'])

# 尝试不同的布局算法
pos = nx.kamada_kaway_layout(G)  # 尝试 Kamada-Kaway 布局

plt.figure(figsize=(14, 12))  # 增加图形尺寸

# 绘制有向图
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue',
        edge_color='gray', font_size=12, font_weight='bold',
        arrows=True, arrowsize=20, width=2)

plt.title("分拣中心运输线路有向图", fontsize=16)
plt.tight_layout()  # 调整图形布局
plt.show()
