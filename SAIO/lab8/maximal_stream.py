import math

import numpy as np


class MaximalStream:
    def __init__(self, graph, d, x, s, t, v):
        self.U = graph
        self.d = d
        self.x = x
        self.s = s
        self.t = t
        self.v = v
        self.I_c = 1
        self.I_t = 1
        self.L = [s]
        self.g = {s: 0}
        self. i = s
        self.p = {s: 1}

    def solve(self):
        while True:
            self.step_two()
            self.step_three()
            if self.step_four() == 'continue':
                continue
            if not self.step_five():
                return self.x, self.v

    def step_two(self):
        i = self.i
        neighbors = self.U[i]
        for j in neighbors:
            if j in self.L:
                continue
            if self.x[(i, j)] < self.d[(i, j)]:
                self.L.append(j)
                self.g[j] = i
                self.I_t += 1
                self.p[j] = self.I_t

    def step_three(self):
        i = self.i
        for node, neighbors in self.U.items():
            if node in self.L:
                continue
            if i in neighbors and self.x[(node, i)] > 0:
                self.L.append(node)
                self.g[node] = -i
                self.I_t += 1
                self.p[node] = self.I_t

    def step_four(self):
        if self.t in self.L:
            self.recovery_path()
            self.drop_vars()
            return 'continue'

    def drop_vars(self):
        self.I_c = 1
        self.I_t = 1
        self.L = [self.s]
        self.g = {self.s: 0}
        self.i = self.s
        self.p = {self.s: 1}

    def step_five(self):
        self.I_c += 1
        for p, value in self.p.items():
            if value == self.I_c:
                self.i = p
                return True
        return False

    def recovery_path(self):
        a = []
        path = [self.t]
        i = self.g[self.t]
        a.append(self.d[i, self.t] - self.x[i, self.t])
        while i != self.s:
            path.append(i)
            s = math.fabs(i)
            i = self.g[s]
            if i >= 0:
                a.append(min(a[-1], self.d[i, s] - self.x[i, s]))
            else:
                a.append(min(a[-1], self.x[s, -i]))
        path.append(self.s)
        a_m = a[-1]
        for i in range(len(path) - 1):
            i, j = path[i: i + 2]
            if i < 0:
                i = math.fabs(i)
            if j < 0:
                i, j = math.fabs(j), i
            self.x[j, i] = self.x[j, i] + a_m
        self.v = self.v + a_m



if __name__ == '__main__':
    s = 0
    t = 6
    graph = {s: [1, 3],
             1: [3, 4],
             2: [4, 5],
             3: [2, 5],
             4: [5, t],
             5: [t],
             t: []}
    d = {(s, 1): 4,
         (s, 3): 9,
         (1, 3): 2,
         (1, 4): 4,
         (2, 4): 1,
         (2, 5): 10,
         (3, 2): 1,
         (3, 5): 6,
         (4, 5): 1,
         (4, t): 2,
         (5, t): 9}
    x = {(s, 1): 4,
         (s, 3): 5,
         (1, 3): 2,
         (1, 4): 2,
         (2, 4): 1,
         (2, 5): 0,
         (3, 2): 1,
         (3, 5): 6,
         (4, 5): 1,
         (4, t): 2,
         (5, t): 7}
    max_stream = MaximalStream(graph, d, x, s, t, 9)
    print(max_stream.solve())
