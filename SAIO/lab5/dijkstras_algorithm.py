import numpy as np


def dijkstra(N, S, matrix):
    valid = [True] * N
    weight = [np.inf] * N
    weight[S] = 0
    for i in range(N):
        min_weight = np.inf
        ID_min_weight = -1
        for i in range(len(weight)):
            if valid[i] and weight[i] < min_weight:
                min_weight = weight[i]
                ID_min_weight = i
        for i in range(N):
            if weight[ID_min_weight] + matrix[ID_min_weight][i] < weight[i]:
                weight[i] = weight[ID_min_weight] + matrix[ID_min_weight][i]
        valid[ID_min_weight] = False
    return weight
