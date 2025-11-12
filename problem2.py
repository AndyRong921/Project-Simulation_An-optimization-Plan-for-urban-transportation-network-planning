import pandas as pd
import matplotlib.pyplot as plt
import re
from matplotlib.lines import Line2D
from geopy.distance import (geodesic)
from scipy.spatial import KDTree
import random
import networkx as nx



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
plt.figure(figsize=(18, 12))
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
labels = {n: f"{n}\n({degrees[n]}连接)" for n in top_nodes}
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
plt.show()

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters


for _, route in routes.iterrows():
    ...
    for i in range(len(related_ids) - 1):
        u = related_ids[i]
        v = related_ids[i + 1]
        coord_u = (stops.loc[stops['stop_id'] == u, 'Y'].values[0],
                   stops.loc[stops['stop_id'] == u, 'X'].values[0])
        coord_v = (stops.loc[stops['stop_id'] == v, 'Y'].values[0],
                   stops.loc[stops['stop_id'] == v, 'X'].values[0])

        distance = calculate_distance(coord_u, coord_v)
        bus_speed = 29300 / 3600
        travel_time = distance / bus_speed

        G.add_edge(u, v,
                   color=color,
                   type='bus',
                   weight=travel_time)
walk_speed = 1.4

for i, j in walk_pairs:
    u = stop_ids[i]
    v = stop_ids[j]
    coord_u = (stops.loc[stops['stop_id'] == u, 'Y'].values[0],
               stops.loc[stops['stop_id'] == u, 'X'].values[0])
    coord_v = (stops.loc[stops['stop_id'] == v, 'Y'].values[0],
               stops.loc[stops['stop_id'] == v, 'X'].values[0])

    distance = calculate_distance(coord_u, coord_v)
    walk_time = distance / walk_speed

    G.add_edge(u, v,
               color='#cccccc',
               type='walk',
               weight=walk_time)

def calculate_accessibility(G, time_threshold=1500):
    accessibility = {}
    for node in G.nodes():

        times = nx.single_source_dijkstra_path_length(G, node, weight='weight')
        count = sum(1 for t in times.values() if t <= time_threshold)
        accessibility[node] = count
    return accessibility

accessibility = calculate_accessibility(G)

# 创建画布和轴
plt.figure(figsize=(18, 12))
ax = plt.gca()

# 节点颜色
node_colors = [accessibility.get(node, 0) for node in G.nodes()]
nodes = nx.draw_networkx_nodes(
    G, pos_dict,
    node_size=30,
    node_color=node_colors,
    cmap='viridis',
    alpha=0.8,
    ax=ax
)

# 设置颜色映射
sm = plt.cm.ScalarMappable(
    cmap='viridis',
    norm=plt.Normalize(
        vmin=min(node_colors),
        vmax=max(node_colors)
    )
)
sm.set_array(node_colors)
plt.colorbar(sm, ax=ax, label='The number of stations can be reached in 25 minutes')  # 显式指定Axes

# 绘制步行边，增加柔滑效果
nx.draw_networkx_edges(
    G, pos_dict,
    edgelist=walk_edges,
    edge_color='#cccccc',
    width=1.5,  # 增加宽度
    alpha=0.4,  # 更低的透明度
    ax=ax,
    style='solid'  # 使用实线
)

# 绘制公交边，增加柔滑效果
nx.draw_networkx_edges(
    G, pos_dict,
    edgelist=bus_edges,
    edge_color=colors,
    width=2,  # 增加宽度
    alpha=0.7,  # 更高的透明度
    ax=ax,
    style='solid'  # 使用实线
)

# 绘制标签
nx.draw_networkx_labels(
    G, pos_dict, labels,
    font_size=10,
    font_color='darkred',
    bbox=dict(facecolor='white', alpha=0.8),
    ax=ax
)

# 启用抗锯齿
ax.set_facecolor('white')  # 背景为白色
plt.title("Analysis of bus network accessibility - 25 minutes", fontsize=16)
plt.axis('off')
plt.tight_layout()

# 设置抗锯齿
ax.set_aspect('auto')
ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)
plt.show()

def convert_to_utm(df, lon_col='X', lat_col='Y'):
    """将经纬度转换为UTM坐标系"""
    p = Proj(proj='utm', zone=18, ellps='WGS84')
    x, y = p(df[lon_col].values, df[lat_col].values)
    return x, y


# 将站点的经纬度转换为UTM坐标
stops['x'], stops['y'] = convert_to_utm(stops)
coords = stops[['x', 'y']].values.astype(float)
pos_dict = {sid: (x, y) for sid, x, y in zip(stops['stop_id'], coords[:, 0], coords[:, 1])}


def generate_population_points(coords, num=1000):
    """在整个网络覆盖范围内生成均匀分布的人口点"""
    x_min, y_min = np.min(coords, axis=0)
    x_max, y_max = np.max(coords, axis=0)
    return np.column_stack([
        np.random.uniform(x_min, x_max, num),
        np.random.uniform(y_min, y_max, num)
    ])


# 随机生成人口点
sample_population = generate_population_points(coords)

def add_random_station_and_connection(G, pos_dict, num_new_stations=3):
    """随机新增站点并连接到原有网络"""
    # 确保新站点的ID从现有的站点ID开始递增
    existing_node_ids = [str(node) for node in G.nodes()]  # 确保使用字符串类型的ID
    new_stations = [str(int(max(existing_node_ids, key=int)) + i + 1) for i in range(num_new_stations)]

    new_positions = {
        station: (random.uniform(min(pos_dict.values(), key=lambda x: x[0])[0],
                                 max(pos_dict.values(), key=lambda x: x[0])[0]),
                  random.uniform(min(pos_dict.values(), key=lambda x: x[1])[1],
                                 max(pos_dict.values(), key=lambda x: x[1])[1]))
        for station in new_stations
    }

    # 添加新的站点
    G.add_nodes_from(new_stations)
    pos_dict.update(new_positions)  # 确保新的站点坐标被加入 pos_dict

    # 随机连接新站点到现有站点
    for new_station in new_stations:
        existing_station = random.choice(list(G.nodes()))
        if existing_station != new_station:
            G.add_edge(new_station, existing_station, weight=random.randint(1, 10))  # 随机加权边

    return G, pos_dict


# 在现有网络上添加一些新的站点和线路
G, pos_dict = add_random_station_and_connection(G, pos_dict, num_new_stations=5)

def service_coverage(G, population_points, radius=1000):
    """计算有效服务覆盖率（单位：米）"""
    kdtree = KDTree([pos_dict[node] for node in G.nodes()])
    count = 0
    for point in population_points:
        distance, _ = kdtree.query([point], k=1)
        if distance <= radius:
            count += 1
    return count / len(population_points)


# 覆盖率
coverage_100m = service_coverage(G, sample_population, 100)
coverage_200m = service_coverage(G, sample_population, 200)
coverage_500m = service_coverage(G, sample_population, 500)
coverage_1km = service_coverage(G, sample_population, 1000)

print(f"""
空间可达性:
   100米覆盖率: {coverage_100m * 100:.1f}%
   200米覆盖率: {coverage_200m * 100:.1f}%
   500米覆盖率: {coverage_500m * 100:.1f}%
  1000米覆盖率: {coverage_1km * 100:.1f}%
""")


import matplotlib.pyplot as plt
import numpy as np
from pyproj import Proj
from sklearn.neighbors import KDTree

def convert_to_utm(df, lon_col='X', lat_col='Y'):
    """将经纬度转换为UTM坐标系"""
    p = Proj(proj='utm', zone=18, ellps='WGS84')
    x, y = p(df[lon_col].values, df[lat_col].values)
    return x, y

def generate_population_points(coords, num=1000):
    """在整个网络覆盖范围内生成均匀分布的人口点"""
    x_min, y_min = np.min(coords, axis=0)
    x_max, y_max = np.max(coords, axis=0)
    return np.column_stack([np.random.uniform(x_min, x_max, num), np.random.uniform(y_min, y_max, num)])

def plot_service_area(coords, population_points, bus_stops, radius, filename):
    """绘制服务覆盖区域"""
    plt.figure(figsize=(10, 8))

    # 随机生成一些居民点
    plt.scatter(population_points[:, 0], population_points[:, 1], c='blue', s=10, label='Population Points', alpha=0.6)

    # 选取一些局部公交站点
    sampled_stops = bus_stops[::10]  # 每10个选一个站点，防止数据过于密集
    plt.scatter(sampled_stops[:, 0], sampled_stops[:, 1], c='red', s=50, label='Bus Stops', marker='^')

    # 绘制圆形覆盖半径
    for stop in sampled_stops:
        circle = plt.Circle((stop[0], stop[1]), radius, color='green', fill=False, linestyle='--')
        plt.gca().add_artist(circle)

    # 设置图表标题和标签
    plt.title(f'Service Area Coverage (Radius = {radius} meters)', fontsize=16)
    plt.xlabel('X (UTM)')
    plt.ylabel('Y (UTM)')
    plt.legend()

    # 保存图片
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

coords = np.random.rand(100, 2) * 1000  # 随机生成100个坐标点作为公交站点坐标
population_points = generate_population_points(coords, num=1000)  # 生成1000个居民点
bus_stops = coords  # 假设公交站点的坐标就是之前生成的坐标

# 输出不同半径下的覆盖区域图像
radii = [100, 200, 500, 1000]
for radius in radii:
    filename = f'coverage_radius_{radius}.png'
    plot_service_area(coords, population_points, bus_stops, radius, filename)
    print(f'Image saved as {filename}')
