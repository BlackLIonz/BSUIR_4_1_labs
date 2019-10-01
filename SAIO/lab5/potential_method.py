import numpy as np
from sortedcontainers import SortedDict


class PotentialMethod:
    def __init__(self, S, U_b, weights):
        self.S = S
        self.U_basis = U_b
        self.U_non_basis = self.get_non_basis_edges()
        self.c = weights
        self.n = len(S)
        self.u = {1: 0}
        self.delta = {}

    def get_u(self):
        visited = [1]
        for i, j in self.U_basis:
            if self.u.get(i) is not None:
                self.u[j] = self.u[i] - self.c[(i, j)]
            elif self.u.get(j) is not None:
                self.u[i] = self.c[(i, j)] + self.u[j]
        self.u = dict(SortedDict(self.u))
        return self.u

    def get_deltas(self):
        for i, j in self.U_non_basis:
            self.delta[(i, j)] = self.u[i] - self.u[j] - self.c[(i, j)]

    def get_non_basis_edges(self):
        self.U_non_basis = []
        for key, value in self.S.items():
            for node in value:
                if (key, node) not in self.U_basis:
                    self.U_non_basis.append((key, node))
        return self.U_non_basis

    def solve(self):
        self.get_u()
        self.get_deltas()
        print(self.delta)


if __name__ == '__main__':
    S = {1: [2],
         2: [6],
         3: [2, 4],
         4: [],
         5: [3, 4],
         6: [1, 3, 5]
         }
    U_b = [(1, 2), (3, 2), (6, 3), (3, 4), (5, 4)]
    weights = {
        (1, 2): 1,
        (2, 6): 3,
        (3, 2): 3,
        (3, 4): 5,
        (5, 3): -4,
        (5, 4): 1,
        (6, 1): -2,
        (6, 3): 3,
        (6, 5): 4,
    }
    pm = PotentialMethod(S, U_b, weights)
    pm.solve()
