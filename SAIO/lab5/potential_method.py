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
        self.deltas = {}
        self.node_zero = None

    def get_u(self):
        visited = [1]
        for edge, values in self.U_basis.items():
            for j in values:
                if self.u.get(edge) is not None:
                    self.u[j] = self.u[edge] - self.c[(edge, j)]
                elif self.u.get(j) is not None:
                    self.u[edge] = self.c[(edge, j)] + self.u[j]
        self.u = dict(SortedDict(self.u))
        return self.u

    def get_deltas(self):
        for edge, values in self.U_non_basis.items():
            for j in values:
                self.deltas[(edge, j)] = self.u[edge] - self.u[j] - self.c[(edge, j)]

    def get_invalid_delta(self):
        for index, delta in self.deltas.items():
            if delta > 0:
                if index[1] in self.U_non_basis[index[0]]:
                    self.node_zero = index
                    return self.node_zero

    def find_cycle(self):
        self.U_plus = [self.node_zero]
        self.U_minus = []
        key, value = self.node_zero
        graph = self.U_basis
        graph[key].append(value)
        return [[node] + path for node in graph for path in self.dfs(graph)][:[]]

    def dfs(self, graph, end=2):
        start = self.node_zero[0]
        fringe = [(start, [])]
        while fringe:
            state, path = fringe.pop()
            if path and state == end:
                yield path
                continue
            for next_state in graph[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path + [next_state]))


    def get_non_basis_edges(self):
        self.U_non_basis = {}
        for key, values in self.S.items():
            for value in values:
                if value in self.U_basis[key]:
                    continue
                if not self.U_non_basis.get(key):
                    self.U_non_basis[key] = []
                self.U_non_basis[key].append(value)
        return self.U_non_basis

    def solve(self):
        self.get_u()
        self.get_deltas()
        if not self.get_invalid_delta():
            raise NotImplemented
        a = self.find_cycle()
        print(a)


if __name__ == '__main__':
    S = {
        1: [2],
        2: [6],
        3: [2, 4],
        4: [],
        5: [3, 4],
        6: [1, 3, 5]
    }
    U_b = {
        1: [2],
        2: [],
        3: [2, 4],
        4: [],
        5: [4],
        6: [3]
    }
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
