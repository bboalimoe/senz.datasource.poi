__author__ = 'wzf'

def filterClustersBySize(cluster, dataArray, size):
    allCluster = [[] for row in range(cluster.max())]

    i = 0
    while i < len(cluster):
        index = cluster[i] - 1
        allCluster[index].append(dataArray[i])  # put points to its cluster
        i += 1

    validCluster = []
    for cluster in allCluster:
        if (len(cluster) >= size):
            validCluster.append(cluster)   # filter cluster

    return validCluster