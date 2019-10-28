import numpy as np


class DijkstraAlgorithm:
    def __init__(self, matrix, weights, s, t):
        self.matrix = matrix
        self.weights = weights
        self.s = s
        self.t = t
        self.f = {}
        self.B = dict(zip(range(1, len(matrix) + 1), [np.inf] * len(matrix)))

        self.B[s] = 0
        self.f[s] = 0

    def solve(self):
        visited = list(range(1, len(self.matrix) + 1))
        pointer = self.s
        while len(visited):
            neighbors = self.matrix[pointer]
            for neighbor in neighbors:
                if self.B[neighbor] > (self.B[pointer] + self.weights[(pointer, neighbor)]):
                    self.B[neighbor] = self.B[pointer] + self.weights[(pointer, neighbor)]
                    self.f[neighbor] = pointer
            visited.remove(pointer)
            pointer = min(self.B.items(), key=lambda x: x[1] if x[0] in visited else np.inf)[0]
        return self.f


if __name__ == '__main__':
    matrix = {
        1: [2, 6],
        2: [3],
        3: [4, 5],
        4: [],
        5: [7],
        6: [2, 5, 7],
        7: [2, 3],
    }
    weights = {
        (1, 2): 12,
        (1, 6): 1,
        (2, 3): 2,
        (3, 4): 1,
        (3, 5): 5,
        (5, 7): 2,
        (6, 2): 10,
        (6, 5): 5,
        (6, 7): 8,
        (7, 2): 2,
        (7, 3): 6,
    }
    dijkstra = DijkstraAlgorithm(matrix, weights, 1, 4)
    path = dijkstra.solve()
    pointer = 4
    res = []
    while len(res) != len(path):
        res.append(pointer)
        if pointer != 1:
            pointer = path[pointer]
    print(' -> '.join(str(x) for x in reversed(res)))
