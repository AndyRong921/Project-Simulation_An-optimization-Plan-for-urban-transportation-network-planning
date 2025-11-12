# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re
from scipy.spatial import KDTree
from matplotlib.lines import Line2D

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 数据加载
routes = pd.read_csv(r"Bus_Routes.csv",
                     usecols=['Route_Name', 'Route_Numb', 'Route_Type'])
stops = pd.read_csv(r"Bus_Stops.csv",
                    usecols=['stop_id', 'Y', 'X', 'Routes_Ser'])


# 2. 数据预处理（增强清洗）
def clean_route_ser(s):
    """清洗站点路由标识字段"""
    # 保留字母、数字、逗号和空格
    cleaned = re.sub(r'[^A-Z0-9, ]', '', str(s).upper())
    # 转换CityLink标识为纯颜色名称（关键修复）
    cleaned = re.sub(r'CITYLINK\s+(\w+)', r'\1', cleaned)
    # 规范逗号分隔格式
    cleaned = re.sub(r'\s*,\s*', ',', cleaned).strip(',')
    return cleaned


stops['Routes_Ser'] = stops['Routes_Ser'].apply(clean_route_ser).fillna('')
stops['stop_id'] = stops['stop_id'].astype(str)

# 清洗线路编号字段（关键修复）
routes['Route_Numb'] = (
    routes['Route_Numb']
    .astype(str)
    .str.strip()
    .str.upper()
    .str.replace(r'CITYLINK[\s\-]*', '', regex=True)  # 彻底移除所有前缀变体
    .str.strip()
)

# 3. 颜色映射定义（修正版）
citylink_colors = {
    'BLUE': '#1f77b4',  # 蓝色
    'BROWN': '#8c564b',  # 棕色
    'GOLD': '#ff7f0e',  # 金色
    'GREEN': '#2ca02c',  # 绿色
    'LIME': '#00ff00',  # 新增青柠色
    'NAVY': '#000080',  # 海军蓝
    'ORANGE': '#d62728',  # 橙色
    'PINK': '#ff69b4',  # 新增粉色
    'PURPLE': '#9467bd',  # 紫色
    'RED': '#ff0000',  # 新增红色
    'SILVER': '#c0c0c0',  # 新增银色
    'YELLOW': '#ffff00'  # 新增黄色
}

route_type_colors = {
    'MTA Commuter Bus': '#4b0082',  # 通勤巴士紫色
    'MTA Local Bus - CityLink': None,  # 特殊标记，需单独处理
    'MTA Local Bus - Express BusLink': '#ffd700',  # 金色（示例）
    'MTA Local Bus - LocalLink': '#2ca02c'  # 常规公交绿色
}

# 4. 构建网络
G = nx.Graph()
coords = stops[['X', 'Y']].values.astype(float)
stop_ids = stops['stop_id'].tolist()
pos_dict = {sid: (x, y) for sid, x, y in zip(stop_ids, coords[:, 0], coords[:, 1])}
G.add_nodes_from(stop_ids)

# 5. 生成公交连接（带调试输出）
for _, route in routes.iterrows():
    route_num = route['Route_Numb'].strip()
    route_type = route['Route_Type']

    # 获取颜色（关键逻辑）
    if route_type == 'MTA Local Bus - CityLink':
        color = citylink_colors.get(route_num.upper(), '#dddddd')
    else:
        color = route_type_colors.get(route_type, '#2ca02c')

    # 优化正则匹配（关键修复）
    pattern = re.compile(rf'(?:^|,)\s*{re.escape(route_num)}\s*(?:,|$)', re.IGNORECASE)
    mask = stops['Routes_Ser'].str.contains(pattern, na=False)
    related_ids = stops.loc[mask, 'stop_id'].tolist()

    # 生成连接
    edge_count = 0
    for i in range(len(related_ids) - 1):
        u, v = related_ids[i], related_ids[i + 1]
        if not G.has_edge(u, v):
            G.add_edge(u, v, color=color, type='bus', width=2.0)
            edge_count += 1

# 6. 添加步行连接
kdtree = KDTree(coords)
walk_pairs = kdtree.query_pairs(0.0045)
for i, j in walk_pairs:
    u, v = stop_ids[i], stop_ids[j]
    if not G.has_edge(u, v):
        G.add_edge(u, v, color='#cccccc', type='walk', width=0.5)

# 7. 可视化
plt.figure(figsize=(18, 12), dpi=300)  # 增加dpi以提高图片分辨率
nx.draw_networkx_nodes(G, pos_dict, node_size=20, node_color='lightgrey', alpha=0.6)

# 绘制步行连接
walk_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'walk']
nx.draw_networkx_edges(G, pos_dict, edgelist=walk_edges,
                       edge_color='#cccccc', width=0.5, alpha=0.3)

# 绘制公交线路
bus_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'bus']
colors = [G[u][v]['color'] for u, v in bus_edges]
widths = [G[u][v]['width'] for u, v in bus_edges]
nx.draw_networkx_edges(G, pos_dict, edgelist=bus_edges,
                       edge_color=colors, width=widths, alpha=0.9)

# 标注关键节点
degrees = dict(G.degree())
top_nodes = sorted(degrees, key=lambda x: degrees[x], reverse=True)[:5]
labels = {n: f"{n}\n({degrees[n]}Connection)" for n in top_nodes}
nx.draw_networkx_labels(G, pos_dict, labels,
                        font_size=10, font_color='darkred',
                        bbox=dict(facecolor='white', alpha=0.8))

# 添加图例
legend_elements = [
    Line2D([0], [0], color='#4b0082', lw=2, label='Commuter buses'),
    Line2D([0], [0], color='#1f77b4', lw=2, label='CityLink Blue Line'),
    Line2D([0], [0], color='#8c564b', lw=2, label='CityLink Brown Line'),
    Line2D([0], [0], color='#2ca02c', lw=2, label='Regular buses）'),
    Line2D([0], [0], color='#cccccc', lw=2, label='Pedestrian connection')
]
plt.legend(handles=legend_elements, loc='upper right')

plt.title("Baltimore Visualization of the bus network", fontsize=16)
plt.axis('off')
plt.tight_layout()

# 保存为PNG格式
plt.savefig("bus_network.png", format="png", dpi=300, bbox_inches='tight')
plt.show()

# 1. 增加少量的公交线路连接：仅对度数较低的节点进行适度优化，每个节点最多增加1个连接
low_degree_nodes = [n for n, d in G.degree() if d < 4]  # 找到度数较低的节点
for node in low_degree_nodes:
    # 选择性地增加连接，仅选择部分低度节点进行连接
    low_degree_neighbors = [n for n, d in G.degree() if n != node and d < 4]
    selected_neighbors = low_degree_neighbors[:1]  # 每个节点最多增加1个连接
    for target in selected_neighbors:
        if not G.has_edge(node, target):
            G.add_edge(node, target, color='blue', type='bus', width=2.0)

# 2. 增加适度的步行连接：增加步行连接的阈值，减少连接数量
walk_pairs = kdtree.query_pairs(0.0035)  # 增加步行连接的阈值，减少连接数量
for i, j in walk_pairs:
    u, v = stop_ids[i], stop_ids[j]
    if not G.has_edge(u, v):
        G.add_edge(u, v, color='#cccccc', type='walk', width=0.5)

# 3. 稍微增加公交线路交叉连接：限制每条线路最多增加1条连接
for _, route in routes.iterrows():
    route_num = route['Route_Numb'].strip()
    # 获取与该线路相关的站点
    pattern = re.compile(rf'(?:^|,)\s*{re.escape(route_num)}\s*(?:,|$)', re.IGNORECASE)
    mask = stops['Routes_Ser'].str.contains(pattern, na=False)
    related_ids = stops.loc[mask, 'stop_id'].tolist()

    # 选择性增加连接：只连接每条线路中的一小部分非相邻站点
    for i in range(len(related_ids) - 1):
        for j in range(i + 2, min(i + 3, len(related_ids))):  # 每条线路最多增加1个连接
            u, v = related_ids[i], related_ids[j]
            if not G.has_edge(u, v):
                G.add_edge(u, v, color='orange', type='bus', width=1.5)

# 4. 计算优化后的网络特征
network_density = nx.density(G)
average_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
clustering_coeff = nx.average_clustering(G)