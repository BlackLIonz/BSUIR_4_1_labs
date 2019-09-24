import numpy as np


class ResourceAllocation:
    def __init__(self, f_table):
        self.f_table = f_table
        self.n, self.c = self.f_table.shape
        self.c = self.c - 1
        self.B = [[] for i in range(self.n)]
        self.B[0] = list(self.f_table[0, :])

    def _get_B_k(self, k, y):
        b = [self.f_table[k, z] + self.B[k - 1][y - z] for z in range(y + 1)]
        return max(b)

    def solve(self):
        for k in range(1, self.n):
            self.B[k].append(0)
            for y in range(1, self.c + 1):
                self.B[k].append(self._get_B_k(k, y))
        return self.B


if __name__ == '__main__':
    table = np.array([[0, 3, 4, 5, 8, 9, 10],
                      [0, 2, 3, 7, 9, 12, 13],
                      [0, 1, 2, 6, 11, 11, 13]])
    task = ResourceAllocation(table)
    task.solve()
