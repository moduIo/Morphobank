####
# Features are read from file and learning algorithms are applied to the data.
# ---
# COMMAND LINE ARGUMENTS:
# sys.argv[1] := a CSV list of paths to Morphobank feature files
# sys.argv[2] := k, the number of clusters
#
# Example Usage: 
# python3 morphobank_clustering.py 'features.txt' '10'
####
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans

###
# Main
###
# Load data
data = np.loadtxt(open(sys.argv[1]), delimiter=',', usecols=(1, 2, 3))

# Store into numpy array
X = np.array(data)

# Run learning algorithms
kmeans = KMeans(n_clusters=int(sys.argv[2]), random_state=7)
clusters = kmeans.fit_predict(X)
centroids = kmeans.cluster_centers_

# Generate plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2],
            marker='x', s=169, linewidths=2,
            color='w', zorder=10)
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c = clusters)
ax.set_xlabel('Jaccard Label Similarity')
ax.set_ylabel('Jaccard State Similarity')
ax.set_zlabel('TF-IDF Cosine Similarity')

plt.show()