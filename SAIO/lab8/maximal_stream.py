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
            if self.step_four():
                return self.x
            self.step_five()

    def step_two(self):
        i = self.i
        neighbors = self.U[i]
        for j in neighbors:
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
            return 1

    def step_five(self):
        self.I_c += 1
        for p, value in self.p.items():
            if value == self.I_c:
                self.i = p
                return
        raise NotImplemented('End?')

    def recovery_path(self):
        a = []
        i = self.g[self.t]
        a.append(self.d[(i, self.t)] - self.x[(i, self.t)])
        while True:
            q = self.g[i]
            if q >= 0:
                new_a = min([a[-1], self.d[(q, i)] - self.x[(q, i)]])
                a.append(new_a)
            elif q < 0:
                new_a = min([a[-1], self.x[(i, -q)]])
                a.append(new_a)
            i = math.fabs(q)
            if q == self.s:
                break
        i = self.g[self.t]
        while True:
            q = self.g[i]
            if q >= 0:
                self.x[(q, i)] += a[-1]
            elif q < 0:
                self.x[(i, -q)] -= a[-1]
            i = math.fabs(q)
            if q == self.s:
                break


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
