import numpy as np


class MaximalPath:
    def __init__(self, matrix, weights, s, t):
        self.matrix = matrix
        self.weights = weights
        self.s = s
        self.t = t
        self.f = {}
        self.B = dict(zip(range(1, len(matrix) + 1), [np.inf] * len(matrix)))
        self.I = []

        self.B[s] = 0
        self.f[s] = 0

    def w(self, I):
        non_visited_neighbors = []
        for i in I:
            for j in self.matrix[i]:
                if j not in self.I:
                    non_visited_neighbors.append(j)
        return non_visited_neighbors

    def I_minus(self, I):
        neighbors = []
        for i in I:
            pass

        return neighbors

    def solve(self):
        self.I.append(self.s)
        self.B[self.s] = 0
        self.f[self.s] = 0
        while True:
            w_I = self.w(self.I)



if __name__ == '__main__':
    matrix = {
        1: [2, 6],
        2: [3, 5],
        3: [4],
        4: [],
        5: [3, 4],
        6: [2, 3, 5],
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
    dijkstra = MaximalPath(matrix, weights, 1, 4)
    path = dijkstra.solve()
    pointer = 4
    res = []
    while len(res) != len(path):
        res.append(pointer)
        if pointer != 1:
            pointer = path[pointer]
    print(' -> '.join(str(x) for x in reversed(res)))
