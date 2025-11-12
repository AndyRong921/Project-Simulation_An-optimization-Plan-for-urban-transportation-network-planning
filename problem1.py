import pandas as pd
import ast
import folium

# Load and filter the dataset
df1 = pd.read_csv("MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv")
filtered_df = df1[df1['Functional Class Code'].isin([1, 2])]

# Specify columns to keep
columns_to_keep = ['AADT 2014', 'AADT 2015', 'AADT 2016', 'AADT 2017', 'AADT 2018',
                   'AADT (Current)', 'node start', 'node(s) end']
filtered_df = filtered_df.dropna(subset=['node start', 'node(s) end'], how='all')[columns_to_keep]

# Convert 'node start' and 'node(s) end' columns to lists
def convert_to_list(cell):
    try:
        # Use ast.literal_eval to safely evaluate the string
        if pd.notna(cell) and isinstance(cell, str):
            return list(ast.literal_eval(cell))
    except (ValueError, SyntaxError):
        # Handle strings that cannot be parsed
        pass
    return []

filtered_df['node start'] = filtered_df['node start'].apply(convert_to_list)
filtered_df['node(s) end'] = filtered_df['node(s) end'].apply(convert_to_list)
filtered_df['nodes'] = filtered_df['node start'] + filtered_df['node(s) end']
filtered_df = filtered_df[filtered_df['nodes'].apply(len) > 0]

# Load node coordinates
nodes_all_df = pd.read_csv('nodes_all.csv', header=None, usecols=[0, 1, 2],
                         names=['osmid', 'y', 'x'], skiprows=1)
new_nodes_data = {'osmid': [7487021968, 9768381905, 8270449366, 8270462846],
                  'y': [39.3856799, 39.4187001, 39.3796506, 39.3793737],
                  'x': [-76.5246908, -76.6693374, -76.4719395, -76.4600492]}
new_nodes_df = pd.DataFrame(new_nodes_data)
nodes_all_df = pd.concat([nodes_all_df, new_nodes_df], ignore_index=True)

# Extract node coordinates
all_node_ids = {int(node_id) for node_list in filtered_df['nodes'] for node_id in node_list}
node_coords_list = []

for node_id in all_node_ids:
    node_info = nodes_all_df[nodes_all_df['osmid'].astype(int) == node_id]
    if not node_info.empty:
        lat, lon = node_info['y'].values[0], node_info['x'].values[0]
        node_coords_list.append({'node_id': node_id, 'latitude': lat, 'longitude': lon})

# Create and save map
if node_coords_list:
    initial_lat, initial_lon = node_coords_list[0]['latitude'], node_coords_list[0]['longitude']
    m = folium.Map(location=[initial_lat, initial_lon], zoom_start=12)
    
    for node in node_coords_list:
        folium.Marker(location=[node['latitude'], node['longitude']],
                      popup=f"Node ID: {node['node_id']}",
                      icon=folium.Icon(color='blue')).add_to(m)
                      
    m.save("nodes_map.html")
    print("Map has been saved to nodes_map.html")
else:
    print("No valid nodes to plot.")
