import copy

import numpy as np
from sortedcontainers import SortedDict


class PotentialMethod:
    def __init__(self, S, U_b, weights, x):
        self.S = S
        self.U_basis = U_b
        self.U_non_basis = self.get_non_basis_edges()
        self.c = weights
        self.x = x
        self.n = len(S)
        self.u = None
        self.deltas = {}
        self.ij_zero = None
        self.U_plus = None
        self.U_minus = None
        self.teta = None
        self.ij_astr = None
        self.sigma = None

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

    def get_u(self):
        u = {1: 0}
        while len(u) != 6:
            for node, values in self.U_basis.items():
                for j in values:
                    if u.get(node) is not None and u.get(j) is None:
                        u[j] = u[node] - self.c[(node, j)]
                    elif u.get(j) is not None and u.get(node) is None:
                        u[node] = self.c[(node, j)] + u[j]
        self.u = dict(SortedDict(u))
        return self.u

    def get_deltas(self):
        for edge, values in self.U_non_basis.items():
            for j in values:
                self.deltas[(edge, j)] = self.u[edge] - self.u[j] - self.c[(edge, j)]

    def get_invalid_delta(self):
        for index, delta in self.deltas.items():
            if delta > 0:
                if index[1] in self.U_non_basis[index[0]]:
                    self.ij_zero = index
                    return self.ij_zero

    def find_cycle(self):
        paths = self.create_paths()
        positive_edge = self.ij_zero
        positive_paths = []
        negative_paths = []
        for path in paths:
            if all([node in path for node in positive_edge]):
                positive_paths.append(path)
            else:
                negative_paths.append(path)
        for positive_path in positive_paths:
            for negative_path in negative_paths:
                for i in range(1, len(max([positive_path, negative_path], key=len))):
                    if positive_path[i] == negative_path[i]:
                        self.U_plus = self.get_edges(positive_path[:i + 1])
                        self.U_minus = self.get_edges(negative_path[:i + 1])
                        return self.U_plus, self.U_minus

    def create_paths(self):
        key, value = self.ij_zero
        graph = copy.deepcopy(self.U_basis)
        graph[key].append(value)

        path = [[key]]
        while True:
            new_path = []
            skip = 0
            for node in path:
                node_copy = copy.deepcopy(node)
                if len(graph[node[-1]]) == 0:
                    new_path.append(node_copy)
                    skip += 1
                    continue
                for next_node in graph[node[-1]]:
                    new_path.append(node_copy + [next_node])
            if skip == len(new_path):
                return new_path
            path = new_path

    def get_edges(self, path):
        edges = []
        for i in range(1, len(path)):
            edges.append((path[i - 1], path[i]))
        return edges

    def dfs(self, graph, end=2):
        start = self.ij_zero[0]
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

    def calculate_teta(self):
        self.teta = min([self.x[edge] for edge in self.U_minus])

    def get_sigma(self):
        min_x = (None, np.inf)
        for edge in self.U_minus:
            weight = self.x[edge]
            if weight < min_x[1]:
                min_x = (edge, weight)
        self.ij_astr, self.sigma = min_x

    def create_new_x(self):
        for edge in self.U_minus:
            self.x[edge] -= self.sigma
        for edge in self.U_plus:
            self.x[edge] += self.sigma

    def create_new_U_b(self):
        self.U_basis[self.ij_zero[0]].append(self.ij_zero[1])
        self.U_basis[self.ij_astr[0]].remove(self.ij_astr[1])

        self.U_non_basis = self.get_non_basis_edges()

    def solve(self):
        while True:
            self.get_u()
            self.get_deltas()
            if not self.get_invalid_delta():
                raise NotImplemented
            self.find_cycle()
            self.get_sigma()
            self.create_new_x()
            self.create_new_U_b()


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
    x = {
        (1, 2): 1,
        (2, 6): 0,
        (3, 2): 3,
        (3, 4): 1,
        (5, 3): 0,
        (5, 4): 5,
        (6, 1): 0,
        (6, 3): 9,
        (6, 5): 0,
    }
    pm = PotentialMethod(S, U_b, weights, x)
    pm.solve()
