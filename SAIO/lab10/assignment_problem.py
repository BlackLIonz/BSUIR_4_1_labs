import copy
import collections

import numpy as np

from SAIO.lab8.maximal_stream import MaximalStream


class HungarianAlgorithm:
    def __init__(self, array):
        self.matrix = array
        self.n = len(array)
        self.v = self.y = None

    def solve(self):
        self.row_and_column_reduction(self.matrix)
        while True:
            self.v, self.x, self.y = self.new_system()
            if self.v == self.n:
                return self.get_optimal_plan()
            else:
                self.modification_reduced_matrix()

    def get_optimal_plan(self):
        plan = []
        for i in range(1, self.n + 1):
            for j in range(self.n + 1, self.n * 2 + 1):
                if self.x.get((i, j)) == 1:
                    plan.append((i, j - self.n))
        return plan

    def modification_reduced_matrix(self):
        N = {
            1: [i - 1 for i in range(1, self.n + 1) if i in self.y],
            2: [i - self.n - 1 for i in range(self.n + 1, self.n * 2 + 1) if i in self.y]
        }
        c = []
        for i in N[1]:
            for j in [item for item in range(self.n) if item not in N[2]]:
                c.append(self.matrix[i, j])
        alpha = min(c)
        for i in range(self.n):
            for j in range(self.n):
                if i in N[1] and j not in N[2]:
                    self.matrix[i, j] = self.matrix[i, j] - alpha
                elif i not in N[1] and j in N[2]:
                    self.matrix[i, j] = self.matrix[i, j] + alpha

    def new_system(self):
        s = 0
        t = self.n * 2 + 1
        graph = collections.defaultdict(list, {s: list(range(1, self.n + 1))})
        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i, j] == 0:
                    graph[i + 1].append(j + self.n + 1)
        for i in range(self.n + 1, t):
            graph[i].append(t)

        d = self.fill_dict(self.make_pairs(graph), 1)
        x = self.fill_dict(self.make_pairs(graph), 0)
        for i, nodes in graph.items():
            if i not in range(1, self.n + 1):
                continue
            for j in nodes:
                d[i, j] = np.inf
        max_stream = MaximalStream(graph, d, x, s, t, 0)
        x, v = max_stream.solve()
        return v, x, max_stream.L

    @staticmethod
    def row_and_column_reduction(array):
        for i in range(len(array)):
            array[i, :] = array[i, :] - min(array[i, :])
        for j in range(len(array)):
            array[:, j] = array[:, j] - min(array[:, j])

    @staticmethod
    def make_pairs(matrix):
        pairs = []
        for node, neighbors in matrix.items():
            pairs.extend([(node, neighbor) for neighbor in neighbors])
        return pairs

    @staticmethod
    def fill_dict(list, value):
        dict = {}
        for key in list:
            dict[key] = value
        return dict


if __name__ == '__main__':
    matrix = np.array([[2, -1, 9, 4],
                       [3, 2, 5, 1],
                       [13, 0, -3, 4],
                       [5, 6, 1, 2]])
    hungarian = HungarianAlgorithm(matrix)
    plan = hungarian.solve()
    x = [f'X{i}{j}' for i, j in plan]
    print(', '.join(x))
