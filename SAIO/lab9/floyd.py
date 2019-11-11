import copy

import numpy as np


class Floyd:
    def __init__(self, matrix):
        self.matrix = matrix
        self.length = len(self.matrix)
        self.R = np.array([list(range(self.length))] * self.length)
        self.D = np.array([])

    def solve(self, start, end):
        start -= 1
        end -= 1
        if len(self.D) == 0:
            self.D = copy.deepcopy(self.matrix)
            self.calculate_paths()
        path = [start]
        now = start
        while now != end:
            now = self.R[now, end]
            path.append(now)
        print(' -> '.join(map(lambda x: str(x + 1), path)))

    def calculate_paths(self):
        for i in range(len(self.D)):
            indexes = self.get_working_matrix(i)
            self.get_d(indexes, i)

    def get_d(self, matrix, j):
        for i in matrix:
            for k in matrix:
                if i == j or k == j or i == k:
                    continue
                d = self.D[i, j] + self.D[j, k]
                if self.D[i, k] > d:
                    self.D[i, k] = d
                    self.R[i, k] = j

    def get_working_matrix(self, i):
        indexes = []
        for j in range(self.length):
            if self.D[i, j] != np.inf:
                indexes.append(j)
        return indexes


if __name__ == '__main__':
    D = np.array([[0, 9, np.inf, 3, np.inf, np.inf, np.inf, np.inf],
                  [9, 0, 2, np.inf, 7, np.inf, np.inf, np.inf],
                  [np.inf, 2, 0, 2, 4, 8, 6, np.inf],
                  [3, np.inf, 2, 0, np.inf, np.inf, 5, np.inf],
                  [np.inf, 7, 4, np.inf, 0, 10, np.inf, np.inf],
                  [np.inf, np.inf, 8, np.inf, 10, 0, 7, np.inf],
                  [np.inf, np.inf, 6, 5, np.inf, 7, 0, np.inf],
                  [np.inf, np.inf, np.inf, np.inf, 9, 12, 10, 0]])
    floyd = Floyd(D)
    floyd.solve(1, 5)
