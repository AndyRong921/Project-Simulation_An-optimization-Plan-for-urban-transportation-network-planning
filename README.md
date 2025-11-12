Baltimore Transportation Network Evaluation and Optimization Project

🚀 Project Introduction

This project aims to conduct a comprehensive evaluation and analysis of the transportation infrastructure in Baltimore, USA.

Based on Graph Theory and Network Models, we performed a thorough assessment of Baltimore's transportation system. We specifically analyzed the impact of the Francis Scott Key Bridge collapse and proposed a comprehensive improvement strategy that includes both bridge reconstruction and bus network optimization.

This repository contains our complete analysis methodology, core mathematical models, and key implementation code for this task.

💡 Project Execution Strategy and Analysis

Our overall solution follows a four-stage process: "Data First - Assess Current State - Specific Analysis - Comprehensive Optimization".

1. Phase 1: Data Preprocessing and Key Node Identification

Faced with a massive amount of raw data, we first performed data cleaning and preprocessing.

Metric Establishment: To filter the core hubs of Baltimore's transportation network from over 50,000 nodes, we proposed two key evaluation metrics:

Node Degree: Represents the node's connectivity.

Average Neighbor's Distance: Represents the node's transit efficiency.

Node Filtering: Using our defined comprehensive weighting formula, we successfully identified the top 20 most critical transportation hubs (Top 20 Important Nodes), laying the foundation for subsequent macro-level network modeling.

2. Phase 2: Bridge Collapse Impact Analysis

We constructed a Road Traffic Flow Model to quantify the impact of the bridge collapse.

Model Abstraction: We used the K-means algorithm to cluster the selected key nodes into three groups, abstracting them into three key routes: Highway, Tunnel, and Bridge.

Impact Assessment: We defined the Congestion Level ($Y_{ij} = d_{ij} / SM_{ij}$, i.e., actual flow / max capacity) as the core metric.

Model Solution: By comparing data before and after the bridge collapse, we found:

The bridge's own traffic flow (546 units) dropped to 0.

This traffic was forced to divert, causing Highway traffic to increase by 205.23 (units) and Tunnel traffic to increase by 666 (units).

The tunnel's congestion level $\delta_{ij}$ soared by 19.05%, and the highway's also rose by 4.19%, confirming the massive negative impact of the collapse on commuter efficiency.

3. Phase 3: Bus System Special Assessment

We established a Bus Traffic System Evaluation Model, focusing on two dimensions: Accessibility and Coverage.

Accessibility Analysis: We used the Dijkstra algorithm to calculate the "shortest path" between any two points in the bus network (converting distance to time based on average bus speed). The results showed that most stops have good accessibility within a 40-minute timeframe.

Coverage Analysis: We evaluated the coverage efficiency of bus stops by setting different service radii (Radius) and defined a Reachability metric $\omega$ (Reachability $\omega = f/r$, i.e., coverage / radius).

Key Finding: When the coverage radius $r = 150m$, the $\omega$ metric peaked, and the bus network coverage reached 28.0%. This provided crucial data for our subsequent station layout optimization.

4. Phase 4: Comprehensive Optimization Strategy

Based on the analysis from the previous models, we proposed a combined optimization strategy: "Key Bridge Reconstruction + Bus Network System Optimization".

Bus Optimization Algorithm: We didn't just add more stops; we performed precise optimization using algorithms:

Prioritized connecting low-degree nodes to improve network connectivity.

Controlled walking connections by setting a walking distance threshold (0.0045).

Limited cross-connections between bus lines (max 1) to avoid system over-complexity.

Performance Evaluation: After optimization, our bus network showed significant improvements in three key graph theory metrics:

Network Density: Increased by 11.11%

Average Degree: Increased by 4.0%

Clustering Coefficient: Increased by 9.37%

This proves that our optimization strategy can effectively enhance the robustness and efficiency of Baltimore's bus network.

💻 Code Implementation

The code in this repository is mainly used for data processing, K-means clustering, Dijkstra's shortest path algorithm, and bus network optimization simulation as described in the models above.

Runtime Environment

Python 3.x

MATLAB (for some model calculations)

[Main dependencies, e.g., pandas, numpy, scikit-learn, networkx, matplotlib]

# Install main dependencies
pip install -r requirements.txt


Code Structure

.
├── /paper/                 # Contains related analysis documents or reports
├── /code/                  # Contains all implementation code
│   ├── task1_preprocessing.py  # Phase 1: Data preprocessing and node filtering
│   ├── task2_bridge_impact.py  # Phase 2: K-means and bridge impact analysis
│   ├── task3_bus_evaluation.py # Phase 3: Dijkstra and bus accessibility
│   └── task4_optimization.py   # Phase 4: Bus network optimization algorithm
├── /data/                  # Contains (anonymized) raw or processed data
├── README.md               # The repository documentation
└── requirements.txt        # Python dependency packages


(Please note: The code file structure above is an example; please modify it according to your actual files)

👥 Project Contributors

a: [Role, e.g., Model construction, Algorithm implementation]

b: [Role, e.g., Data analysis, Report writing]

c: [Role, e.g., Data preprocessing, Code validation]

📜 Disclaimer

The results of this project are intended for academic exchange and technical sharing purposes only.

The solution may have limitations, and the models and code are provided for reference only. We welcome discussion and corrections.

If you find this project helpful, please give it a ⭐️ Star!
