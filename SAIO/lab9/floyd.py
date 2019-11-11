import numpy as np


class Floyd:
    def __init__(self, D):
        self.D = D
        self.length = len(self.D)
        self.R = [list(range(1, self.length + 1))] * self.length

    def solve(self):
        for i in range(len(self.D)):
            indexes = self.get_working_matrix(i)
            d = self.get_d(indexes, i)

    def get_d(self, matrix, k):
        d = {}
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if i == j:
                    continue

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
    floyd.solve()

