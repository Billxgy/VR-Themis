import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import time 

start_time = time.time()


file_path = 'Data/statisticalFeaturesUnity.txt'
Clusters_path = "CoarseProcessStage/Clustering/clusters.json"
data = []
app_names = []

with open(Clusters_path, 'w') as file:
    pass

with open(file_path, 'r') as file:
    lines = file.readlines()[1:]  
    for line in lines:
        parts = line.strip().split()
        app_name = parts[0]
        app_names.append(app_name)
        features = list(map(float, parts[1:]))

        if len(features) != 13:
            print(f"[Wrong] App '{app_name}' does not have exact 13 features, it has {len(features)} features.")
        else:
            data.append(features)

data = np.array(data)

data_scaled = StandardScaler().fit_transform(data)


minPts = 3  
k = minPts - 1  

def select_k_distance(data, k):
    k_distances = []
    for i in range(data.shape[0]):
        dist = np.linalg.norm(data[i] - data, axis=1)
        dist.sort()
        k_distances.append(dist[k])
    return np.array(k_distances)

k_distances = select_k_distance(data_scaled, k)
k_distances.sort()

# plt.figure(figsize=(10, 5))
# plt.plot(np.arange(len(k_distances)), k_distances[::-1], marker='o')
# plt.title("K-Distance Graph")
# plt.xlabel("Points sorted by distance")
# plt.ylabel("Distance")
# plt.grid()
# plt.show()

eps = 0.1  

# DBSCAN 
dbscan_model = DBSCAN(eps=eps, min_samples=minPts)
labels = dbscan_model.fit_predict(data_scaled)

print("Cluster labels:", labels)

clusters_dict = {}

unique_labels = np.unique(labels)
for label in unique_labels:
    if label != -1:  
        cluster_name = f"Cluster {label}"
        print(cluster_name)
        clusters_dict[cluster_name] = []
        for i in range(len(labels)):
            if labels[i] == label:
                print(f" - {app_names[i]}")
                clusters_dict[cluster_name].append(app_names[i])

with open(Clusters_path, 'w') as json_file:
    json.dump(clusters_dict, json_file, indent=4)

if len(set(labels)) > 1:
    silhouette_avg = silhouette_score(data_scaled, labels)
    print(f"Silhouette Coefficient: {silhouette_avg}")
else:
    print("clustering result contains only one cluster or noise point, the index cannot be calculated.")

end_time = time.time()
execution_time = end_time - start_time
print(f"Run time: {execution_time:.4f} senconds")