####
# Features are read from file and learning algorithms are applied to the data.
#
# ---
# COMMAND LINE ARGUMENTS:
# sys.argv[1] := a CSV list of paths to Morphobank feature files
#
# Example Usage: 
# python3 morphobank_learner.py 'features.txt'
####
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans

###
# Main
###
# Load data
data = np.loadtxt(open(sys.argv[1]), delimiter=',')

# Store into numpy array
X = np.array(data)

# Run learning algorithms
k_means = KMeans(n_clusters = 2).fit_predict(X)

# Generate plot
plt.xlabel('Jaccard Label Similarity')
plt.ylabel('Jaccard State Similarity')
plt.scatter(X[:, 0], X[:, 1], c = k_means)

plt.show()