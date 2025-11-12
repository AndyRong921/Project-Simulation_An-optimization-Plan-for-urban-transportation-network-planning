# 🗺️ Regulating the Traffic of Future: An Applicable Evaluation and Optimization Model for Baltimore 🚗

This project presents a comprehensive evaluation and optimization model for the transportation system in Baltimore, USA. Leveraging graph theory, this study establishes a network model and proposes a specific model for the bus network to address challenges posed by the city's transportation infrastructure, particularly following the collapse of the Francis Scott Key Bridge.

<img width="4144" height="2761" alt="image" src="https://github.com/user-attachments/assets/d936cf9e-cd24-4b1e-9963-a808140f971d" />





## 🛠️ Project Methodology

The project's workflow is divided into four core tasks:

### 1️⃣ Task 1: Data Preprocessing & Key Node Identification

* **Objective:** 🎯 To filter and identify the most critical nodes within the transportation network from raw data to prepare for modeling.
* **Method:**
    1.  **Data Cleaning:** 🧹 Processed and cleaned an initial dataset of over 220,000 traffic nodes.
    2.  **Metric Establishment:** 📏 Developed two key evaluation metrics:
        * **Node Degree:** Represents the connectivity of a node.
        * **Average Neighbor's Distance:** Represents the operational efficiency of a node.
    3.  **Node Filtering:** 🔎 Applied a comprehensive formula to identify and select the 20 most important traffic nodes.
<img width="1000" height="801" alt="image" src="https://github.com/user-attachments/assets/e9175f95-65e6-4dd5-8f95-59b96e1597e5" />
<img width="1268" height="690" alt="image" src="https://github.com/user-attachments/assets/784f83e3-08b1-4d26-939d-306968f54438" />


# 🗺️ Regulating the Traffic of Future: An Applicable Evaluation and Optimization Model for Baltimore 🚗

This project presents a comprehensive evaluation and optimization model for the transportation system in Baltimore, USA. Leveraging graph theory, this study establishes a network model and proposes a specific model for the bus network to address challenges posed by the city's transportation infrastructure, particularly following the collapse of the Francis Scott Key Bridge.

## 🛠️ Project Methodology

The project's workflow is divided into four core tasks:

### 1️⃣ Task 1: Data Preprocessing & Key Node Identification

* **Objective:** 🎯 To filter and identify the most critical nodes within the transportation network from raw data to prepare for modeling.
* **Method:**
    1.  **Data Cleaning:** 🧹 Processed and cleaned an initial dataset of over 220,000 traffic nodes.
    2.  **Metric Establishment:** 📏 Developed two key evaluation metrics:
        * **Node Degree:** Represents the connectivity of a node.
        * **Average Neighbor's Distance:** Represents the operational efficiency of a node.
    3.  **Node Filtering:** 🔎 Applied a comprehensive formula to identify and select the 20 most important traffic nodes.

### 2️⃣ Task 2: Road Network Modeling (Bridge Collapse Impact)

* **Objective:** 💥 To assess the impact of the Key Bridge collapse on Baltimore's road traffic network.
* **Method:**
    1.  **Path Abstraction:** 🛣️ Used the K-means algorithm to cluster qualifying nodes into three groups, abstracting them into three key routes: Highway, Tunnel, and Bridge.
<table>
  <tr>
    <td align="center"><em>Fig 5: Surrounding Tunnels/Bridges</em></td>
    <td align="center"><em>Fig 6: K-Means Cluster Analysis</em></td>
  </tr>
  <tr>
    <td><img width="400" alt="The condition of a bridge or tunnel around a collapsed bridge" src="https://github.com/user-attachments/assets/9522d157-7f25-42c2-83e2-5d0b40b2c0d9" /></td>
    <td><img width="400" alt="Cluster analysis of three types of nodes" src="https://github.com/user-attachments/assets/b921019f-3529-4395-8afa-6234368b7ae5" /></td>
  </tr>
</table>

    2.  **Network Modeling:** 📉 Built a foundational network model to evaluate annual average traffic flow and congestion levels.
<table>
  <tr>
    <td align="center"><em>Fig 4: All Nodes After Cleaning</em></td>
    <td align="center"><em>Fig 7: Route Diagram for Modeling</em></td>
  </tr>
  <tr>
    <td><img width="400" alt="Figure of all nodes after cleaning" src="https://github.com/user-attachments/assets/afc27de2-a2ee-4c0a-bd10-2d4ba80a5767" /></td>
    <td><img width="400" alt="A line diagram with modeling implications related to the effects of bridge collapse" src="https://github.com/user-attachments/assets/5091b9a7-e3c8-44ff-9ba2-9f99998a66aa" /></td>
  </tr>
</table>

    3.  **Impact Analysis:** 📊 Compared traffic flow and congestion data before and after the bridge collapse. The results showed that the collapse reduced the bridge's traffic to zero, while traffic on the highway and tunnel routes increased significantly, with a corresponding rise in congestion.
    
<img width="374" alt="Table snippet showing traffic increase" src="https://github.com/user-attachments/assets/dc0a3af0-bc4c-4fd1-94ce-061a1e37c26e" />

### 3️⃣ Task 3: Bus System Evaluation Model

* **Objective:** 🚌 To evaluate the performance of Baltimore's public bus network.
* **Method:**
    1.  **Model Dimensions:** 📐 Established an evaluation model based on two key dimensions: **Accessibility** and **Coverage**.
    2.  **Data Visualization:** 🗺️ Processed and visualized the bus network data.
    3.  **Accessibility Analysis:** 🚶‍♂️ Used Dijkstra's algorithm to analyze network reachability.
    4.  **Findings:** 💡 The study found that network accessibility peaked when the bus stop coverage radius was 150 meters, achieving a 28.0% coverage rate at this radius.


### 4️⃣ Task 4: Transport Network Optimization Strategy

* **Objective:** 🚀 To propose a comprehensive transportation improvement plan based on the preceding analyses.
* **Method:**
    1.  **Strategy:** ✨ Adopted a combined "Key Bridge Reconstruction + Bus Network System Optimization" strategy.
    2.  **Optimization Actions:** 🚉 Optimized the bus network by adding new bus stops at key nodes, such as airports and train stations.
    3.  **Effectiveness Evaluation:** ✅ The optimization resulted in improvements across three key network metrics:
        * **Network Density** increased by 11.11%
        * **Average Degree** increased by 4.0%
        * **Clustering Coefficient** increased by 9.37%
<img width="1000" height="594" alt="image" src="https://github.com/user-attachments/assets/14a10e03-5251-4153-8a9f-5558ea8f85f1" />
<img width="386" height="87" alt="image" src="https://github.com/user-attachments/assets/12072cb1-a756-41e7-92a9-cd025201b4ba" />
---

## 📈 Key Models & Formulas

### Road Network (Task 2)

* **Congestion Level ($Y_{ij}$):** Measures the ratio of actual traffic flow ($d_{ij}$) to the maximum capacity ($SM_{ij}$).
    $$
    Y_{ij} = \frac{d_{ij}}{SM_{ij}}
    $$
* **Collapse Impact Index ($\delta$):** Quantifies the change in minimum congestion ($MIN_1$ before, $MIN_2$ after) to evaluate the severity of the bridge collapse.
    $$
    \delta = \frac{|MIN_1 - MIN_2|}{MIN_1}
    $$

### Bus System (Task 3)

* **Bus Stop Coverage ($f$):** Calculates the total circular coverage area ($n \cdot \pi r^2$) as a fraction of the total shortest path area ($M_{min}$).
    $$
    f = \frac{n \cdot \pi r^2}{M_{min}} = \frac{n \cdot \pi r^2}{2a \cdot \min \sum L_{ij}}
    $$
* **Coverage-Radius Ratio ($\omega$):** An efficiency metric to evaluate the reasonableness of bus stop placement (coverage per unit of radius).
    $$
    \omega = \frac{f}{r}
    $$

### Network Optimization (Task 4)

* **Network Density ($D$):** Measures the ratio of existing edges ($E$) to the total possible edges in a network of $N$ nodes.
    $$
    D = \frac{E}{N(N-1)/2}
    $$
* **Average Degree ($AD$):** The average number of connections (degree $D_i$) per node in the network.
    $$
    AD = \frac{1}{N} \sum_{i=1}^{N} D_i
    $$
* **Clustering Coefficient ($C(i)$):** Measures how connected a node's neighbors ($e_i$) are to each other.
    $$
    C(i) = \frac{2e_i}{D_i(D_i - 1)}
    $$

---

## 👥 Contributors

* **A (Author):** Primarily responsible for modeling; assisted with programming (Matlab, R).
    * *Undergraduate in Mathematics and Applied Mathematics.*
* **B:** Primarily responsible for programming (Python, HTML).
    * *Undergraduate in Software Engineering.*
* **C:** Primarily responsible for the paper (LaTeX).
    * *Undergraduate in Information and Computing Science.*

## 📜 Usage Statement

This document provides an overview of the research content from this project. All models, data, and conclusions are derived from the original study. This document is intended for academic exchange and project demonstration purposes only. For citation, please refer to the original research report.
