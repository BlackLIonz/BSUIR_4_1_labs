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
        non_visited_neighbors = set()
        for i in I:
            for j in self.matrix[i]:
                if j not in self.I:
                    non_visited_neighbors.add(j)
        return non_visited_neighbors

    def I_minus(self, i):
        neighbors = []
        for key, value in self.matrix.items():
            if i in value:
                neighbors.append(key)
        return neighbors

    def find_subset(self, I):
        for i in I:
            I_minus = self.I_minus(i)
            if self.if_subset(self.I, I_minus):
                return i

    @staticmethod
    def if_subset(lst, sub_lst):
        return set(sub_lst).issubset(set(lst))

    def solve(self):
        self.I.append(self.s)
        self.B[self.s] = 0
        self.f[self.s] = 0
        while len(self.f) != len(self.matrix):
            w_I = self.w(self.I)
            j_astr = self.find_subset(w_I)
            B_i, i = self.get_B(j_astr)
            self.B[j_astr] = B_i
            self.f[j_astr] = i
            self.I.append(j_astr)
        return self.f

    def get_B(self, j_astr):
        maximum = -np.inf
        max_i = None
        for i in self.I_minus(j_astr):
            new_B = self.B[i] + self.weights[(i, j_astr)]
            if new_B > maximum:
                maximum = new_B
                max_i = i
        return maximum, max_i


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
        (1, 2): 2,
        (1, 6): 1,
        (2, 3): 2,
        (2, 5): 7,
        (3, 4): 1,
        (5, 3): 1,
        (5, 4): 1,
        (6, 2): 4,
        (6, 3): 4,
        (6, 5): 1,
    }
    max_path = MaximalPath(matrix, weights, 1, 4)
    path = max_path.solve()
    pointer = 4
    res = []
    while len(res) != len(path):
        res.append(pointer)
        if pointer != 1:
            pointer = path[pointer]
    print(' -> '.join(str(x) for x in reversed(res)))
